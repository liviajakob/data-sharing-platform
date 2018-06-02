'''
Created on 2 Jun 2018

@author: livia
'''
from display_data.database import Database
from flask import Flask, render_template, jsonify, request
import json

api = Flask(__name__)

@api.route('/', methods=['POST', 'GET'])
def index():
    ###
    dic = {}
    dic['hi']='Livia'
    return jsonify(dic)