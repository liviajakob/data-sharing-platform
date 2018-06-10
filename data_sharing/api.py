'''
Created on 2 Jun 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request, send_file
import json
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Download(Resource):
    def download(filename):
        uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=uploads, filename=filename)

api.add_resource(HelloWorld, '/')
api.add_resource(HelloWorld, '/')


'''@api.route('/', methods=['POST', 'GET'])
def index():
    ###
    dic = {}
    dic['hi']='Livia'
    return jsonify(dic)'''
    
    
if __name__ == '__main__':
    app.run(debug=True)