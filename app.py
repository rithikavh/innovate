# app.py
from flask import Flask, render_template, request, jsonify
import hashlib
import datetime
import json
import os

app = Flask(__name__)

blockchain = []

def create_genesis_block():
    genesis_block = {
        'index': 0,
        'timestamp': str(datetime.datetime.now()),
        'data': 'Genesis Block',
        'previous_hash': '0',
        'hash': calculate_hash(0, str(datetime.datetime.now()), 'Genesis Block', '0')
    }
    blockchain.append(genesis_block)

def calculate_hash(index, timestamp, data, previous_hash):
    block_string = str(index) + timestamp + str(data) + previous_hash
    return hashlib.sha256(block_string.encode()).hexdigest()

def create_new_block(data, previous_hash):
    index = len(blockchain)
    timestamp = str(datetime.datetime.now())
    hash_value = calculate_hash(index, timestamp, data, previous_hash)
    return {
        'index': index,
        'timestamp': timestamp,
        'data': data,
        'previous_hash': previous_hash,
        'hash': hash_value
    }

def add_block(data):
    previous_block = blockchain[-1]
    new_block = create_new_block(data, previous_block['hash'])
    blockchain.append(new_block)
    return new_block

def is_chain_valid():
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]
        if current_block['previous_hash'] != previous_block['hash']:
            return False
        if calculate_hash(current_block['index'], current_block['timestamp'], current_block['data'], current_block['previous_hash']) != current_block['hash']:
            return False
    return True

create_genesis_block()

@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain)

@app.route('/add_license', methods=['POST'])
def add_license():
    content_id = request.form['content_id']
    license_details = request.form['license_details']
    data = f'License: Content ID: {content_id}, Details: {license_details}'
    new_block = add_block(data)
    return jsonify(new_block)

@app.route('/verify_chain')
def verify_chain():
    is_valid = is_chain_valid()
    return jsonify({'is_valid': is_valid})

@app.route('/get_chain')
def get_chain():
    return jsonify({'chain': blockchain})

if __name__ == '__main__':
    app.run(debug=True, port=5001)