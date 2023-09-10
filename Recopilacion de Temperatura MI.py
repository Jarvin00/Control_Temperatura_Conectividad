import pandas as pd
import Adafruit_DHT
import time
from datetime import datetime


pin_st = [17, 27, 22, 23]
data_list = []


sensor_temp = Adafruit_DHT.DHT22
timestamp1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


while True:

    timestamp = datetime.now().strftime('%Y-%m-%dH:%M:%S')
    success = True
    sensor_data = {'Timestamp': timestamp}

    for i in range(len(pin_st)):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor_temp, pin_st[i])
            print(f"Sensor {i+1} leído correctamente")  if temperature is not None and humidity is not None else print(f"Error al leer el sensor {i+1}")
                
        except Exception as e:
            print(f"Error al leer el sensor {i+1}: {e}")
            humidity = None
            temperature = None
            success = False

        sensor_data[f'Stemp{i+1}'] = temperature if temperature is not None else -1
        sensor_data[f'Shum{i+1}'] = humidity if (humidity is not None) and (humidity<=100) else -1
        


    data_list.append(sensor_data)
   

    try:
        data = pd.DataFrame(data_list)
        data.to_excel(f'sample_data_{timestamp1}.xlsx', sheet_name='Pag_1', index=False)
    except Exception as e:
        print(f"Error al escribir en el archivo Excel: {e}")

    time.sleep(600)
