'''
Internal API for web GUI
File: app.py

App Endpoints:
    index - the main app page
    about - the about page
    
    colours - returns requested colours as JSON
    datasets - returns requested datasets as JSON
    layertypes - returns all available layertypes as JSON

Classes:
    MyFormatter - specific Formatter
    APIRequestException - API Exception class


@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request
from display_data.system_configuration import ConfigSystem
from string import Formatter

app = Flask(__name__)
  

# render HTML templates
    
@app.route('/', methods=['POST', 'GET'])
def index():
    '''HTML for index page of the app'''
    conf=ConfigSystem()
    params = conf.getWebParameters()
    api_loc = conf.getApiRoot()+':'+str(conf.getApiPort())
    return render_template('main.html', api_location=api_loc, tiles_weblocation=params['tiles_weblocation'], map_centre=params['map_centre'], projection=params['projection'])

@app.route('/about')
def about():
    '''HTML for about page'''
    conf=ConfigSystem()
    api_loc = conf.getApiRoot()+':'+str(conf.getApiPort())
    return render_template('about.html', root=api_loc)



# internal API
 
@app.route('/colours', methods=['GET'])
def colours():
    '''
    Returns requested colour schema as JSON
    
    Input parameter:
        layergroup_id (int) - id of the layergroup
    
    '''
    layer_id = request.args.get('layergroup_id')
    database = Database()
    database.scopedSession()
    try:
        layer=database.getLayerGroups({'id': layer_id})[0]
    except IndexError:
        raise APIRequestException('Not Found: Requested layergroup does not exist', status_code=404)
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
    '''Returns a JSON of the datasets, including filteroptions
    
    Input Parameters
        layertype (str) - (optional) Type of data. Use one of the following: dem, error, velocity, rate
        startdate (str) - (optional) Filters only datasets with layers starting before this date. Format: 'YYYY-MM-DD' (e.g. 2013-11-21)
        enddate (str) - (optional)     Filters only datasets with layers ending after this date. Format: 'YYYY-MM-DD' (e.g. 2013-11-21)
        id (int) - (optional) Dataset id. Only returns the dataset with the specified id
        page (int) - (optional), (default: 1) Page number
        page (int) - (optional), (default 8) Page size
        response (str) - (optional), (default: json) Response type. Use one of the following: json, xml
    
    
    '''
    database = Database()
    database.scopedSession()
        
    page=0
    page_size=8
    if 'page' in request.args:
        try:
            page=int(request.args.get('page'))-1
        except:
            raise APIRequestException('Invalid Arguments: <page> must be an integer', status_code=420)
    if 'page_size' in request.args:
        try:
            page_size = int(request.args.get('page_size'))
        except ValueError:
            raise APIRequestException('Invalid Arguments: <page_size> must be an integer', status_code=420)
    
    layerinfo=False
    if 'layerinfo' in request.args:
        try:
            layerinfo=booleanConverter(request.args.get('layerinfo'))
        except ValueError:
            raise APIRequestException('Invalid Arguments: <folayerin> must be a boolean', status_code=420)
    try:
        datasets=database.getDatasets(filters=request.args.to_dict(), dic=True, page=page, page_size=page_size, orderbyarea=True, layerinfo=layerinfo)
    except ValueError:
        raise APIRequestException('Invalid Arguments: one or multiple input parameters are invalid, refer to the documentation', status_code=420)
    database.closeSession()
    return jsonify(datasets)

 
   
@app.route('/layertypes')
def layertypes():
    '''Returns the available layertypes
    '''
    conf = ConfigSystem()
    layertypes = conf.getLayerTypes()
    dic = {'layertypes': layertypes} 
    return jsonify(dic)



    
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
        rv = dict(self.payload or ())
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





def booleanConverter(value):
    '''Converts a boolean string to a boolean
    Raises a ValueError if input string can't be converted
    
    Input Parameter:
        value (str) - a boolean string; False, false, True or true 
    
    '''
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError


# Formatting


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
    port= ConfigSystem().getAppPort()
    app.run(debug=True, threaded=True, host='0.0.0.0', port=port)
