import threading
from flask import Flask, jsonify

import serial
import time
import re


app = Flask(__name__)
valorList = []

# Função para separar os valores de temperatura e pressão
def get_data():
    porta_serial = serial.Serial('COM3', 9600, timeout=1)
    try:
        while True:
            # Lê uma linha da porta serial
            linha_serial = porta_serial.readline().decode('utf-8').strip()

            # Extrai os valores usando regex
            match = re.search(r'P{([\d.]+)},T{([\d.]+)},LDR{(\d+)},T1{(\w+)},T2{(\w+)},SP{(\d+)};', linha_serial)

            if match:
                # Armazena os valores em uma lista
                valores = [
                    float(match.group(1)),  # Valor de pressão
                    float(match.group(2)),  # Valor de temperatura
                    int(match.group(3)),    # Valor de LDR
                    match.group(4),          # Estado do Transistor1
                    match.group(5),          # Estado do Transistor2
                    int(match.group(6))      # Posição do Servo
                ]

                # Imprime a lista de valores
                valorList.clear()
                valorList.append(valores)
                
                return valorList
    

    except KeyboardInterrupt:
        print("Leitura da porta serial interrompida pelo usuário.")

    finally:
        # Fecha a porta serial ao encerrar o programa
        porta_serial.close()
        
def ler_pressao():
    a = get_data()
    return a[0][0]

def ler_temperatura():
    a = get_data()
    return a[0][1]

def ler_ldr():
    a = get_data()
    return a[0][2]

def ler_transistor1():
    a = get_data()
    return a[0][3]

def ler_transistor2():
    a = get_data()
    return a[0][4]

def ler_servo():
    a = get_data()
    return a[0][5]

# inicializa um thread para ler os dados da porta serial
#thread = threading.Thread(target=get_data)
#thread.start()


# Endpoints da API
@app.route('/pressao', methods=['GET'])
def obter_pressao():
    pressao = ler_pressao()
    return jsonify({'pressao': pressao})

@app.route('/temperatura', methods=['GET'])
def obter_temperatura():
    temperatura = ler_temperatura()
    return jsonify({'temperatura': temperatura})

@app.route('/ldr', methods=['GET'])
def obter_ldr():
    ldr = ler_ldr()
    return jsonify({'ldr': ldr})

@app.route('/transistor1', methods=['GET'])
def obter_transistor1():
    transistor1 = ler_transistor1()
    return jsonify({'transistor1': transistor1})

@app.route('/transistor2', methods=['GET'])
def obter_transistor2():
    transistor2 = ler_transistor2()
    return jsonify({'transistor2': transistor2})

@app.route('/servo', methods=['GET'])
def obter_servo():
    servo = ler_servo()
    return jsonify({'servo': servo})

if __name__ == '__main__':
    app.run(debug=True)
