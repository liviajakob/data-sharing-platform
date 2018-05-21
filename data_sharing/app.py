'''
Created on 25 Apr 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify

app = Flask(__name__)
    
@app.route('/', methods=['POST', 'GET'])
def index():
    database = Database()
    database.scopedSession()
    query = database.getDatasets(1)[0]
    
    database.closeSession()
    
    return render_template('main.html', data=query.getBoundingBox(), error=False)
 
 
 
@app.route('/datasets/<int:dataset_id>')
def datasets(dataset_id):
    database = Database()
    database.scopedSession()
    
    dataset=database.getDatasets(dataset_id)[0]
    geoDict=dataset.asGeoDict()
    print(geoDict)
    database.closeSession()
    return jsonify(geoDict)

 
 
    



if __name__ == '__main__':
    print("hi")
    
    app.run(debug=True)