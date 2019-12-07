from flask import Flask, request, jsonify, make_response, render_template, url_for
import pymysql
import os

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "newuser"
        password = "password"
        db = "fabrica"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE cars (id INTEGER NOT NULL AUTO_INCREMENT, fabricante VARCHAR(20) NOT NULL, modelo VARCHAR(20) NOT NULL, vin VARCHAR(20) NOT NULL, PRIMARY KEY (id))''')
        self.cur.execute('''CREATE TABLE cars_data (id INTEGER NOT NULL AUTO_INCREMENT, VIN VARCHAR(20) NOT NULL, speed VARCHAR(20) NOT NULL, rpm VARCHAR(20) NOT NULL, coolant_temp VARCHAR(20) NOT NULL, engine_load VARCHAR(20) NOT NULL, intake_pressure VARCHAR(20) NOT NULL, PRIMARY KEY (id))''')
        return "Tabelas criadas"

    def insert_cars(self, fabricante, modelo, vin):
        query = f'''INSERT INTO cars  (fabricante, modelo, vin) VALUES ("{fabricante}", "{modelo}", "{vin}")'''
        self.cur.execute(query)
        self.con.commit()
        return "Carro inserido"	

    def insert_cars_data(self, vin, speed, rpm, coolant_temp, engine_load, intake_pressure):
        query = f'''INSERT INTO cars_data (vin, speed, rpm, coolant_temp, engine_load, intake_pressure) VALUES ("{vin}", "{speed}", "{rpm}", "{coolant_temp}", "{engine_load}", "{intake_pressure}")'''
        self.cur.execute(query)
        self.con.commit()
        return "Dados do carro inseridos"
	
    def get_cars(self):
        self.cur.execute(f'''SELECT * FROM cars''')
        result = self.cur.fetchall()
        return result

    def get_vin(self, vin):
        self.cur.execute('''SELECT vin FROM cars''')
        result = self.cur.fetchall()
        return result

    def get_data(self, vin):
        self.cur.execute(f'''SELECT * FROM cars_data WHERE vin="{vin}"''')
        result = self.cur.fetchall()
        return result

app = Flask(__name__)
db = Database()
# print(db.create_tables())

@app.route('/', methods=['POST', 'GET'])
def register_car():
    error = None

    if request.method == 'POST' and 'fabricante' in request.form and 'modelo' in request.form and 'vin' in request.form:
        fabricante = request.form['fabricante']
        modelo = request.form['modelo']
        vin = request.form['vin']

        carros = db.get_vin(vin)
        for carro in carros:
            if carro["vin"] == vin:
                error = "Carro ja cadastrado"

        db.insert_cars(fabricante, modelo, vin)

    carros = db.get_cars()
    return render_template('index.html', cars=carros)

@app.route('/dados', methods=['POST','GET'])
def show_data():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            vin = request.json['vin']
            speed = request.json['speed']
            rpm = request.json['rpm']
            coolant_temp = request.json['coolant_temp']
            engine_load = request.json['engine_load']
            intake_pressure = request.json['intake_pressure']

            db.insert_cars_data(vin, speed, rpm, coolant_temp, engine_load, intake_pressure)
            return jsonify({'message' : 'Data stored'}), 200
        else:
            return jsonify({'message' : 'No data provided'}), 400

    vin = request.args.get('vin')
    dados = db.get_data(vin)
    return render_template('dados.html', dados=dados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="80")
