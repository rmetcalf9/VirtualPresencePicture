from flask import request
from flask_restplus import Resource, fields
import datetime
import pytz
from baseapp_for_restapi_backend_with_swagger import readFromEnviroment

def getAPIModel(appObj):
  pictureModel = appObj.flastRestPlusAPIObject.model('pictureAPI', {
    'Identifier': fields.String(default='DEFAULT', description='Unique identifier for this picture'),
    'Expires': fields.DateTime(dt_format=u'iso8601', description='Date this record will be discarded'),
    'Contents': fields.Raw(default=None, descrition='Data saved in this record')
  })
  serverInfoServerModel = appObj.flastRestPlusAPIObject.model('mainAPI', {
    'Version': fields.String(default='DEFAULT', description='Version of container running on server')
  })
  return appObj.flastRestPlusAPIObject.model('ServerInfo', {
    'Server': fields.Nested(serverInfoServerModel),
    'Pictures': fields.List(fields.Nested(pictureModel))
  })  

class PictureClass:
  pictures = dict();
  appObj = None
  validityDuration = datetime.timedelta(minutes=30)
  def resetData(self, appObj):
    self.appObj = appObj
    self.pictures = dict();
  def getJSON(self):
    return { 
      'Server': { 'Version': self.appObj.version },
      'Pictures': list(map(lambda x: x[1], self.pictures.items()))
     }
  def addPicture(self, identifier, content):
    self.pictures[identifier] = {
      'Identifier': identifier,
      'Expires': self.appObj.getCurDateTime() + self.validityDuration,
      'Contents': content
    }
    return

pictureClass = PictureClass()

def resetData(appObj):
  pictureClass.resetData(appObj)
  
def registerAPI(appObj):
  pictureClass.resetData(appObj)

  nsServerinfo = appObj.flastRestPlusAPIObject.namespace('serverinfo', description='General Server Operations')
  @nsServerinfo.route('/')
  class servceInfo(Resource):
  
    '''General Server Operations XXXXX'''
    @nsServerinfo.doc('getserverinfo')
    @nsServerinfo.marshal_with(getAPIModel(appObj))
    @nsServerinfo.response(200, 'Success')
    def get(self):
     '''Get general information about the dockjob server'''
     curDatetime = datetime.datetime.now(pytz.utc)
     return pictureClass.getJSON()
    
  @nsServerinfo.route('/<string:identifier>')
  @nsServerinfo.param('identifier', 'Picture identifier')
  class pictureInfo(Resource):
  
    @nsServerinfo.doc('postPicture')
    #@nsServerinfo.expect(jobCreationModel, validate=True)
    @appObj.flastRestPlusAPIObject.response(400, 'Validation error')
    @appObj.flastRestPlusAPIObject.response(201, 'Created')
    @appObj.flastRestPlusAPIObject.marshal_with(getAPIModel(appObj), code=201, description='Picture data stored')
    def post(self, identifier):
      '''Create Picture'''
      content = request.get_json()
      pictureClass.addPicture(identifier, content)
      return pictureClass.getJSON(), 201