'''
Created on 25 Apr 2018

@author: livia
'''
from display_data.database import Query, Database
from flask import Flask, render_template

app = Flask(__name__)
    
@app.route('/')
def index():
    database = Database()
    database.scopedSession()
    query = database.getDatasets(3)
    
    database.closeSession()
    
    return "This is {}".format(query[0])
    



if __name__ == '__main__':
    print("hi")
    query = Query(3)
    print(query)
    
    database = Database()
    database.scopedSession()
    query = database.getDatasets(1)[0]
    print(query)
    
    app.run(debug=True)