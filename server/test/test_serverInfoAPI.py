from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json
from appObj import appObj
import pytz
import datetime

serverInfoWithoutAnyPictures = {
      'Server': {
        'Version': env['APIAPP_VERSION']
      },
      'Pictures': []
}
samplePictureIdentifier = 'ABC123'
samplePictureContent = { 'SomeContent': 'abc' }

serverInfoWithSamplePictureContent = {
      'Server': {
        'Version': env['APIAPP_VERSION']
      },
      'Pictures': [{
        'Identifier': samplePictureIdentifier,
        'Expires': "2018-11-22T14:16:00+00:00",
        'Contents': samplePictureContent
      }]
}

class test_api(testHelperAPIClient):

  def test_getServerInfo(self):
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, serverInfoWithoutAnyPictures)

  def test_swaggerJSONProperlyShared(self):
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200)
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200)

  def test_getAddPicture(self):
    appObj.setTestingDateTime(pytz.timezone('Europe/London').localize(datetime.datetime(2018,11,22,13,46,0,0)))
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, serverInfoWithoutAnyPictures)

    result = self.testClient.post('/api/serverinfo/' + samplePictureIdentifier, json=samplePictureContent)
    self.assertEqual(result.status_code, 201)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, serverInfoWithSamplePictureContent)
    
  def test_getAddedPictureExpires(self):
    self.test_getAddPicture()
    appObj.setTestingDateTime(pytz.timezone('Europe/London').localize(datetime.datetime(2018,11,22,14,36,0,0)))
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, serverInfoWithoutAnyPictures)
