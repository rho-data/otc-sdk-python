#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
 This sample demonstrates how to download an cold object
 from OBS using the OBS SDK for Python.
'''

AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'yourdomainname'
bucketName = 'my-obs-cold-bucket-demo'
objectKey = 'my-obs-cold-object-key-demo'

from com.obs.client.obs_client import ObsClient
# Constructs a obs client instance with your account for accessing OBS
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)

# Create a cold bucket
print('Create a new cold bucket for demo\n')
from com.obs.models.create_bucket_header import CreateBucketHeader
obsClient.createBucket(bucketName, CreateBucketHeader(storageClass='GLACIER'))

# Create a cold object
print('Create a new cold object for demo\n')
obsClient.putContent(bucketName, objectKey, 'Hello OBS')

# Restore the cold object
print('Restore the cold object')
obsClient.restoreObject(bucketName, objectKey, 1, tier='Expedited')


# Wait 6 minute to get the object
import time
time.sleep(6 * 60)

# Get the cold object status
print('Get the cold object status')
resp = obsClient.restoreObject(bucketName, objectKey, 1, tier='Expedited')
print('\tstatus code ' + str(resp.status))

# Get the cold object
print('Get the cold object')
resp = obsClient.getObject(bucketName, objectKey, loadStreamInMemory=True)
print('\tobject content:%s' % resp.body.buffer)

# Delete the cold object
obsClient.deleteObject(bucketName, objectKey)
