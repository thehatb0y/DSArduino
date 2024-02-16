from flask import Flask, jsonify, request
from flask_cors import CORS

from flask import Flask, render_template, Response
import cv2

import serial
import time
import re


app = Flask(__name__)
CORS(app)
valorList = []
appIndex = Flask(__name__, static_folder='C:\\Users\\mtsc\\OneDrive\\Área de Trabalho\\ESeDS\\Arduino\\darkpan-1.0.0\\static')

# Get data from serial port
def get_data():
    porta_serial = serial.Serial('COM4', 9600, timeout=1)
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
        porta_serial.close()
        
    finally:
        # Fecha a porta serial ao encerrar o programa
        porta_serial.close()
        print("Porta serial fechada.")

# Send data to serial port  
def send_data(StringToSend):
    
    porta_serial = serial.Serial('COM4', 9600, timeout=1)
    try:
        while True:
            porta_serial.write(StringToSend.encode('utf-8'))
            return "Comando enviado com sucesso!"

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

def capture_frames():
    camera = cv2.VideoCapture(0)  # Abre a webcam padrão
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
def capture_frames1():
    camera = cv2.VideoCapture(1)  # Abre a webcam padrão
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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

@app.route('/554', methods=['GET'])
def enviar_544():
    send_data('554')
    return jsonify({'message': 'Comando 554 enviado com sucesso!'})

@app.route('/555', methods=['GET'])
def enviar_555():
    send_data('555')
    return jsonify({'message': 'Comando 555 enviado com sucesso!'})

@app.route('/445', methods=['GET'])
def enviar_445():
    send_data('445')
    return jsonify({'message': 'Comando 554 enviado com sucesso!'})

@app.route('/444', methods=['GET'])
def enviar_444():
    send_data('444')
    return jsonify({'message': 'Comando 555 enviado com sucesso!'})

@app.route('/10', methods=['GET'])
def enviar_10():
    send_data('10')
    return jsonify({'message': 'Comando 10 enviado com sucesso!'})

@app.route('/11', methods=['GET'])
def enviar_11():
    send_data('11')
    return jsonify({'message': 'Comando 11 enviado com sucesso!'})



@app.route('/getall', methods=['GET'])   
def obter_todos():
    all = get_data()
    return jsonify({'pressao': all[0][0], 'temperatura': all[0][1], 'ldr': all[0][2], 'transistor1': all[0][3], 'transistor2': all[0][4], 'servo': all[0][5]})
 


 # Função para capturar frames da webcam

# Rota para exibir a página HTML
@app.route('/')
def index():
    return appIndex.send_static_file('index.html')

# Rota para acessar a stream da webcam
@app.route('/video_feed')
def video_feed():
    return Response(capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(capture_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)