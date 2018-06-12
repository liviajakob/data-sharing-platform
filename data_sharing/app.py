'''
Created on 25 Apr 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request, send_from_directory
import json
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)
    
@app.route('/', methods=['POST', 'GET'])
def index():
    database = Database()
    database.scopedSession()
    query = database.getDatasets()[0]
    
    database.closeSession()
    
    return render_template('main.html', data=query.getBoundingBox(), error=False)
 
 
 
@app.route('/datasets/<int:dataset_id>')
def datasets(dataset_id):
    '''Returns a JSON of the dataset'''
    database = Database()
    database.scopedSession()
    
    dataset=database.getDatasets(dataset_id)[0]
    geoDict=dataset.asGeoDict()
    print(geoDict)
    geoCollection = {}
    geoCollection['type']= 'FeatureCollection'
    geoCollection['features'] = [geoDict]
    
    database.closeSession()
    return jsonify(geoCollection)

 
  
@app.route('/data')
def data():
    '''Returns a JSON of the datasets, including filteroptions'''
    database = Database()
    database.scopedSession()
    
    filtering = 'hi' #request.args
    
    #data = request.data
    #dataDict = json.loads(data)
    
    ##lid = request.args.get('lid')    
    
    
    datasets=database.getDatasets(filtering=filtering, dic=True)
    ''''features=[]
    for ds in datasets:
        features.append(ds.asGeoDict())
        
    #print(geoDict)
    geoCollection = {}
    geoCollection['type']= 'FeatureCollection'
    geoCollection['features'] = features'''
    
    database.closeSession()

    return jsonify(datasets)

 
   
@app.route('/layertypes')
def layertypes():
    '''Returns a JSON of the datasets, including filteroptions'''
    database = Database()
    database.scopedSession()
    layertypes=database.getLayerTypes(dic=True)    
    database.closeSession()

    return jsonify(layertypes)

 
    
@app.route('/download', methods=['GET', 'POST'])
def download():
    ''''''
    #database = Database()
    #database.scopedSession()
    #layertypes=database.getLayerTypes(dic=True)    
    #database.closeSession()

    return send_from_directory(directory='/Users/livia/msc_dissertation/CODE/data_sharing/data/input', filename='Greenland_1000_error.tif')
    



if __name__ == '__main__':
    print("hi")
    
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)