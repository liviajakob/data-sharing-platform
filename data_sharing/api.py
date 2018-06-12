'''
Created on 2 Jun 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request, send_file, send_from_directory, make_response
import json
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from display_data.system_configuration import ConfigSystem
from get_data.query_point import retrieve_pixel_value

app = Flask(__name__)
CORS(app)

#api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


'''class Download(Resource):
    def download(self, filename):
        uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=uploads, filename=filename)

api.add_resource(HelloWorld, '/')
api.add_resource(HelloWorld, '/')'''


@app.route('/', methods=['GET'])
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
    
    return response


@app.route('/get_file/<int:pid>', methods=['GET'])
def get_file(pid):
    rasterf=getLayerFilePath(pid)
    #raster = '/Users/livia/msc_dissertation/CODE/data_sharing/data/output/datasets/'+str(pid)+'/dem/raw_input.tif'
    response = send_file(rasterf)
    return response

@app.route('/get_value/<int:lid>', methods=['GET', 'OPTIONS'])
def get_value(lid):
    print('we are here')
    print(lid)
    fname=getLayerFilePath(lid)
    #raster = '/Users/livia/msc_dissertation/CODE/data_sharing/data/output/datasets/'+str(pid)+'/dem/raw_input.tif'
    #response = send_file(rasterf)
    x = request.args.get('x')
    y = request.args.get('y')
    print(x,y)
    coords=[float(x),float(y)]
    #-102834.5, -2151176.688
    print(coords)
    print(fname)
    val=retrieve_pixel_value(coords, fname)
    try:
        val = "{:.6f}".format(val)
    except:
        pass
    response={}
    response['value']=val
    return jsonify(response)
  

def getLayerFilePath(pid):
    database = Database()
    database.scopedSession()
    layer = database.getLayerById(pid)[0]
    ltype=database.getLayertypeById(layer.layertype_id).name
    conf = ConfigSystem()
    rasterf = conf.getLayerRawFile(ltype=ltype, d_id=layer.dataset_id)
    database.closeSession()
    return rasterf
    

    
if __name__ == '__main__':
    app.run(debug=True, threaded=True)