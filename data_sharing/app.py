'''
Created on 25 Apr 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request, send_from_directory
import json, os
from flask_cors import CORS
from display_data.system_configuration import ConfigSystem
import ast

app = Flask(__name__)
#CORS(app)
    
@app.route('/', methods=['POST', 'GET'])
def index():
    try: 
        database = Database()
        database.scopedSession()
        query = database.getDatasets()[0]
        
        database.closeSession()
        
        return render_template('main.html', data=query.getBoundingBox(), error=False)
    except:
        return render_template('main.html', data=query.getBoundingBox(), error=True)
 
@app.route('/get_colours', methods=['POST', 'GET'])
def get_colours():
    layer_id = request.args.get('layer_id')
    database = Database()
    database.scopedSession()
    layer=database.getLayers({'id': layer_id})[0]
    database.closeSession()
    

    conf= ConfigSystem()
    pth = conf.getLayersColourfile(layer)
    file_o = open(pth, 'r')
    lines = file_o.readlines()
    rgbarr=[]
    vals=[]
    for line in lines:
        split=line.split()
        if split[0] != 'nan':
            rgb='rgb('+split[1]+', ' + split[2] + ', ' + split[3] + ')'
            rgbarr.append(rgb)
            vals.append(split[0])
    minmax = {'min': "{0:.1f}".format(float(vals[0])), 'max': "{0:.1f}".format(float(vals[-1]))}
    dic={'rgb': rgbarr, 'max': minmax['max'], 'min': minmax['min'], 'values': vals}

    return jsonify(dic)
 
 
 
@app.route('/datasets/<int:dataset_id>')
def datasets(dataset_id):
    '''Returns a JSON of the dataset'''
    database = Database()
    database.scopedSession()
    
    dataset=database.getDatasets(filters={'id': int(dataset_id)}, dic=True, timelayers=True)
    #geoDict=dataset.asGeoDict()
    #print(geoDict)
    #geoCollection = {}
    #geoCollection['type']= 'FeatureCollection'
    #geoCollection['features'] = [geoDict]
    print('DATSET', dataset)
    database.closeSession()
    return jsonify(dataset)

 
  
@app.route('/data')
def data():
    '''Returns a JSON of the datasets, including filteroptions'''
    database = Database()
    database.scopedSession()
    filters = {}
    print('requestargs', request.args)
    if 'filter' in request.args:
        try: 
            print('TRY TO CENVERT', request.args.get('filter'))
            filters = ast.literal_eval(request.args.get('filter'))
        except Exception as e:
            print('NOT POSSIBLE')
            print(e)
            pass
        
    print('FILTERRRR   ',filters, type(filters), 'ARGS: ', request.args.get('filter'), type(request.args.get('filter')), str(request.args.get('filter')))
    page=0
    page_size=5
    try:
        page=int(request.args.get('page'))-1
    except:
        pass
    
    if 'page_size' in request.args:
        try:
            page_size = int(request.args.get('page_size'))
        except:
            pass #wrong input, just default is used
    
    datasets=database.getDatasets(filters=filters, dic=True, page=page, page_size=page_size, orderbyarea=True)
    database.closeSession()

    return jsonify(datasets)

 
   
@app.route('/layertypes')
def layertypes():
    '''Returns a JSON of the datasets, including filteroptions'''
    #database = Database()
    #database.scopedSession()
    #layertypes=database.getLayerTypes(dic=True)    
    #database.closeSession()
    
    conf = ConfigSystem()
    layertypes = conf.getLayerTypes()
    dic = {'layertypes': layertypes} 

    return jsonify(dic)


"""@app.route('/tileurl/<int:layer_id>')
def tileurl(layer_id):
    database = Database()
    database.scopedSession()
    layer=database.getLayers({'id': layer_id})[0]    
    database.closeSession()
    
    conf = ConfigSystem()
    abs_path = conf.getTilesFolder(layer.layertype, layer.date, layer.dataset_id)
    prefix = conf.getDataOutputPath()
    rel_path = os.path.relpath(abs_path, prefix)
    return jsonify({'rel_url' : rel_path, 'abs_url' : abs_path})"""
    
    
'''@app.route('/download', methods=['GET', 'POST'])
def download():
    ''''''
    #database = Database()
    #database.scopedSession()
    #layertypes=database.getLayerTypes(dic=True)    
    #database.closeSession()

    return send_from_directory(directory='/Users/livia/msc_dissertation/CODE/data_sharing/data/input', filename='Greenland_1000_error.tif')'''
    

@app.route('/about')
def about():
    '''Returns an about page'''
    return render_template('about.html', error=False)





if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)