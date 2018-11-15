#appObj.py - This file contains the main application object
# to be constructed by app.py

#All times will be passed to callers in UTC
# it is up to the callers to convert into any desired user timezone

import pytz

from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass as parAppObj, readFromEnviroment
from flask_restplus import fields
import time
import datetime

class appObjClass(parAppObj):
  curDateTimeOverrideForTesting = None
  serverStartTime = None

  def init(self, env, serverStartTime, testingMode = False):
    self.curDateTimeOverrideForTesting = None
    self.serverStartTime = serverStartTime
    super(appObjClass, self).init(env)

  def initOnce(self):
    super(appObjClass, self).initOnce()

  def setTestingDateTime(self, val):
    self.curDateTimeOverrideForTesting = val
  def getCurDateTime(self):
    if self.curDateTimeOverrideForTesting is None:
      return datetime.datetime.now(pytz.timezone("UTC"))
    return self.curDateTimeOverrideForTesting


appObj = appObjClass()