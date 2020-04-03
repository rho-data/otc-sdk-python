#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
  This sample demonstrates how to do bucket-related operations
  (such as do bucket ACL/CORS/Lifecycle/Logging/Website/Location/Tagging/OPTIONS)
  on OBS using the OBS SDK for Python.
'''

AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'yourdomainname'
bucketName = 'my-obs-bucket-demo'

from com.obs.client.obs_client import ObsClient
# Constructs a obs client instance with your account for accessing OBS
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server)

def createBucket():
    resp = obsClient.createBucket(bucketName)
    if resp.status < 300:
        print('Create bucket:' + bucketName + ' successfully!\n')
    else:
        print(resp.errorCode)

def getBucketLocation():
    resp = obsClient.getBucketLocation(bucketName)
    if resp.status < 300:
        print('Getting bucket location ' + str(resp.body) + ' \n')
    else:
        print(resp.errorCode)

def getBucketStorageInfo():
    resp = obsClient.getBucketStorageInfo(bucketName)
    if resp.status < 300:
        print('Getting bucket storageInfo ' + str(resp.body) + ' \n')
    else:
        print(resp.errorCode)

def doBucketQuotaOperation():
    # Set bucket quota to 1GB
    obsClient.setBucketQuota(bucketName, 1024 * 1024 * 1024)

    resp = obsClient.getBucketQuota(bucketName)

    print('Getting bucket quota ' + str(resp.body) + ' \n')

def doBucketVersioningOperation():
    print('Getting bucket versioning config ' + str(obsClient.getBucketVersioningConfiguration(bucketName).body) + ' \n')
    # Enable bucket versioning
    obsClient.setBucketVersioningConfiguration(bucketName, 'Enabled')
    print('Current bucket versioning config ' + str(obsClient.getBucketVersioningConfiguration(bucketName).body) + ' \n')

    # Suspend bucket versioning
    obsClient.setBucketVersioningConfiguration(bucketName, 'Suspended')
    print('Current bucket versioning config ' + str(obsClient.getBucketVersioningConfiguration(bucketName).body) + ' \n')

def doBucketAclOperation():
    print('Setting bucket ACL to public-read \n')
    obsClient.setBucketAcl(bucketName, aclControl='public-read')

    print('Getting bucket ACL ' + str(obsClient.getBucketAcl(bucketName).body) + ' \n')

    print('Setting bucket ACL to private \n')
    obsClient.setBucketAcl(bucketName, None, 'private')

    print('Getting bucket ACL ' + str(obsClient.getBucketAcl(bucketName).body) + ' \n')


def doBucketCorsOperation():
    print('Setting bucket CORS\n')
    from com.obs.models.cors_rule import CorsRule
    cors1 = CorsRule(id='rule1', allowedMethod=['PUT', 'HEAD', 'GET'],
                     allowedOrigin=['http://www.a.com', 'http://www.b.com'], allowedHeader=['Authorization1'],
                     maxAgeSecond=100, exposeHeader=['x-obs-test1'])
    cors2 = CorsRule(id='rule2', allowedMethod=['PUT', 'HEAD', 'GET'],
                     allowedOrigin=['http://www.c.com', 'http://www.d.com'], allowedHeader=['Authorization2'],
                     maxAgeSecond=200, exposeHeader=['x-obs-test2'])

    corsList = [cors1, cors2]

    obsClient.setBucketCors(bucketName, corsList)

    print('Getting bucket CORS ' + str(obsClient.getBucketCors(bucketName).body) + '\n')

def optionsBucket():
    print('Options bucket \n')
    from com.obs.models.options import Options
    option = Options(origin='http://www.a.com', accessControlRequestMethods=['GET', 'PUT'],
                     accessControlRequestHeaders=['Authorization1'])
    print('\t' + str(obsClient.optionsBucket(bucketName, option).body))

def getBucketMetadata():
    print('Getting bucket metadata\n')

    resp = obsClient.getBucketMetadata(bucketName, origin='http://www.b.com', requestHeaders='Authorization1')
    print('storageClass:', resp.body.storageClass)
    print('accessContorlAllowOrigin:', resp.body.accessContorlAllowOrigin)
    print('accessContorlMaxAge:', resp.body.accessContorlMaxAge)
    print('accessContorlExposeHeaders:', resp.body.accessContorlExposeHeaders)
    print('accessContorlAllowMethods:', resp.body.accessContorlAllowMethods)
    print('accessContorlAllowHeaders:', resp.body.accessContorlAllowHeaders)

    print('Deleting bucket CORS\n')
    obsClient.deleteBucketCors(bucketName)

def doBucketLifycleOperation():
    print('Setting bucket lifecycle\n')

    from com.obs.models.expiration import Expiration, NoncurrentVersionExpiration
    from com.obs.models.rule import Rule
    from com.obs.models.lifecycle import Lifecycle
    from com.obs.models.date_time import DateTime

    rule1 = Rule(id='delete obsoleted files', prefix='obsoleted/', status='Enabled', expiration=Expiration(days=10))
    rule2 = Rule(id='delete temporary files', prefix='temporary/', status='Enabled', expiration=Expiration(date=DateTime(2017, 12, 31)))
    rule3 = Rule(id='delete temp files', prefix='temp/', status='Enabled', noncurrentVersionExpiration=NoncurrentVersionExpiration(noncurrentDays=10))

    Llifecycle = Lifecycle(rule=[rule1, rule2, rule3])
    obsClient.setBucketLifecycleConfiguration(bucketName, Llifecycle)

    print('Getting bucket lifecycle:')
    resp = obsClient.getBucketLifecycleConfiguration(bucketName)
    print('\t' + str(resp.body) + '\n')

    print('Deleting bucket lifecyle\n')
    obsClient.deleteBucketLifecycleConfiguration(bucketName)

def doBucketLoggingOperation():
    print('Setting bucket logging\n')

    obsClient.setBucketAcl(bucketName, None, 'log-delivery-write')

    from com.obs.models.logging import Logging
    obsClient.setBucketLoggingConfiguration(bucketName, Logging(targetBucket=bucketName, targetPrefix='log-'))

    print('Getting bucket logging:')
    print('\t' + str(obsClient.getBucketLoggingConfiguration(bucketName).body) + '\n')

    print('Deleting bucket logging\n')
    obsClient.setBucketLoggingConfiguration(bucketName, Logging())

    print('Getting bucket logging:')
    print('\t' + str(obsClient.getBucketLoggingConfiguration(bucketName).body) + '\n')

def doBucketWebsiteOperation():
    print('Setting bucket website\n')
    from com.obs.models.website_configuration import WebsiteConfiguration
    from com.obs.models.index_document import IndexDocument
    from com.obs.models.error_document import ErrorDocument
    Lwebsite = WebsiteConfiguration(indexDocument=IndexDocument(suffix='index.html'), errorDocument=ErrorDocument(key='error.html'))
    obsClient.setBucketWebsiteConfiguration(bucketName, Lwebsite)

    print('Getting bucket website:')
    print('\t' + str(obsClient.getBucketWebsiteConfiguration(bucketName).body) + '\n')
    print('Deleting bucket website\n')
    obsClient.deleteBucketWebsiteConfiguration(bucketName)

def doBucketTaggingOperation():
    print('Setting bucket tagging\n')
    from com.obs.models.tag import TagInfo
    tagInfo = TagInfo()
    tagInfo.addTag('key1', 'value1').addTag('关键字', '测试值')
    resp = obsClient.setBucketTagging(bucketName, tagInfo)
    
    if resp.status < 300:
        print('Getting bucket tagging\n')
        resp = obsClient.getBucketTagging(bucketName)
        for item in resp.body.tagSet:
            print('\t' + item.key + ':' + item.value + '\n')
    
        print('Deleting bucket tagging\n')
        obsClient.deleteBucketTagging(bucketName)
    else:
        print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

def deleteBucket():
    print('Deleting bucket ' + bucketName + '\n')
    resp = obsClient.deleteBucket(bucketName)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)


# Put bucket operation
createBucket()

# Get bucket location operation
getBucketLocation()

# Get bucket storageInfo operation
getBucketStorageInfo()

# Put/Get bucket quota operations
doBucketQuotaOperation()

# Put/Get bucket versioning operations
doBucketVersioningOperation()

# Put/Get bucket acl operations
doBucketAclOperation()

# Put/Get/Delete bucket cors operations
doBucketCorsOperation()

# Options bucket operation
optionsBucket()

# Get bucket metadata operation
getBucketMetadata()

# Put/Get/Delete bucket lifecycle operations
doBucketLifycleOperation()

# Put/Get/Delete bucket logging operations
doBucketLoggingOperation()

# Put/Get/Delete bucket website operations
doBucketWebsiteOperation()

# Put/Get/Delete bucket tagging operations
doBucketTaggingOperation()

# Delete bucket operation
deleteBucket()
