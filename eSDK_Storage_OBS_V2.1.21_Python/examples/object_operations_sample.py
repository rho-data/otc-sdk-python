#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
 This sample demonstrates how to do object-related operations
 (such as create/delete/get/copy object, do object ACL/OPTIONS)
 on OBS using the OBS SDK for Python.
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

# Create object
resp = obsClient.putContent(bucketName, objectKey, 'Hello OBS')
if resp.status < 300:
    print('Create object ' + objectKey + ' successfully!\n')

# Get object metadata
print('Getting object metadata')
resp = obsClient.putContent(bucketName, objectKey, 'Hello OBS')
print('\t' + str(resp.header))

# Get object
print('Getting object content')
resp = obsClient.getObject(bucketName, objectKey, loadStreamInMemory=True)
print('\tobject content:%s' % resp.body.buffer)

# Copy object
print('Copying object\n')
destObjectKey = objectKey + '-back'
resp = obsClient.copyObject(sourceBucketName=bucketName, sourceObjectKey=objectKey, destBucketName=bucketName, destObjectKey=destObjectKey)
if resp.status < 300:
    print('Copy object ' + destObjectKey + ' successfully!\n')

# Options object

from com.obs.models.cors_rule import CorsRule
cors1 = CorsRule(id='rule1', allowedMethod=['PUT', 'HEAD', 'GET'],
                 allowedOrigin=['http://www.a.com', 'http://www.b.com'], allowedHeader=['Authorization1'],
                 maxAgeSecond=100, exposeHeader=['x-obs-test1'])
corsList = [cors1]
obsClient.setBucketCors(bucketName, corsList)

from com.obs.models.options import Options
print('Options object:')
options = Options(origin='http://www.a.com', accessControlRequestMethods=['PUT'])
resp = obsClient.optionsObject(bucketName, objectKey, options)
print(resp.body)


# Put/Get object acl operations
print('Setting object ACL to public-read \n')
obsClient.setObjectAcl(bucketName, objectKey, aclControl='public-read')

print('Getting object ACL ' + str(obsClient.getObjectAcl(bucketName, objectKey).body) + '\n')
print('Setting object ACL to private \n')

print('Getting object ACL ' + str(obsClient.getObjectAcl(bucketName, objectKey).body) + '\n')

# Delete object
print('Deleting objects\n')
obsClient.deleteObject(bucketName, objectKey)
obsClient.deleteObject(bucketName, destObjectKey)
