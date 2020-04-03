#!/usr/bin/python  
# -*- coding:utf-8 -*- 

'''
 This sample demonstrates how to do common operations in v4 temporary signature way
 on OBS using the OBS SDK for Python.
'''

AK = '*** Provide your Access Key ***'
SK = '*** Provide your Secret Key ***'
server = 'yourdomainname'
bucketName = 'my-obs-bucket-demo'
objectKey = 'my-obs-object-key-demo'

import sys, ssl
IS_PYTHON2 = sys.version_info.major == 2 or sys.version < '3'

if IS_PYTHON2:
    from urlparse import urlparse
    import httplib
else:
    import http.client as httplib
    from urllib.parse import urlparse


from com.obs.client.obs_client import ObsClient
# Constructs a obs client instance with your account for accessing OBS
obsClient = ObsClient(access_key_id=AK, secret_access_key=SK, server=server, is_secure=False)

def doAction(msg, method, res, content=None):
    print(msg + ' using v4 temporary signature url:')
    url = res['signedUrl']
    print('\t' + url)

    url = urlparse(url)

    conn = httplib.HTTPConnection(url.hostname, url.port)
    path = url.path + '?' + url.query
    conn.request(method, path, headers=res['actualSignedRequestHeaders'])

    if content is not None:
        content = content if IS_PYTHON2 else content.encode('UTF-8')
        conn.send(content)

    result = conn.getresponse()
    status = result.status
    responseContent = result.read()
    if status < 300:
        print(msg + ' using v4 temporary signature url successfully.')
    else:
        print(msg + ' using v4 temporary signature url failed!!')

    if responseContent:
        print('\tresponseContent:')
        print('\t%s' % responseContent)
    conn.close()
    print('\n')

# Create bucket
method = 'PUT'
res = obsClient.createV4SignedUrl(method, bucketName, expires=3600)
doAction('Creating bucket', method, res)

# Set/Get/Delete bucket cors
method = 'PUT'
from com.obs.models.cors_rule import CorsRule
from com.obs.utils import convert_util, common_util
cors1 = CorsRule(id='rule1', allowedMethod=['PUT', 'HEAD', 'GET'],
                 allowedOrigin=['http://www.a.com', 'http://www.b.com'], allowedHeader=['Authorization1'],
                 maxAgeSecond=100, exposeHeader=['x-obs-test1'])
cors2 = CorsRule(id='rule2', allowedMethod=['PUT', 'HEAD', 'GET'],
                 allowedOrigin=['http://www.c.com', 'http://www.d.com'], allowedHeader=['Authorization2'],
                 maxAgeSecond=200, exposeHeader=['x-obs-test2'])
corsList = [cors1, cors2]

content = convert_util.transCorsRuleToXml(corsList)
headers = {'Content-Type': 'application/xml', 'Content-Length': str(len(content)), 'Content-MD5': common_util.base64_encode(common_util.md5_encode(content))}
res = obsClient.createV4SignedUrl(method, bucketName, specialParam='cors', headers=headers)
doAction('Setting bucket cors', method, res, content)

method = 'GET'
res = obsClient.createV4SignedUrl(method, bucketName, specialParam='cors')
doAction('Getting bucket cors', method, res)

method = 'DELETE'
res = obsClient.createV4SignedUrl(method, bucketName, specialParam='cors')
doAction('Deleting bucket cors', method, res)

# Put object
method = 'PUT'
content = 'Hello OBS'
headers = {'Content-Length' : str(len(content))}
res = obsClient.createV4SignedUrl(method, bucketName, objectKey, headers=headers)
doAction('Creating object', method, res, content)

# Get object
method = 'GET'
res = obsClient.createV4SignedUrl(method, bucketName, objectKey)
doAction('Getting object', method, res)

# Set/Get object acl
method = 'PUT'
headers = {'x-amz-acl': 'public-read'}
res = obsClient.createV4SignedUrl(method, bucketName, objectKey, specialParam='acl', headers=headers)
doAction('Setting object acl', method, res)

method = 'GET'
res = obsClient.createV4SignedUrl(method, bucketName, objectKey, specialParam='acl')
doAction('Getting object acl', method, res)

# Delete object
method = 'DELETE'
res = obsClient.createV4SignedUrl(method, bucketName, objectKey)
doAction('Deleting object', method, res)

# Delete bucket
method = 'DELETE'
res = obsClient.createV4SignedUrl(method, bucketName, expires=3600)
doAction('Deleting bucket', method, res)
