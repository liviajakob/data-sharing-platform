'''
External RESTful API for accessing the data of the IceExplorer
File: api.py

API Endpoints:
    file
    datasets
    getvalues
    
Classes:
    APIRequestException - API Exception class

@author: livia
'''
from display_data.database import Database
from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS
from display_data.system_configuration import ConfigSystem
from get_data.query_point import retrieve_pixel_value
import os, glob
from dicttoxml import dicttoxml
from datetime import datetime


app = Flask(__name__)
CORS(app) #allow cross origin


@app.route('/v1/file', methods=['GET'])
def file():
    '''file API endpoint:
    
    URL Input Parameter:
        layergroup_id (int) - (required) Layer group id
        date - (required) Date of the layer in the following format: 'YYYY-MM-DD' (e.g. 2013-11-21)
    
    Endpoint URL: 
    root/v1/file
    
    Example URL:
    root/v1/file?layergroup_id=1&date=2017-06-26
    
    Response type:
        the requested file, e.g. a TIFF file
    
    '''
    ## layergroup_id
    try:
        pid=request.args.get('layergroup_id')
        pid = int(pid)
    except TypeError:
        raise APIRequestException('Missing Arguments: <layergroup_id> is missing', status_code=419)
    except ValueError:
        raise APIRequestException('Invalid Arguments: <layergroup_id> must be an integer', status_code=420)
    ## date
    try:
        date=request.args.get('date')
        datetime.strptime(date, "%Y-%m-%d")
    except TypeError:
        raise APIRequestException('Missing Arguments: <date> is missing', status_code=419)
    except ValueError:
        raise APIRequestException('Invalid Arguments: <date> is in the wrong format, should be YYY-MM-DD', status_code=420)
    # get the file path
    rasterf=getLayerRawfileFilePath(pid, date)
    try:
        response = send_file(rasterf)
    except FileNotFoundError:
        raise APIRequestException('Not Found: Requested file could not be found, check if the input parameters match', status_code=404)
    return response


@app.route('/v1/values', methods=['GET'])
def values():
    '''Returns date and value pairs of the time layers of a given layer and x and y coordinates
    
    URL Input parameter:
        layergroup_id (int) - the id of the queried layer
        x (str/float) - x-Coordinate
        y (str/float) - y-Coordinate
    
    
    Response type: JSON
        containes an array with x and y value pairs of dates and values
    
    Example Response:
    
    {data: [{
            x: 2012-07-27,
            y: 20
        }, {
            x: 2013-07-27,
            y: 10
        }]
    }
    
    '''  
    try:
        lid=request.args.get('layergroup_id')
        lid = int(lid)
    except TypeError:
        raise APIRequestException('Missing Arguments: <layergroup_id> is missing', status_code=419)
    except ValueError:
        raise APIRequestException('Invalid Arguments: <layergroup_id> must be an integer', status_code=420)

    fnames=getLayerProjectedFilePaths(lid)
    
    #coordinates
    x = request.args.get('x')
    y = request.args.get('y')
    try:
        coords=[float(x),float(y)]
    except TypeError:
        raise APIRequestException('Missing Arguments: coordinates are missing', status_code=419)
    except ValueError:
        raise APIRequestException('Invalid Arguments: coordinates are in the wrong format, float is expected', status_code=420)    
    
    pixelvalues=[]
    for fname in fnames:
        val=retrieve_pixel_value(coords, fname)
        try:
            val = round(val,4)
        except:
            raise APIRequestException('Internal Server Error: unexpected internal server error', status_code=500) 
        date = os.path.basename(os.path.dirname(fname)) #folder name
        pixelvalues.append({'y': val, 'x': date})
    
    response={}
    response['data']=pixelvalues
    return jsonify(response)



