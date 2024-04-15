from flask import Flask, jsonify
import psutil
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask(__name__)

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_cpu_temp():
    temp = psutil.sensors_temperatures()
    if 'cpu_thermal' in temp:
        return temp['cpu_thermal'][0].current
    elif 'cpu-thermal' in temp:
        return temp['cpu-thermal'][0].current
    else:
        return None

def get_memory_usage():
    mem = psutil.virtual_memory()
    total_memory = mem.total // (1024 * 1024)  # Convert to MB
    used_memory = mem.used // (1024 * 1024)    # Convert to MB
    return used_memory, total_memory

def get_uptime():
    return time.time() - psutil.boot_time()

@app.route('/')
def index():
    cpu_usage = get_cpu_usage()
    cpu_temp = get_cpu_temp()
    used_memory, total_memory = get_memory_usage()
    uptime = get_uptime()
    return jsonify(
                   cpu_usage=f"{cpu_usage}%",
                   cpu_temp=f"{cpu_temp}°C",
                   memory_usage=f"{used_memory}/{total_memory} MB",
                   uptime=f"{uptime/3600:.2f} hours"
                  )

if __name__ == '__main__':
    app.run(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT"))
    )
