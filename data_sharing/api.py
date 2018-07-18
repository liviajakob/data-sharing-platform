'''
API for accessing the data of the IceExplorer

@author: livia
'''
from display_data.database import Database
from flask import Flask, jsonify, request, send_file, Response
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from display_data.system_configuration import ConfigSystem
from get_data.query_point import retrieve_pixel_value
import os, glob, ast
from dicttoxml import dicttoxml

app = Flask(__name__)
CORS(app) #allow cross origin

#api = Api(app)


'''class Download(Resource):
    def download(self, filename):
        uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=uploads, filename=filename)

api.add_resource(HelloWorld, '/')
api.add_resource(HelloWorld, '/')'''


'''@app.route('/', methods=['GET'])
def index():
    ###
    dic = {}
    dic['hi']='Livia'
    base='/Users/livia/msc_dissertation/CODE/data_sharing/data/output'
    attachment_filename='hi5.tif'
    #return jsonify(dic)
    response = send_file('/Users/livia/msc_dissertation/CODE/data_sharing/data/input/Greenland_1000_error.tif')
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    
    return response'''

# TODO: more flexible
@app.route('/v1/file', methods=['GET'])
def file():
    pid=request.args.get('layer_id')
    date = request.args.get('date')
    rasterf=getLayerRawfileFilePath(pid, date)
    #raster = '/Users/livia/msc_dissertation/CODE/data_sharing/data/output/datasets/'+str(pid)+'/dem/raw_input.tif'
    response = send_file(rasterf)
    return response

@app.route('/v1/values', methods=['GET'])
def values():
    '''Returns date and value pairs of the time layers of a given layer and x and y coordinates
    
    Input parameter -
        layer_id - the id of the queried layer
        x - x-Coordinate
        y - y-Coordinate
    
    
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
    # TODO: Error handling
    
    lid=request.args.get('layer_id')
    fnames=getLayerProjectedFilePaths(lid)
    x = request.args.get('x')
    y = request.args.get('y')
    coords=[float(x),float(y)]
    pixelvalues=[]
    for fname in fnames:
        val=retrieve_pixel_value(coords, fname)
        try:
            val = round(val,4) #"{:.6f}".format(val)
            pass
        except:
            pass
        date = os.path.basename(os.path.dirname(fname)) #folder name
        pixelvalues.append({'y': val, 'x': date})
    
    response={}
    response['data']=pixelvalues
    return jsonify(response)


# TODO: Error handling 
@app.route('/v1/datasets', methods=['GET'])
def datasets():
    '''Returns a JSON of the datasets, including filteroptions'''
    database = Database()
    database.scopedSession()
    
    protocol = 'json'
    if 'protocol' in request.args:
        protocol = request.args.get('protocol')
            
    print(request.args)
    
    datasets=database.getDatasets(request.args.to_dict(), dic=True, orderbyarea=False, layerinfo=True)
    database.closeSession()
    
    if protocol.lower() == 'json':
        return jsonify(datasets) #jsonify is flask function, so header is set automatically
    elif protocol.lower() == 'xml':
        xml=dicttoxml(datasets)
        return Response(xml, mimetype='text/xml')
    else:
        return protocol +' is not a valid protocol type'


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404




###### Helper Methods

 
def getLayerRawfileFilePath(layer_id, date):
    '''Returns one raw file (unprojected) path
    
    Input Parameter:
        layer_id - ID of the layer
        date - date of the time layer
    
    '''
    database = Database()
    database.scopedSession()
    layer = database.getLayerGroups({'id': layer_id})[0]
    #ltype=database.getLayertypeById(layer.layertype).name
    conf = ConfigSystem()
    file = conf.getLayerRawFile( ltype=layer.layertype, d_id=layer.dataset_id, date=date)
    
    database.closeSession()
    return file
     
  

def getLayerProjectedFilePaths(layer_id):
    '''Returns reprojected raw file path of all the time series files of a layer
    
    Input Parameter:
        layer_id - ID of the layer
    '''
    database = Database()
    database.scopedSession()
    layer = database.getLayerGroups({'id': layer_id})[0]
    #ltype=database.getLayertypeById(layer.layertype).name
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
    

    
if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5002)