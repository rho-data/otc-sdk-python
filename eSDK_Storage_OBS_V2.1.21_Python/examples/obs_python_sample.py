#!/usr/bin/python
# -*- coding:utf-8 -*-

from com.obs.client.obs_client import ObsClient
from com.obs.models.create_bucket_header import CreateBucketHeader
from com.obs.models.head_permission import HeadPermission
from com.obs.models.grant import Grant, Permission
from com.obs.models.grantee import Grantee, Group
from com.obs.models.owner import Owner
from com.obs.models.acl import ACL
from com.obs.models.versions import Versions
from com.obs.models.rule import Rule
from com.obs.models.lifecycle import Lifecycle
from com.obs.models.expiration import Expiration, NoncurrentVersionExpiration
from com.obs.models.date_time import DateTime
from com.obs.models.condition import Condition
from com.obs.models.redirect import Redirect
from com.obs.models.routing_rule import RoutingRule
from com.obs.models.error_document import ErrorDocument
from com.obs.models.index_document import IndexDocument
from com.obs.models.redirect_all_request_to import RedirectAllRequestTo
from com.obs.models.website_configuration import WebsiteConfiguration
from com.obs.models.tag import TagInfo
from com.obs.models.logging import Logging
from com.obs.models.cors_rule import CorsRule
from com.obs.models.options import Options
from com.obs.models.notification import Notification, TopicConfiguration, FilterRule
from com.obs.models.delete_objects_request import DeleteObjectsRequest, Object
from com.obs.models.restore import TierType
from com.obs.models.complete_multipart_upload_request import CompleteMultipartUploadRequest, CompletePart
from com.obs.models.list_multipart_uploads_request import ListMultipartUploadsRequest
from com.obs.models.put_object_header import PutObjectHeader
from com.obs.models.copy_object_header import CopyObjectHeader
from com.obs.models.get_object_header import GetObjectHeader
from com.obs.models.get_object_request import GetObjectRequest
from com.obs.response.get_object_response import ObjectStream
from com.obs.models.server_side_encryption import SseKmsHeader, SseCHeader
from com.obs.log.Log import LogConf


AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'yourdomainname'
region = 'region'
secure = True

# create ObsClient instance
TestObs = ObsClient(access_key_id=AK, secret_access_key=SK, is_secure=secure, server=server, region=region)

# init log
def initLog():
    TestObs.initLog(LogConf('../log.conf'), 'test_client')

# create bucket
def CreateBucket():
    headers = CreateBucketHeader(aclControl=HeadPermission.PUBLIC_READ, storageClass='STANDARD_IA')

    resp = TestObs.createBucket(bucketName='bucket001', header=headers, location=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)

# delete bucket
def DeleteBucket():
    resp = TestObs.deleteBucket(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)

# list buckets
def ListBuckets():
    resp = TestObs.listBuckets()
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

    listBucket = resp.body
    if listBucket:
        print('owner_id:', listBucket.owner.owner_id, ',owner_name:', listBucket.owner.owner_name)
        i = 0
        for item in listBucket.buckets:
            print('buckets[', i, ']:')
            print('bucket_name:', item.name, ',create_date:', item.create_date)
            i += 1

# head bucket
def HeadBucket():
    resp = TestObs.headBucket(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',resHeader:', resp.header)

# get bucket metadata
def GetBucketMetadata():
    resp = TestObs.getBucketMetadata(bucketName='bucket001', origin='www.example.com', requestHeaders='header1')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('storageClass:', resp.body.storageClass)
        print('accessContorlAllowOrigin:', resp.body.accessContorlAllowOrigin)
        print('accessContorlMaxAge:', resp.body.accessContorlMaxAge)
        print('accessContorlExposeHeaders:', resp.body.accessContorlExposeHeaders)
        print('accessContorlAllowMethods:', resp.body.accessContorlAllowMethods)
        print('accessContorlAllowHeaders:', resp.body.accessContorlAllowHeaders)


