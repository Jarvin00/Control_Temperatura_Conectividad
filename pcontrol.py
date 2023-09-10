import Adafruit_DHT
import asyncio
import RPi.GPIO as GPIO
import time
import requests
import atexit

async def sensor_data():
    n_set = 0
    start = 0
    sensor_temp = Adafruit_DHT.DHT22
    pin_st = 27
    print("a")
           
    HOST = "192.168.0.9"
    PORT = 9999
    SERVER_IP = "http://200.126.14.228:5000/api/sensorPanelSolar/lastvalue"
#    SERVER_IP = "http://www.google.com"
    
    while True:   
        try:
                    print(n_set)
                    print(start)
                    humidity, temperature = Adafruit_DHT.read_retry(sensor_temp, pin_st)
                    n_set, start = await refrigeration_protocol(temperature, humidity, n_set, start)
                    print(f"Sensor {pin_st} leído correctamente",temperature,humidity)  
                        
        except Exception as e:
                    print(f"Error al leer el sensor {pin_st}: {e}")
                    humidity = None
                    temperature = None
                    success = False

        try:
            print("c")
            print(requests.get(SERVER_IP).status_code)

        except Exception as e:
            print(f"Error de Conexion de red: {e}")
            await reboot_protocol()  
        print("fin")
        time.sleep(10)
        

async def refrigeration_protocol(temperature, humidity, n_set, start):

    pin_vt = 12
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_vt, GPIO.OUT)
    print("e")
    if (temperature > 30 or humidity > 69) and n_set == 0:
        print("f")
        n_set = 1
        print(n_set)
        GPIO.output(pin_vt, False)
        start = time.time()       
        await sensor_warning_message(temperature, humidity)
    if temperature <= 30 and humidity <= 69 and n_set == 1:
        print("g")
        n_set = 0
        GPIO.output(pin_vt, True)
        final = time.time()       
        time_set = round(final-start, 0)
        await time_warning_message(time_set)
    return n_set, float(start)

async def reboot_protocol():
    print("h")
    pin_rl=22
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_rl, GPIO.OUT)        
        GPIO.output(pin_rl,True)
        time.sleep(15)
        GPIO.output(pin_rl, False)
        time.sleep(120)
        await reboot_warning_message()
        
    
    except Exception as e:
            print(e)        


async def sensor_warning_message (temperature,humidity):

    token = '6620354687:AAGCI2R7E3zS_cr-yy4PoaVmdhsN7S07wjE'
    chat_id = '-974561315'
    alert_temp = str("La temperatura supero los 30 grados, iniciando protocolo de refrigeracion")
    alert_humidity = str("La humedad general supero el 80 porciento, iniciando protocolo de refrigeracion")
    try:
        if temperature > 29:
            print(alert_temp)
            requests.post('https://api.telegram.org/bot'+token+'/sendMessage',
                      data={'chat_id':chat_id, 'text':alert_temp})
        if humidity > 69:
            print(alert_humidity)
            requests.post('https://api.telegram.org/bot' + token + '/sendMessage',
                          data={'chat_id': chat_id, 'text': alert_humidity})
    except Exception as e:
        print(e)

async def time_warning_message (time_set):

    token = '6620354687:AAGCI2R7E3zS_cr-yy4PoaVmdhsN7S07wjE'
    chat_id = '-974561315'
    try:
        if time_set > 60:
            time = time_set/60
            timer = "minutos"
            if time > 60:
                time = time_set / 60
                timer = "horas"
        else:
            time = time_set
            timer = "segundos"
        time_vent = str("La temperatura se ha estabilizado, el ventilador se mantuvo encendido:"+ str(time) +timer)
        print(time_vent)
        requests.post('https://api.telegram.org/bot'+token+'/sendMessage',
                      data={'chat_id':chat_id, 'text':time_vent})
    except Exception as e:
        print(e)
async def reboot_warning_message ():
    
    token = '6620354687:AAGCI2R7E3zS_cr-yy4PoaVmdhsN7S07wjE'
    chat_id = '-974561315'
    alert_reboot = str("La señal de conexión se perdio, se procedera a activar el protocolo de reinicio")
    print(alert_reboot)
    try:
        requests.post('https://api.telegram.org/bot'+token+'/sendMessage',
                  data={'chat_id':chat_id, 'text':alert_reboot})
    except Exception as e:
        print(e)


def exit_handler():
    GPIO.cleanup()
atexit.register(exit_handler)
asyncio.run(sensor_data())
# try:
#     asyncio.run(sensor_data())
# except KeyboardInterrupt:
#     GPIO.cleanup()