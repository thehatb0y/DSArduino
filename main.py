from flask import Flask, jsonify
import random  # Usado para gerar valores simulados

import serial
import time
import re

app = Flask(__name__)

# Função para separar os valores de temperatura e pressão
def separate_data(linha_serial):
    # Usando regex para extrair os valores
    match = re.search(r'P{(\d+)};T{([\d.]+)};w{(\d+)};L{(\d+)};', linha_serial)

    if match:
        valor_P = match.group(1)
        valor_T = match.group(2)
        valor_w = match.group(3)
        valor_L = match.group(4)

        lista = [valor_P, valor_T, valor_w, valor_L]
        return lista
    else:
        return 0
    
def get_data():
    ser = serial.Serial('COM3', 9600, timeout=1)
    try:
        a=0
        while a==0:
            # Lê uma linha da porta serial
            linha_serial = ser.readline().decode('utf-8').strip()
            list = separate_data(linha_serial)
            if list != 0:
                a=1
                print(list)
                ser.close()
                return list
            time.sleep(1)
    except:
        print("Erro ao ler porta serial")
        ser.close()
        return 0

def ler_pressao():
    a = get_data()
    return a[0]

def ler_temperatura():
    a = get_data()
    return a[1]

def ler_watts():
    a = get_data()
    return a[2]

def ler_luminosidade():
    a = get_data()
    return a[3]

# Endpoints da API
@app.route('/temperatura', methods=['GET'])
def obter_temperatura():
    temperatura = ler_temperatura()
    return jsonify({'temperatura': temperatura})

@app.route('/pressao', methods=['GET'])
def obter_pressao():
    pressao = ler_pressao()
    return jsonify({'pressao': pressao})

@app.route('/watts', methods=['GET'])
def obter_watts():
    watts = ler_watts()
    return jsonify({'watts': watts})

@app.route('/luminosidade', methods=['GET'])
def obter_luminosidade():
    luminosidade = ler_luminosidade()
    return jsonify({'luminosidade': luminosidade})

if __name__ == '__main__':
    app.run(debug=True)
