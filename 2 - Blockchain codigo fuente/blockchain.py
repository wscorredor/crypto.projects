#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:10:09 2024
@author: wolfang corredor
"""

# Módulo 1 - Crear una Cadena de Bloques

# Para Instalar:
# Flask==1.1.2: pip install Flask==1.1.2, en caso de que existan inconvenientes, eliminar las librerías existentes e instalar las últimas versiones
# Cliente HTTP Postman: Postman es una herramienta útil para probar y desarrollar APIs. Puede utilizarse para enviar solicitudes HTTP a los endpoints definidos en este código.
# pip install --upgrade jinja2

# Introducción y Explicación del Código:
# Este programa implementa una cadena de bloques (blockchain) básica utilizando Python.
# Una cadena de bloques es una estructura de datos descentralizada y segura que registra transacciones
# en bloques enlazados mediante criptografía. Este código crea una blockchain simple y proporciona
# funcionalidades para minar nuevos bloques, obtener la cadena de bloques completa y verificar su validez.
# Después de ejecutar el código, se puede acceder a los endpoints definidos a través de una aplicación
# web Flask. Los endpoints incluyen la minería de un nuevo bloque, la obtención de la cadena de bloques
# completa y la verificación de su validez.

# Importar las librerías
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Crear la Cadena de Bloques
class Blockchain:
    
    def __init__(self):
        # Inicialización de la cadena de bloques con el bloque génesis
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        # Crear un nuevo bloque en la cadena
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        # Obtener el último bloque en la cadena
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        # Algoritmo de prueba de trabajo para encontrar el nonce (prueba de trabajo)
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else: 
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        # Generar el hash del bloque usando SHA-256
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        # Comprobar la validez de toda la cadena de bloques
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
# Parte 2 - Minado de un Bloque de la Cadena

# Crear una aplicación web usando Flask
app = Flask(__name__)
# Si se obtiene un error 500, actualizar Flask, reiniciar Spyder y ejecutar la siguiente línea
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Crear una instancia de la clase Blockchain
blockchain = Blockchain()

# Endpoint para minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : '¡Enhorabuena, has minado un nuevo bloque!', 
                'index': block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200

# Endpoint para obtener la cadena de bloques completa
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchain.chain, 
                'length' : len(blockchain.chain)}
    return jsonify(response), 200

# Endpoint para comprobar la validez de la cadena de bloques
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'Todo correcto. La cadena de bloques es válida.'}
    else:
        response = {'message' : 'Houston, tenemos un problema. La cadena de bloques no es válida.'}
    return jsonify(response), 200  

# Ejecutar la aplicación en el host y puerto especificados
app.run(host = '0.0.0.0', port = 5000)