# set bucket quota
def SetBucketQuota():
    resp = TestObs.setBucketQuota(bucketName='bucket001', quota=1048576 * 600)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket quota
def GetBucketQuota():
    resp = TestObs.getBucketQuota(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('quota:', resp.body.quota)

# set bucket storagePolicy
def SetBucketStoragePolicy():
    resp = TestObs.setBucketStoragePolicy(bucketName='bucket001', storageClass='STANDARD')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket storagePolicy
def GetBucketStoragePolicy():
    resp = TestObs.getBucketStoragePolicy(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('storageClass:', resp.body.storageClass)

# get bucket storageinfo
def GetBucketStorageInfo():
    resp = TestObs.getBucketStorageInfo(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('size:', resp.body.size, ',objectNumber:', resp.body.objectNumber)

# set bucket acl
def SetBucketAcl():
    Lowner = Owner(owner_id='ownerid', owner_name='ownername')

    Lgrantee1 = Grantee(grantee_id='userid', grantee_name='username', group=None)
    Lgrantee2 = Grantee(group=Group.LOG_DELIVERY)

    Lgrant1 = Grant(grantee=Lgrantee1, permission=Permission.READ)
    Lgrant2 = Grant(grantee=Lgrantee2, permission=Permission.READ_ACP)
    Lgrant3 = Grant(grantee=Lgrantee2, permission=Permission.WRITE)
    Lgrants = [Lgrant1, Lgrant2, Lgrant3]

    Lacl = ACL(owner=Lowner, grants=Lgrants)

    resp = TestObs.setBucketAcl(bucketName='bucket001', acl=Lacl, aclControl=None)
    # resp = TestObs.setBucketAcl(bucketName='bucket001', acl=None, aclControl=HeadPermission.PUBLIC_READ_WRITE)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket acl
def GetBucketAcl():
    resp = TestObs.getBucketAcl(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('owner_id:', resp.body.owner.owner_id, ',owner_name:', resp.body.owner.owner_name)
        i = 0
        for grant in resp.body.grants:
            print('grants[', i, ']:')
            print('permission:', grant.permission)
            print('grantee_name:', grant.grantee.grantee_name, ',grantee_id:', grant.grantee.grantee_id, ',group:', grant.grantee.group)
            i += 1

# set bucket policy
def SetBucketPolicy():
    LpolicyJSON = '''{'Version':'2008-10-17','Id': 'Policy1375342051334','Statement': [{'Sid': 'Stmt1375240018061','Action': ['s3:GetBucketPolicy'],'Effect': 'Allow','Resource': 'arn:aws:s3:::bucket001','Principal': { 'AWS': ['*'] } }]}'''
    resp = TestObs.setBucketPolicy(bucketName='bucket001', policyJSON=LpolicyJSON)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket policy
def GetBucketPolicy():
    resp = TestObs.getBucketPolicy(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('policyJSON:', resp.body)

# delete bucket policy
def DeleteBucketPolicy():
    resp = TestObs.deleteBucketPolicy(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# set bucket versioning configuration
def SetBucketVersioningConfiguration():
    resp = TestObs.setBucketVersioningConfiguration(bucketName='bucket001', status='Enabled')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket versioning configuration
def GetBucketVersioningConfiguration():
    resp = TestObs.getBucketVersioningConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    print('status:', resp.body)

# list versions
def ListVersions():
    Lversion = Versions(prefix=None, key_marker=None, max_keys=2, delimiter=None, version_id_marker=None)

    resp = TestObs.listVersions(bucketName='bucket001', version=Lversion)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('name:', resp.body.head.name, ',prefix:', resp.body.head.prefix, ',keyMarker:', resp.body.head.keyMarker, ',maxKeys:', resp.body.head.maxKeys)
        print('nextKeyMarker:', resp.body.head.nextKeyMarker, ',nextVersionIdMarker:', resp.body.head.nextVersionIdMarker, ',versionIdMarker:', resp.body.head.versionIdMarker, ',isTruncated:', resp.body.head.isTruncated)
        i = 0
        for version in resp.body.versions:
            print('versions[', i, ']:')
            print('owner_id:', version.owner.owner_id, ',owner_name:', version.owner.owner_name)
            print('key:', version.key)
            print('lastModified:', version.lastModified, ',versionId:', version.versionId, ',eTag:', version.eTag, ',storageClass:', version.storageClass, ',isLatest:', version.isLatest, ',size:', version.size)
            i += 1
        i = 0
        for marker in resp.body.markers:
            print('markers[', i, ']:')
            print('owner_id:', marker.owner.owner_id, ',owner_name:', marker.owner.owner_name)
            print('key:', marker.key)
            print('key:', marker.key, ',versionId:', marker.versionId, ',isLatest:', marker.isLatest, ',lastModified:', marker.lastModified)
            i += 1
        i = 0
        for Prefix in resp.body.commonPrefixs:
            print('commonPrefixs[', i, ']')
            print('prefix:', Prefix.prefix)
            i += 1

# list objects
def ListObjects():
    resp = TestObs.listObjects(bucketName='bucket001', prefix=None, marker=None, max_keys=2, delimiter=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('name:', resp.body.name, ',prefix:', resp.body.prefix, ',marker:', resp.body.marker, ',max_keys:', resp.body.max_keys)
        print('delimiter:', resp.body.delimiter, ',is_truncated:', resp.body.is_truncated, ',next_marker:', resp.body.next_marker)
        i = 0
        for content in resp.body.contents:
            print('contents[', i, ']:')
            print('owner_id:', content.owner.owner_id, ',owner_name:', content.owner.owner_name)
            print('key:', content.key, ',lastmodified:', content.lastmodified, ',etag:', content.etag, ',size:', content.size, ',storageClass:', content.storageClass)
            i += 1
        i = 0
        for prefix in resp.body.commonprefixs:
            print('commonprefixs[', i, ']:')
            print('prefix:', prefix.prefix)
            i += 1


# set bucket lifecycle configuration
def SetBucketLifecycleConfiguration():
    Lexpiration = Expiration(date=DateTime(2030, 6, 10), days=None)

    noncurrentVersionExpiration = NoncurrentVersionExpiration(noncurrentDays=60)

    Lrule = Rule(id='101', prefix='test', status='Enabled', expiration=Lexpiration, noncurrentVersionExpiration=noncurrentVersionExpiration)

    Lrules = [Lrule]
    Llifecycle = Lifecycle(rule=Lrules)

    resp = TestObs.setBucketLifecycleConfiguration(bucketName='bucket001', lifecycle=Llifecycle)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket lifecycle configuration
def GetBucketLifecycleConfiguration():
    resp = TestObs.getBucketLifecycleConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        i = 0
        for rule in resp.body.lifecycleConfig.rule:
            print('rule[', i, ']:')
            print('id:', rule.id, ',prefix:', rule.prefix, ',status:', rule.status)
            print('expiration:', rule.expiration)
            print('noncurrentVersionExpiration:', rule.noncurrentVersionExpiration)
            i += 1

# delete bucket lifecycle configuration
def DeleteBucketLifecycleConfiguration():
    resp = TestObs.deleteBucketLifecycleConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# set bucket website configuration
def SetBucketWebsiteConfiguration():
    Lweb = RedirectAllRequestTo(hostName='www.xxx.com', protocol='http')

    Lindex = IndexDocument(suffix='index.html')

    Lerr = ErrorDocument(key='error.html')

    Lcondition = Condition(keyPrefixEquals=None, httpErrorCodeReturnedEquals=404)

    Lredirect = Redirect(protocol='http', hostName=None, replaceKeyPrefixWith=None, replaceKeyWith='NotFound.html',
                         httpRedirectCode=None)

    Lrout = RoutingRule(condition=Lcondition, redirect=Lredirect)

    Lrouts = [Lrout, Lrout]
    Lwebsite = WebsiteConfiguration(redirectAllRequestTo=None, indexDocument=Lindex, errorDocument=Lerr,
                                    routingRules=Lrouts)

    resp = TestObs.setBucketWebsiteConfiguration(bucketName='bucket001', website=Lwebsite)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket website configuration
def GetBucketWebsiteConfiguration():
    resp = TestObs.getBucketWebsiteConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        if resp.body.redirectAllRequestTo:
            print('redirectAllRequestTo.hostName:', resp.body.redirectAllRequestTo.hostName, ',redirectAllRequestTo.Protocol:', resp.body.redirectAllRequestTo.Protocol)
        if resp.body.indexDocument:
            print('indexDocument.suffix:', resp.body.indexDocument.suffix)
        if resp.body.errorDocument:
            print('errorDocument.key:', resp.body.errorDocument.key)
        if resp.body.routingRules:
            i = 0
            for rout in resp.body.routingRules:
                print('routingRule[', i, ']:')
                i += 1
                print('condition.keyPrefixEquals:', rout.condition.keyPrefixEquals, ',condition.httpErrorCodeReturnedEquals:', rout.condition.httpErrorCodeReturnedEquals)
                print('redirect.protocol:', rout.redirect.protocol, ',redirect.hostName:', rout.redirect.hostName, ',redirect.replaceKeyPrefixWith:', rout.redirect.replaceKeyPrefixWith, ',redirect.replaceKeyWith:', rout.redirect.replaceKeyWith, ',redirect.httpRedirectCode:', rout.redirect.httpRedirectCode)

# delete bucket website configuration
def DeleteBucketWebsiteConfiguration():
    resp = TestObs.deleteBucketWebsiteConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# set bucket logging configuration
def SetBucketLoggingConfiguration():
    Lgrantee = Grantee(grantee_id='userid', grantee_name='username', group=None)
    Lgrantee1 = Grantee(grantee_id=None, grantee_name=None, group=Group.ALL_USERE)

    Lgrant1 = Grant(grantee=Lgrantee, permission=Permission.WRITE)
    Lgrant2 = Grant(grantee=Lgrantee1, permission=Permission.READ)

    LgrantList = [Lgrant1, Lgrant2]
    Llog = Logging(targetBucket='bucket003', targetPrefix='log_1', targetGrants=LgrantList)

    resp = TestObs.setBucketLoggingConfiguration(bucketName='bucket001', logstatus=Llog)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket logging configuration
def GetBucketLoggingConfiguration():
    resp = TestObs.getBucketLoggingConfiguration(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('targetBucket:', resp.body.targetBucket, 'targetPrefix:', resp.body.targetPrefix)
        i = 0
        for grant in resp.body.targetGrants:
            print('targetGrant[', i, ']:')
            i += 1
            print('permission:', grant.permission, ',grantee.grantee_id:', grant.grantee.grantee_id, ',grantee.grantee_name:', grant.grantee.grantee_name, ',grantee.group:', grant.grantee.group)

# get bucket location
def GetBucketLocation():
    resp = TestObs.getBucketLocation(bucketName='bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('location:', resp.body.location)

# set bucket tagging
def SetBucketTagging():
    tagInfo = TagInfo()
    tagInfo.addTag('testKey1', 'testValue1').addTag('testKey2','testValue2')
    resp = TestObs.setBucketTagging(bucketName='bucket001', tagInfo=tagInfo)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# delete bucket tagging
def DeleteBucketTagging():
    resp = TestObs.deleteBucketTagging('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket tagging
def GetBucketTagging():
    resp = TestObs.getBucketTagging('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    for tag in resp.body.tagSet:
        print('{0}:{1}'.format(tag.key, tag.value))

# set bucket cors
def SetBucketCors():
    cors1 = CorsRule(id='101', allowedMethod=['PUT', 'POST', 'GET', 'DELETE'],
                     allowedOrigin=['www.xxx.com', 'www.x.com'], allowedHeader=['header-1', 'header-2'],
                     maxAgeSecond=100, exposeHeader=['head1'])
    cors2 = CorsRule(id='102', allowedMethod=['PUT', 'POST', 'GET', 'DELETE'],
                     allowedOrigin=['www.xxx.com', 'www.x.com'], allowedHeader=['header-1', 'header-2'],
                     maxAgeSecond=100, exposeHeader=['head1'])

    corsList = [cors1, cors2]

    resp = TestObs.setBucketCors('bucket001', corsList)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket cors
def GetBucketCors():
    resp = TestObs.getBucketCors('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        index = 1
        for rule in resp.body:
            print('corsRule [' + str(index) + ']')
            print('id:', rule.id)
            print('allowedMethod', rule.allowedMethod)
            print('allowedOrigin', rule.allowedOrigin)
            print('allowedHeader', rule.allowedHeader)
            print('maxAgeSecond', rule.maxAgeSecond)
            print('exposeHeader', rule.exposeHeader)
            index += 1

# delete bucket cors
def DeleteBucketCors():
    resp = TestObs.deleteBucketCors('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# options bucket
def OptionsBucket():
    option = Options(origin='www.example.com', accessControlRequestMethods=['GET', 'POST'],
                     accessControlRequestHeaders=['header1', 'header2'])
    resp = TestObs.optionsBucket('bucket001', option)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        print('accessContorlAllowOrigin:', resp.body.accessContorlAllowOrigin)
        print('accessContorlMaxAge:', resp.body.accessContorlMaxAge)    
        print('accessContorlExposeHeaders:', resp.body.accessContorlExposeHeaders)   
        print('accessContorlAllowMethods:', resp.body.accessContorlAllowMethods)
        print('accessContorlAllowHeaders:', resp.body.accessContorlAllowHeaders)

# options object
def OptionsObject():
    option = Options(origin='www.example.com', accessControlRequestMethods=['PUT'])
    resp = TestObs.optionsObject('bucket001', 'test.txt', option)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        print('accessContorlAllowOrigin:', resp.body.accessContorlAllowOrigin)
        print('accessContorlMaxAge:', resp.body.accessContorlMaxAge)    
        print('accessContorlExposeHeaders:', resp.body.accessContorlExposeHeaders)   
        print('accessContorlAllowMethods:', resp.body.accessContorlAllowMethods)
        print('accessContorlAllowHeaders:', resp.body.accessContorlAllowHeaders)

# set bucket notification
def SetBucketNotification():
    fr1 = FilterRule(name='prefix', value='smn')
    fr2 = FilterRule(name='suffix', value='.jpg')
    topicConfiguration = TopicConfiguration(id='001', topic='urn:smn:region3:35667523534:topic1', events=['s3:ObjectCreated:*'], filterRules=[fr1, fr2])
    resp = TestObs.setBucketNotification('bucket001', Notification(topicConfigurations=[topicConfiguration]))
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get bucket notification
def GetBucketNotification():
    resp = TestObs.getBucketNotification('bucket001')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body is not None:
        for topicConfiguration in resp.body.topicConfigurations:
            print('id:', topicConfiguration.id)
            print('topic:', topicConfiguration.topic)
            print('events:', topicConfiguration.events)
            index = 1
            for rule in topicConfiguration.filterRules:
                print('rule [' + str(index) + ']')
                print('name:', rule.name)
                print('value:', rule.value)

# list multipart uploads
def ListMultipartUploads():
    Lmultipart = ListMultipartUploadsRequest(delimiter=None, prefix=None, max_uploads=10, key_marker=None,
                                             upload_id_marker=None)
    resp = TestObs.listMultipartUploads(bucketName='bucket001', multipart=Lmultipart)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('bucket:', resp.body.bucket, ',keyMarker：', resp.body.keyMarker, 'uploadIdMarker:', resp.body.uploadIdMarker, ',nextKeyMarker：', resp.body.nextKeyMarker, 'delimiter:', resp.body.delimiter)
        print('nextUploadIdMarker:', resp.body.nextUploadIdMarker, ',maxUploads：', resp.body.maxUploads, 'isTruncated:', resp.body.isTruncated, ',prefix：', resp.body.prefix)
        if resp.body.upload:
            i = 0
            for upload in resp.body.upload:
                print('upload[', i, ']:')
                i += 1
                print('key:', upload.key, ',uploadId:', upload.uploadId, ',storageClass:', upload.storageClass, ',initiated:', upload.initiated)
                if upload.owner:
                    print('owner.owner_id:', upload.owner.owner_id, ',owner.owner_name:', upload.owner.owner_name)
                if upload.initiator:
                    print('initiator.id:', upload.initiator.id, 'initiator.name:', upload.initiator.name)
        if resp.body.commonPrefixs:
            i = 0
            for commonPrefix in resp.body.commonPrefixs:
                print('commonPrefix[', i, ']:')
                i += 1
                print('prefix:', commonPrefix.prefix)

# set object acl
def SetObjectAcl():
    Lowner = Owner(owner_id='ownerid', owner_name='ownername')

    Lgrantee = Grantee(grantee_id='userid', grantee_name='username', group=None)

    Lgrant = Grant(grantee=Lgrantee, permission=Permission.READ)

    Lgrants = [Lgrant]

    Lacl = ACL(owner=Lowner, grants=Lgrants)

    resp = TestObs.setObjectAcl(bucketName='bucket001', objectKey='test.txt', acl=None, versionId=None,
                                aclControl=HeadPermission.PUBLIC_READ_WRITE)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get object acl
def GetObjectAcl():
    resp = TestObs.getObjectAcl(bucketName='bucket001', objectKey='test.txt', versionId=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('owner_id:', resp.body.owner.owner_id, ',owner_name:', resp.body.owner.owner_name)
        i = 0
        for grant in resp.body.grants:
            print('Grant[', i, ']:')
            i += 1
            print('permission:', grant.permission)
            print('grantee_name:', grant.grantee.grantee_name, ',grantee_id:', grant.grantee.grantee_id, ',grantee.group:', grant.grantee.group)

# delete object
def DeleteObject():
    resp = TestObs.deleteObject(bucketName='bucket001', objectKey='test.txt', versionId=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# delete objects
def DeleteObjects():
    Lobject1 = Object(key='test.xml', versionId=None)
    Lobject2 = Object(key='test.txt', versionId=None)
    Lobject3 = Object(key='test', versionId=None)
    Lobjects = [Lobject1, Lobject2, Lobject3]

    Lreq = DeleteObjectsRequest(quiet=False, objects=Lobjects)

    resp = TestObs.deleteObjects(bucketName='bucket001', deleteObjectsRequest=Lreq)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        if resp.body.deleted:
            i = 0
            for delete in resp.body.deleted:
                print('deleted[', i, ']:')
                i += 1
                print('key:', delete.key, ',deleteMarker:', delete.deleteMarker, ',deleteMarkerVersionId:', delete.deleteMarkerVersionId)
        if resp.body.error:
            i = 0
            for err in resp.body.error:
                print('error[', i, ']:')
                print('key:', err.key, ',code:', err.code, ',message:', err.message)

# abort multipart uplod
def AbortMultipartUpload():
    resp = TestObs.abortMultipartUpload(bucketName='bucket001', objectKey='test.zip', uploadId='uploadid')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# initiate multipart upload
def InitiateMultipartUpload():
    resp = TestObs.initiateMultipartUpload(bucketName='bucket001', objectKey='test.zip', websiteRedirectLocation=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('bucketName:', resp.body.bucketName, ',objectKey:', resp.body.objectKey, ',uploadId:', resp.body.uploadId)

# complete multipart upload
def CompleteMultipartUpload():
    Lpart1 = CompletePart(partNum=1, etag='etagvalue1')
    Lpart2 = CompletePart(partNum=2, etag='etagvalue2')
    Lparts = []
    Lparts.append(Lpart1)
    Lparts.append(Lpart2)


    LcompleteMultipartUploadRequest = CompleteMultipartUploadRequest(parts=Lparts)

    resp = TestObs.completeMultipartUpload(bucketName='bucket001', objectKey='test.zip', uploadId='uploadid',
                                           completeMultipartUploadRequest=LcompleteMultipartUploadRequest)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('location:', resp.body.location, ',bucket:', resp.body.bucket, ',key:', resp.body.key, ',etag:', resp.body.etag)

# upload part
def UploadPart():
    resp = TestObs.uploadPart(bucketName='bucket001', objectKey='test.zip', partNumber=1, uploadId='uploadid',
                              object='/temp/bigfile.zip', isFile=True, partSize=100 * 1024 * 1024, offset=0)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',header:', resp.header)

    etag1 = dict(resp.header).get('etag')
    print(etag1)

    resp = TestObs.uploadPart(bucketName='bucket001', objectKey='test.zip', partNumber=2, uploadId='uploadid',
                              object='/temp/bigfile.zip', isFile=True, partSize=200 * 1024 * 1024,
                              offset=100 * 1024 * 1024)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',header:', resp.header)

    etag2 = dict(resp.header).get('etag')
    print(etag2)

# copy part
def CopyPart():
    resp = TestObs.copyPart(bucketName='bucket001', objectKey='test.txt', partNumber=1, uploadId='uploadid',
                            copySource='bucket002/test.txt')
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('lastModified:', resp.body.lastModified, ',etag:', resp.body.etag)

# list parts
def ListParts():
    resp = TestObs.listParts(bucketName='bucket001', objectKey='test.zip', uploadId='uploadid', maxParts=None,
                             partNumberMarker=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('bucketName:', resp.body.bucketName, ',objectKey:', resp.body.objectKey, ',uploadId:', resp.body.uploadId, ',storageClass:', resp.body.storageClass,)
        print('partNumbermarker:', resp.body.partNumbermarker, ',nextPartNumberMarker:', resp.body.nextPartNumberMarker, ',maxParts:', resp.body.maxParts, ',isTruncated:', resp.body.isTruncated,)
        if resp.body.initiator:
            print('initiator.name:', resp.body.initiator.name, ',initiator.id:', resp.body.initiator.id)
        if resp.body.parts:
            i = 0
            for part in resp.body.parts:
                print('part[', i, ']:')
                i += 1
                print('partNumber:', part.partNumber, ',lastModified:', part.lastModified, ',etag:', part.etag, ',size:', part.size)

# restore object
def RestoreObject():
    resp = TestObs.restoreObject(bucketName='bucket001', objectKey='test.txt', days=1, versionId=None, tier=TierType.EXPEDITED)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# get object metadata
def GetObjectMetadata():
    resp = TestObs.getObjectMetadata(bucketName='bucket001', objectKey='test.txt', versionId=None)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    print('etag:', resp.body.etag)
    print('lastModified:', resp.body.lastModified)
    print('contentType:', resp.body.contentType)
    print('contentLength:', resp.body.contentLength)

# put content
def PutContent():
    sseHeader = SseKmsHeader.getInstance() 
    Lheaders = PutObjectHeader(md5=None, acl='private', location=None, contentType='text/plain', sseHeader=sseHeader)

    Lmetadata = {'key': 'value'}

    resp = TestObs.putContent(bucketName='bucket001', objectKey='test.txt', content='msg content to put',
                             metadata=Lmetadata, headers=Lheaders)

    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    print(resp.header)

# put file
def PutFile():
    Lheaders = PutObjectHeader(md5=None, acl='private', location=None, contentType='text/plain')

    Lheaders.sseHeader = SseKmsHeader.getInstance()

    Lmetadata = {'key': 'value'}
    file_path = '/temp/test.txt'

    resp = TestObs.putFile(bucketName='bucket001', objectKey='test.txt', file_path=file_path,
                              metadata=Lmetadata, headers=Lheaders)
    if isinstance(resp, list):
        for k, v in resp:
            print('objectKey', k, 'common msg:status:', v.status, ',errorCode:', v.errorCode, ',errorMessage:', v.errorMessage)
    else:
        print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)

# copy object
def CopyObject():
    Lheader = CopyObjectHeader(acl=None, directive=None, if_match=None, if_none_match=None,
                               if_modified_since=DateTime(2017,6,6), if_unmodified_since=None,
                               location=None)
    Lmetadata = {'key': 'value'}
    resp = TestObs.copyObject(sourceBucketName='bucket002', sourceObjectKey='test.txt', destBucketName='bucket001',
                              destObjectKey='test.txt', metadata=Lmetadata, headers=Lheader)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage)
    if resp.body:
        print('lastModified:', resp.body.lastModified, ',etag:', resp.body.etag)

# get object
def GetObject():
    LobjectRequest = GetObjectRequest(content_type='text/plain', content_language=None, expires=None,
                                      cache_control=None, content_disposition=None, content_encoding=None,
                                      versionId=None)

    Lheaders = GetObjectHeader(range='0-10', if_modified_since=None, if_unmodified_since=None, if_match=None,
                               if_none_match=None)
    loadStreamInMemory = False
    resp = TestObs.getObject(bucketName='bucket001', objectKey='test.txt', downloadPath='/temp/test',
                             getObjectRequest=LobjectRequest, headers=Lheaders, loadStreamInMemory=loadStreamInMemory)
    print('common msg:status:', resp.status, ',errorCode:', resp.errorCode, ',errorMessage:', resp.errorMessage, ',header:', resp.header)
    if loadStreamInMemory:
        print(resp.body.buffer)
        print(resp.body.size)
    elif resp.body.response:
        response = resp.body.response
        chunk_size = 65536
        if response is not None:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                print(chunk)
            response.close()
    else:
        print(resp.body.url)

if __name__ == '__main__':
    # initLog()
    #=========================================================
    # bucket operations
    # =========================================================
    # CreateBucket()
    # DeleteBucket()
    # ListBuckets()
    # HeadBucket()
    # GetBucketMetadata()
    # SetBucketQuota()
    # GetBucketQuota()
    # SetBucketStoragePolicy()
    # GetBucketStoragePolicy()
    # GetBucketStorageInfo()
    # SetBucketAcl()
    # GetBucketAcl()
    # SetBucketPolicy()
    # GetBucketPolicy()
    # DeleteBucketPolicy()
    # SetBucketVersioningConfiguration()
    # GetBucketVersioningConfiguration()
    # ListVersions()
    # ListObjects()
    # ListMultipartUploads()
    # DeleteBucketLifecycleConfiguration()
    # SetBucketLifecycleConfiguration()
    # GetBucketLifecycleConfiguration()
    # DeleteBucketWebsiteConfiguration()
    # SetBucketWebsiteConfiguration()
    # GetBucketWebsiteConfiguration()
    # SetBucketLoggingConfiguration()
    # GetBucketLoggingConfiguration()
    # GetBucketLocation()
    # DeleteBucketTagging()
    # SetBucketTagging()
    # GetBucketTagging()
    # DeleteBucketCors()
    # SetBucketCors()
    # GetBucketCors()
    # OptionsBucket()
    # SetBucketNotification()
    # GetBucketNotification()
    #=========================================================
    # object operations
    # =========================================================
    # OptionsObject()
    # SetObjectAcl()
    # GetObjectAcl()
    # DeleteObject()
    # DeleteObjects()
    # RestoreObject()
    # AbortMultipartUpload()
    # InitiateMultipartUpload()
    # UploadPart()
    # CompleteMultipartUpload()
    # CopyPart()
    # ListParts()
    # GetObjectMetadata()
    # PutContent()
    # CopyObject()
    # PutFile()
    # GetObject()
    pass
