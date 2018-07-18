'''
Created on 25 Apr 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from display_data.system_configuration import ConfigSystem
import ast
from string import Formatter

app = Flask(__name__)
#CORS(app)
    
@app.route('/', methods=['POST', 'GET'])
def index():
    try: 
        database = Database()
        database.scopedSession()
        query = database.getDatasets()[0]
        
        database.closeSession()
        
        return render_template('main.html', data=query.getExtent(), error=False)
    except:
        return render_template('main.html', data=query.getExtent(), error=True)
 
@app.route('/colours', methods=['GET'])
def colours():
    layer_id = request.args.get('layer_id')
    database = Database()
    database.scopedSession()
    layer=database.getLayerGroups({'id': layer_id})[0]
    database.closeSession()
    

    conf= ConfigSystem()
    pth = conf.getLayerGroupsColourfile(layer)
    file_o = open(pth, 'r')
    lines = file_o.readlines()
    rgbarr=[]
    vals=[]
    for line in lines:
        split=line.split()
        if split[0] != 'nan':
            c1= MyFormatter().format("{0} {1:t}", '', split[1])
            c2= MyFormatter().format("{0} {1:t}", '', split[2])
            c3= MyFormatter().format("{0} {1:t}", '', split[3])
            rgb='rgb('+c1+', ' + c2 + ', ' + c3 + ')'
            rgbarr.append(rgb)
            vals.append(split[0])
    minmax = {'min': "{0:.1f}".format(float(vals[0])), 'max': "{0:.1f}".format(float(vals[-1]))}
    dic={'rgb': rgbarr, 'max': minmax['max'], 'min': minmax['min'], 'values': vals}

    return jsonify(dic)
 
  
@app.route('/datasets')
def datasets():
    '''Returns a JSON of the datasets, including filteroptions'''
    database = Database()
    database.scopedSession()
    #filters = {}
    print('requestargs', request.args)
    '''if 'filter' in request.args:
        try: 
            print('TRY TO CENVERT', request.args.get('filter'))
            filters = ast.literal_eval(request.args.get('filter'))
        except Exception as e:
            print('NOT POSSIBLE')
            print(e)
            pass'''
        
    #print('FILTERRRR   ',filters, type(filters), 'ARGS: ', request.args.get('filter'), type(request.args.get('filter')), str(request.args.get('filter')))
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
    
    layerinfo=False
    if 'layerinfo' in request.args:
        layerinfo=booleanConverter(request.args.get('layerinfo'))
    
    datasets=database.getDatasets(filters=request.args.to_dict(), dic=True, page=page, page_size=page_size, orderbyarea=True, layerinfo=layerinfo)
    database.closeSession()

    return jsonify(datasets)

 
   
@app.route('/layertypes')
def layertypes():
    '''Returns the available layertypes'''
    #database = Database()
    #database.scopedSession()
    #layertypes=database.getLayerTypes(dic=True)    
    #database.closeSession()
    
    conf = ConfigSystem()
    layertypes = conf.getLayerTypes()
    dic = {'layertypes': layertypes} 

    return jsonify(dic)


    

@app.route('/about')
def about():
    '''Returns the about page HTML'''
    return render_template('about.html', error=False, root="localhost:5002")





def booleanConverter(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
            raise Exception


class MyFormatter(Formatter):
    '''Extends the Formatter class
    
    Use: 
        MyFormatter().format("{0} {1:t}", "Hello", 4.567)
        -- returns "Hello 4"
    
    '''
    def format_field(self, value, format_spec):
        if format_spec == 't':  # Truncate and render as int
            return str(int(float(value)))
        return super(MyFormatter, self).format_field(value, format_spec)





if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)