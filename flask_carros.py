from flask import Flask, request, jsonify, make_response, render_template
import pymysql
import os
import obd
import time

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "username"
        password = "password"
        db = "fabrica"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE users (id INTEGER NOT NULL AUTO_INCREMENT, usuario VARCHAR(20) NOT NULL, senha VARCHAR(20) NOT NULL, email VARCHAR(50), PRIMARY KEY (id))''')
        self.cur.execute('''CREATE TABLE cars (id INTEGER NOT NULL AUTO_INCREMENT, usuario VARCHAR(20) NOT NULL, marca VARCHAR(20) NOT NULL, modelo VARCHAR(20) NOT NULL, VIN VARCHAR(20) NOT NULL, PRIMARY KEY (id))''')
        self.cur.execute('''CREATE TABLE cars_data (id INTEGER NOT NULL AUTO_INCREMENT, VIN VARCHAR(20) NOT NULL, speed VARCHAR(20) NOT NULL, rpm VARCHAR(20) NOT NULL, coolant_temp VARCHAR(20) NOT NULL, engine_load VARCHAR(20) NOT NULL, intake_pressure VARCHAR(20) NOT NULL))''')
        return "Tabelas criadas"

    def insert_users(self, usuario, senha, email):
        query = f'''INSERT INTO users (usuario, senha, email) VALUES ("{usuario}", "{senha}", "{email}")'''
        self.cur.execute(query)
        self.con.commit()
        return "Usuario inserido"

    def insert_cars(self, usuario, marca, modelo, VIN):
        query = f'''INSERT INTO cars (usuario, marca, modelo, VIN) VALUES ("{usuario}", "{marca}", "{modelo}", "{VIN}")'''
        self.cur.execute(query)
        self.con.commit()
        return "Carro inserido" 

    def insert_cars_data(self, VIN, speed, rpm, coolant_temp, engine_load, intake_pressure):
        query = f'''INSERT INTO cars_data (VIN, speed, rpm, coolant_temp, engine_load, intake_pressure) VALUES ("{VIN}", "{speed}", "{rpm}", "{coolant_temp}", "{engine_load}", "{intake_pressure}")'''
        self.cur.execute(query)
        self.con.commit()
        return "Dados do carro inseridos"

    def get_users(self):
        self.cur.execute('''SELECT usuario FROM users''')
        result = self.cur.fetchall()
        return result   

    def get_password(self, usuario):

        self.cur.execute(f'''SELECT senha FROM users WHERE usuario="{usuario}"''')
        result = self.cur.fetchall()
        return result

    def get_cars(self, usuario):
        self.cur.execute(f'''SELECT * FROM cars WHERE usuario="{usuario}"''')
        result = self.cur.fetchall()
        return result

    def get_VIN(self,VIN):
        self.cur.execute('''SELECT VIN FROM cars''')
        result = self.cur.fetchall()
        return result

    def get_data(self, VIN):
       self.cur.execute(f'''SELECT * FROM cars_data WHERE VIN="{VIN}"''')
        result = self.cur.fetchall()
        return result

app = Flask(__name__)
db = Database()

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # db.create_tables()
    error = None
    msg = ["Felipe", "Batatão"]

    if request.method == 'POST': 
        usuario = request.form['usuario'] 
        senha = request.form['senha']
        usuarios = db.get_users()
        for user in usuarios:
            if user["usuario"] == usuario:
                if senha == db.get_password(usuario)[0]["senha"]:
                    return jsonify({'result' : "Usuario aprovado"}), 200

                else:
                    error = "Senha incorreta"
            else:
                error = "Usuario nao cadastrado"
        return jsonify({'result' : error}), 400

    return render_template('login.html', msg=msg)

@app.route('/api/register', methods=['POST', 'GET'])
    def register_page():
    print("request /api/register")
    msg = 'Alou'
    error = None

    if request.method == 'POST' and 'usuario' in request.form and 'senha' in request.form and 'email' in request.form:
        print("request POST")
        usuario = request.form['usuario']
        senha = request.form['senha']
        email = request.form['email']
        all_users = db.get_users()
        print (all_users)

        for user in all_users:
            if user["usuario"] == usuario:
                error = "Usuario ja cadastrado"
                return jsonify({'result' : error}), 400


            print(db.insert_users(usuario, senha, email))

            return jsonify({'result' : "Usuario cadastrado com sucesso"}), 200

        elif request.method == 'GET':
            msg = 'Preencha todos os campos!'

        return render_template('register.html', msg=msg)

@app.route('/carros', methods=['GET'])
def show_cars():

    usuario = request.form['usuario'] #fazer com request.args
    carros = db.get_cars(usuario)
    print (carros)
    return render_template('carros.html', carros=carros)


@app.route('/carros/dados', methods=['POST','GET'])
def show_data():
    # if request.method == 'POST':
    data = request.get_json()
    if data:
        VIN = request.json['VIN']
        speed = request.json['speed']
        rpm = request.json['rpm']
        coolant_temp = request.json['coolant_temp']
        engine_load = request.json['engine_load']
        intake_pressure = request.json['intake_pressure']

        db.insert_cars_data(VIN, speed, rpm, coolant_temp, engine_load, intake_pressure)

        dados = db.get_data(VIN)
        return render_template('dados.html', dados=dados)

    else: 
        return jsonify({'message' : 'No data provided'}), 400


    #usuario = request.form['usuario'] #fazer com request.args
    # VIN2 = request.form['VIN'] #fazer com request.args


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="3000")