@app.route('/v1/datasets', methods=['GET'])
def datasets():
    '''Returns dataset information, including filteroptions
    
    URL Input Paramters:
        layertype (str) - (optional) Type of data. Use one of the following: dem, error, velocity, rate
        startdate (str) - (optional) Filters only datasets with layers starting before this date. Format: 'YYYY-MM-DD' (e.g. 2013-11-21)
        enddate (str) - (optional)     Filters only datasets with layers ending after this date. Format: 'YYYY-MM-DD' (e.g. 2013-11-21)
        id (int) - (optional) Dataset id. Only returns the dataset with the specified id
        page (int) - (optional), (default: 1) Page number. The default page size is 100 datasets
        response (str) - (optional), (default: json) Response type. Use one of the following: json, xml
    
    Endpoint URL: 
    root/v1/datasets
    
    Example URL:
    root/v1/datasets?layertype=dem&startdate=2011-09-21
    
    Response type:
        the data in requested protocol type 
    
    '''
    database = Database()
    database.scopedSession()
    
    # pagination
    page=0
    page_size=100
    if 'page' in request.args:
        try:
            page=int(request.args.get('page'))-1
        except ValueError:
            raise APIRequestException('Invalid Arguments: <page> must be an integer', status_code=420)
    
    try:
        datasets=database.getDatasets(request.args.to_dict(), dic=True, page=page, page_size=page_size, orderbyarea=False, layerinfo=True)
    except ValueError:
        raise APIRequestException('Invalid Arguments: one or multiple input parameters are invalid, refer to the documentation', status_code=420)
    
    database.closeSession()
    
    # protocol types
    protocol = 'json'
    if 'protocol' in request.args:
        protocol = request.args.get('protocol')
    if protocol.lower() == 'json':
        return jsonify(datasets) #jsonify is a flask function, so header is set automatically
    elif protocol.lower() == 'xml':
        xml=dicttoxml(datasets)
        return Response(xml, mimetype='text/xml')
    else:
        raise APIRequestException('Invalid Arguments: <<'+ protocol +'>> is not a valid <protocol> type', status_code=420)



    
## Error Handling

class APIRequestException(Exception):
    '''Exception class for API Exceptions
    
    Inherits from Exceptions    
    
    '''
    
    # default status code is 400
    status_code = 400

    def __init__(self, message, status_code=None):
        '''
        Input Parameters:
            message (str) - Error message
            status_code (int) - (optional) status code of the occurred error
        
        '''
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        '''Converts the error message to a dictionnary
        
        Returns:
            dict - a dictionnary of the Error
        '''
        rv = {}
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


@app.errorhandler(APIRequestException)
def handle_apiRequestException(error):
    '''Flask error handler to handle the APIRequestException
    
    Response:
        a JSON with information about the occurred Error
    '''
    response = error.to_dict()
    response = jsonify(response)
    return response


###### Helper Methods

 
def getLayerRawfileFilePath(layergroup_id, date):
    '''Returns one raw file (unprojected) path
    
    Input Parameter:
        layergroup_id - ID of the layer group
        date - date of the layer
    
    '''
    database = Database()
    database.scopedSession()
    try:
        layer = database.getLayerGroups({'id': layergroup_id})[0]
    except IndexError:
        raise APIRequestException('Not Found: Requested layergroup does not exist', status_code=404)
    conf = ConfigSystem()
    file = conf.getLayerRawFile( ltype=layer.layertype, d_id=layer.dataset_id, date=date)
    database.closeSession()
    return file
     
  

def getLayerProjectedFilePaths(layergroup_id):
    '''Returns reprojected raw file path of all the time series files of a layer
    
    Input Parameter:
        layergroup_id - ID of the layer group
    '''
    database = Database()
    database.scopedSession()
    try:
        layer = database.getLayerGroups({'id': layergroup_id})[0]
    except IndexError:
        raise APIRequestException('Not Found: Requested layergroup does not exist', status_code=404)
    
    conf = ConfigSystem()
    files = conf.getLayerFolders(layer)
    database.closeSession()
    raw = conf.getReprojectedFilename()
    for i, f in enumerate(files): ## add the raw file to the path
        f = os.path.join(f,raw)
        for file in glob.glob(f+'.*'): #get files with any extension
            f=file
            break
        files[i] = f   
    return files



###

    
if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5002)
