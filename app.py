from flask import Flask, redirect, render_template, request, url_for, jsonify
import mysql.connector, os
from mysql.connector import Error
from flaskext.mysql import MySQL
import redis, boto3

app = Flask(__name__) #Executando (__name__) para exibir somente as variaveis
@app.route('/healthcheck') #Executando (./healthcheck) para exibir o 0.0.0.0:5000/healthcheck
def healthcheck():
    api = versaoAPI()
    sts = status()
    mysql = conexaodb()
    nosql = NOSQL()
    fila = FILA()
    return jsonify(api, sts, mysql, nosql, fila)

def versaoAPI():
    versao = 'API: 1.0'
    return (versao)

def status():
    statusDeAcesso = 'Status 200'
    return(statusDeAcesso)
    
def conexaodb():
    conn = None
    try:
        conn = mysql.connector.connect(host=os.getenv('banco'),
           user=os.getenv('user'),
           password=os.getenv('password'),
           db=os.getenv('db')
         )
        if conn.is_connected():
            return ('Mysql OK')
    except:
        return ('Mysql: ERRO')

def FILA():
    conn =  None
    try:
        conectfila = boto3.client('sqs', aws_access_key_id=os.getenv('access'),aws_secret_access_key=os.getenv('secret'), region_name=os.getenv('region')) 
        geturl = conectfila.get_queue_url(QueueName=os.getenv('fila'))
        return('Fila: OK')
    except: 
        return('Fila: ERRO')


def NOSQL():
    conn =  None
    try:
        conn = redis.StrictRedis(host=os.getenv('nosql'), port=6379, password='') 
        if conn.ping() == True:
            return ('Nosql: Ok') 
    except: 
        return('Nosql: ERRO')


if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5000', debug=True)