#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
 This sample demonstrates how to upload multiparts to OBS
 using the OBS SDK for Python.
'''

AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'yourdomainname'
bucketName = 'my-obs-bucket-demo'
objectKey = 'my-obs-object-key-demo'

from com.obs.client.obs_client import ObsClient
# Constructs a obs client instance with your account for accessing OBS
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)

# Create bucket
print('Create a new bucket for demo\n')
obsClient.createBucket(bucketName)

# Step 1: initiate multipart upload
print('Step 1: initiate multipart upload \n')
resp = obsClient.initiateMultipartUpload(bucketName, objectKey)
uploadId = resp.body.uploadId

# Step 2: upload a part
print('Step 2: upload a part\n')

partNum = 1
resp = obsClient.uploadPart(bucketName, objectKey, partNumber=partNum, uploadId=uploadId, object='Hello OBS')
etag = dict(resp.header).get('etag')

# Step 3: complete multipart upload
print('Step 3: complete multipart upload\n')
from com.obs.models.complete_multipart_upload_request import CompletePart, CompleteMultipartUploadRequest
obsClient.completeMultipartUpload(bucketName, objectKey, uploadId, CompleteMultipartUploadRequest([CompletePart(partNum=partNum, etag=etag)]))
