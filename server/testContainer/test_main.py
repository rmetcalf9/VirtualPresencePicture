#Script to test a running container
import unittest
import requests
import os

baseURL="http://virtualpresencepicture:8098"

class test_containerAPI(unittest.TestCase):
#Actual tests below

  def test_WeCanGetToSwaggerFile(self):
    result = requests.get(baseURL + "/api/swagger.json")
    self.assertEqual(result.status_code, 200)

  def test_ContainerVersionMatchesEnviromentVariable(self):
    self.assertTrue('EXPECTED_CONTAINER_VERSION' in os.environ)
    result = requests.get(baseURL + "/api/serverinfo/")
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON['Server']['Version'], os.environ['EXPECTED_CONTAINER_VERSION'])

