'''
Created on 25 Apr 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request, send_from_directory
import json, os
from flask_cors import CORS
from display_data.system_configuration import ConfigSystem

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
    
    l_type = request.args.get('type')
    
    conf= ConfigSystem()
    pth = conf.config['layers']['colpath']
    pth= os.path.join(pth,conf.getColourFile(l_type))
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
    minmax = conf.getLayerScale(l_type)
    dic={'rgb': rgbarr, 'max': minmax['max'], 'min': minmax['min'], 'values': vals}

    return jsonify(dic)
 
 
 
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
    page=1
    page_size=5
    try:
        page=int(request.args.get('page'))-1
    except:
        pass
    
    try: 
        page_size = int(request.args.get('page_size'))
    except:
        pass
    #rows = 0#request.start
    
    #data = request.data
    #dataDict = json.loads(data)
    
    ##lid = request.args.get('lid')    
    
    
    datasets=database.getDatasets(filtering=filtering, dic=True, page=page, page_size=page_size)
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
    #database = Database()
    #database.scopedSession()
    #layertypes=database.getLayerTypes(dic=True)    
    #database.closeSession()
    
    conf = ConfigSystem()
    layertypes = conf.getLayerTypes()
    dic = {'layertypes': layertypes} 

    return jsonify(dic)

 
    
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
    print("hi")
    
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)