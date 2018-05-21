'''
Created on 25 Apr 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template

app = Flask(__name__)
    
@app.route('/')
def index():
    database = Database()
    database.scopedSession()
    query = database.getDatasets(1)[0]
    
    database.closeSession()
    
    return render_template('main.html', data=query.getBoundingBox(), error=False)
    



if __name__ == '__main__':
    print("hi")
    
    database = Database()
    database.scopedSession()
    query = database.getDatasets(1)[0]
    print(query)
    
    app.run(debug=True)