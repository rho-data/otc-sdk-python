#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
This sample demonstrates how to post object under specified bucket from
OBS using the OBS SDK for Python.
'''

AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'yourdomainname'
bucketName = 'my-obs-bucket-demo'
objectKey = 'my-obs-object-key-demo'

import sys, os
IS_PYTHON2 = sys.version_info.major == 2 or sys.version < '3'

if IS_PYTHON2:
    import httplib
else:
    import http.client as httplib

def createSampleFile(sampleFilePath):
    if not os.path.exists(sampleFilePath):
        _dir = os.path.dirname(sampleFilePath)
        if not os.path.exists(_dir):
            os.makedirs(_dir, mode=0o755)
        import uuid
        with open(sampleFilePath, 'w') as f:
            f.write(str(uuid.uuid1()) + '\n')
            f.write(str(uuid.uuid4()) + '\n')
    return sampleFilePath

from com.obs.client.obs_client import ObsClient
# Constructs a obs client instance with your account for accessing OBS
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)


# Create bucket
print('Create a new bucket for demo\n')
obsClient.createBucket(bucketName)

# Create sample file
sampleFilePath = '/temp/text.txt'
createSampleFile(sampleFilePath)

# Claim a post object request
formParams = {'acl': 'public-read', 'content-type': 'text/plain', 'x-amz-meta-meta1': 'value1', 'x-amz-meta-meta2': 'value2'}
res = obsClient.createV4PostSignature(bucketName, objectKey, expires=3600, formParams=formParams)

# Start to post object
formParams['key'] = objectKey
formParams['policy'] = res['policy']
formParams['x-amz-algorithm'] = res['algorithm']
formParams['x-amz-credential'] = res['credential']
formParams['x-amz-date'] = res['date']
formParams['x-amz-signature'] = res['signature']

print('Creating object in v4 post way')
boundary = '9431149156168'

buffers = []
contentLength = 0

# Construct form data
buffer = []
first = True
for key, value in formParams.items():
    if not first:
        buffer.append('\r\n')
    else:
        first = False

    buffer.append('--')
    buffer.append(boundary)
    buffer.append('\r\n')
    buffer.append('Content-Disposition: form-data; name="')
    buffer.append(str(key))
    buffer.append('"\r\n\r\n')
    buffer.append(str(value))

buffer = ''.join(buffer)
buffer = buffer if IS_PYTHON2 else buffer.encode('UTF-8')
contentLength += len(buffer)
buffers.append(buffer)

# Construct file description
buffer = []
buffer.append('\r\n')
buffer.append('--')
buffer.append(boundary)
buffer.append('\r\n')
buffer.append('Content-Disposition: form-data; name="file"; filename="')
buffer.append('myfile')
buffer.append('"\r\n')
buffer.append('Content-Type: text/plain')
buffer.append('\r\n\r\n')

buffer = ''.join(buffer)
buffer = buffer if IS_PYTHON2 else buffer.encode('UTF-8')
contentLength += len(buffer)
buffers.append(buffer)

# Contruct end data
buffer = []
buffer.append('\r\n--')
buffer.append(boundary)
buffer.append('--\r\n')

buffer = ''.join(buffer)
buffer = buffer if IS_PYTHON2 else buffer.encode('UTF-8')
contentLength += len(buffer)
buffers.append(buffer)

contentLength += os.path.getsize(sampleFilePath)


conn = httplib.HTTPConnection(server, 80)
conn.request('POST', '/' + bucketName, headers={'Content-Length': str(contentLength), 'User-Agent': 'OBS/Test', 'Content-Type': 'multipart/form-data; boundary=' + boundary})

# Send form data
conn.send(buffers[0])

# Send file description
conn.send(buffers[1])

# Send file data
with open(sampleFilePath, 'rb') as f:
    while True:
        chunk = f.read(65536)
        if not chunk:
            break
        conn.send(chunk)

# Send end data
conn.send(buffers[2])


result = conn.getresponse()
status = result.status
responseContent = result.read()
if status < 300:
    print('Post object successfully.')
else:
    print('Post object failed!!')

if responseContent:
    print('\tresponseContent:')
    print('\t%s' % responseContent)
conn.close()
print('\n')

if os.path.exists(sampleFilePath):
    os.remove(sampleFilePath)
