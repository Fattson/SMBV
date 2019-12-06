import obd
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int
import time
import requests

#Tempo entre iterações (s)
t = 1

def decodifica(messages):
	d = messages[0].data 
	d = d[3:]
	v = d.decode('ASCII') 
	return v  

#Estabelece conexão OBD
# ports = obd.scan_serial()                        
connection = obd.OBD()

vin = OBDCommand("vin", "Vehicle Id Number", b"0902", 20, decodifica)
connection.supported_commands.add(vin)

#Rotina de aquisição
while (True):
	get_speed = obd.commands.SPEED 
	get_rpm = obd.commands.RPM
	get_coolant_temp = obd.commands.COOLANT_TEMP
	get_engine_load = obd.commands.ENGINE_LOAD 
	get_intake_pressure = obd.commands.INTAKE_PRESSURE
	# get_VIN = obd.commands.vin

	try:
		speed = connection.query(get_speed) 
		rpm = connection.query(get_rpm)
		coolant_temp = connection.query(get_coolant_temp)
		engine_load = connection.query(get_engine_load)
		intake_pressure = connection.query(get_intake_pressure) 
		VIN = connection.query(vin)

		# car_data = {"speed": speed.value.magnitude, "rpm": rpm.value.magnitude, "coolant_temp": coolant_temp.value.magnitude, "engine_load": engine_load.value.magnitude, "intake_pressure": intake_pressure.value.magnitude, "vin": 137915}

		car_data = {
			"speed":30,
			"rpm": 3000.0,
			"coolant_temp": 50,
			"engine_load":100,
			"intake_pressure": 40,
			"vin": "3FADP4EK4CM14767"
		}

		time.sleep(t)
		r = requests.post(url="http://localhost:3000/dados", json=car_data)

	except Exception as error:
		print(error)

# lista = []