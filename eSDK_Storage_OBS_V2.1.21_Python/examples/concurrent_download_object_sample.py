#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
 This sample demonstrates how to download an object concurrently
 from OBS using the OBS SDK for Python.
'''


AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'yourdomainname'
bucketName = 'my-obs-bucket-demo'
objectKey = 'my-obs-object-key-demo'

localFilePath = '/temp/' + objectKey

import platform, os, threading, multiprocessing
IS_WINDOWS = platform.system() == 'Windows' or os.name == 'nt'

def createSampleFile(sampleFilePath):
    if not os.path.exists(sampleFilePath):
        _dir = os.path.dirname(sampleFilePath)
        if not os.path.exists(_dir):
            os.makedirs(_dir, mode=0o755)
        import uuid
        index = 1000000
        with open(sampleFilePath, 'w') as f:
            while index >= 0:
                f.write(str(uuid.uuid1()) + '\n')
                f.write(str(uuid.uuid4()) + '\n')
                index -= 1
    return sampleFilePath

from com.obs.client.obs_client import ObsClient

def doGetObject(lock, completedBlocks, bucketName, objectKey, startPos, endPos, i):
    from com.obs.models.get_object_header import GetObjectHeader
    if IS_WINDOWS:
        global obsClient
    else:
        obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)
    resp = obsClient.getObject(bucketName, objectKey, headers=GetObjectHeader(range='%d-%d' % (startPos, endPos)))
    if resp.status < 300:
        response = resp.body.response
        chunk_size = 65536
        if response is not None:
            with open(localFilePath, 'rb+') as f:
                f.seek(startPos, 0)
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                response.close()
        print('Part#', i+1, 'done\n')
        lock.acquire()
        try:
            completedBlocks.value += 1
        finally:
            lock.release()

if __name__ == '__main__':
    # Constructs a obs client instance with your account for accessing OBS
    obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)
    # Create bucket
    print('Create a new bucket to upload file\n')
    obsClient.createBucket(bucketName)

    sampleFilePath = '/temp/test.txt'
    # Upload an object to your bucket
    print('Uploading a new object to OBS from a file\n')
    obsClient.putFile(bucketName, objectKey, createSampleFile(sampleFilePath))

    if os.path.exists(sampleFilePath):
        os.remove(sampleFilePath)

    # Get size of the object
    resp = obsClient.getObjectMetadata(bucketName, objectKey)
    header = dict(resp.header)
    objectSize = int(header.get('content-length'))

    print('Object size ' + str(objectSize) + '\n')

    # Calculate how many blocks to be divided
    # 5MB
    blockSize = 5 * 1024 * 1024
    blockCount = int(objectSize / blockSize)
    if objectSize % blockSize != 0:
        blockCount += 1

    print('Total blocks count ' + str(blockCount) + '\n')

    # Download the object concurrently
    print('Start to download ' + objectKey + '\n')

    if os.path.exists(localFilePath):
        os.remove(localFilePath)

    lock = threading.Lock() if IS_WINDOWS else multiprocessing.Lock()
    proc = threading.Thread if IS_WINDOWS else multiprocessing.Process

    class Temp(object):
        pass

    completedBlocks = Temp() if IS_WINDOWS else multiprocessing.Value('i', 0)

    if IS_WINDOWS:
        completedBlocks.value = 0

    processes = []
    
    with open(localFilePath, 'wb') as f:
        pass 

    for i in range(blockCount):
        startPos = i * blockSize
        endPos = objectSize - 1 if (i + 1) == blockCount else ((i + 1) * blockSize - 1)
        p = proc(target=doGetObject, args=(lock, completedBlocks, bucketName, objectKey, startPos, endPos, i))
        p.daemon = True
        processes.append(p)


    for p in processes:
        p.start()

    for p in processes:
        p.join()

    if not IS_WINDOWS and completedBlocks.value != blockCount:
        raise Exception('Download fails due to some blocks are not finished yet')

    print('Succeed to download object ' + objectKey + '\n')

    print('Deleting object ' + objectKey + '\n')
    obsClient.deleteObject(bucketName, objectKey)
