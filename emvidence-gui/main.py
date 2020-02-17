from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import jsonify, make_response

import sys
import io
import random
import time
from flask import Response
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from emvincelib import iq, ml, stat
import database

import os
import signal
import subprocess
import configparser
import hashlib


# initialize the config file
config_file_name = "emvidence.config"
config = configparser.ConfigParser()
config.read(config_file_name)

app = Flask(__name__)

#-------------------------------------------------------------------------------
@app.route("/")
def index(name=None):
  #return render_template('index.html', name=name)
  return render_template('login.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard(name=None):
  return render_template('dashboard.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/settings")
def settings(name=None):
  return render_template('settings.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/capture")
def capture(name=None):
  return render_template('capture-data.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/analyse")
def analyse(name=None):
  return render_template('analyse-data.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/user-authentication", methods=['POST', 'GET'])
def authentication():
  # print(request.method, file=sys.stderr)
  # print(request.form['uname'] + " " + request.form['passwd'], file=sys.stderr)

  if is_passwd_correct(request.form['uname'], request.form['passwd']):
    # correct password
    return render_template('dashboard.html')
  else:
    # incorrect password
    return render_template('login.html')


#-------------------------------------------------------------------------------
@app.route("/logout")
def logout(name=None):
  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # updating the login timestamp
  database.updateLogoutTimestamp(db_con, 1)
  # closing database connection
  database.closeDBConnection(db_con)

  return render_template('login.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/plot")
def plot():
  fig = create_figure()
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')

#-------------------------------------------------------------------------------
@app.route("/capture-data", methods=['POST', 'GET'])
def capture_data():
  
  # take the settings sent from the UI
  sdr = request.form['sdr']
  center_frequency = request.form['center_frequency']
  center_frequency_scale = request.form['center_frequency_scale']
  sampling_rate = request.form['sampling_rate']
  sampling_duration = request.form['sampling_duration']
  hash_function = request.form['hash_function']
  file_name = request.form['file_name']

  # convert the center frequency in the correct format 
  center_frequency = int(center_frequency)
  if center_frequency_scale == "H":
    center_frequency = center_frequency
  elif center_frequency_scale == "K":
    center_frequency = center_frequency * 1000
  elif center_frequency_scale == "M":
    center_frequency = center_frequency * 1000000
  elif center_frequency_scale == "G":
    center_frequency = center_frequency * 1000000000

  # compose the command line arguments for the SDR driver
  command = "python2 ./sdr-drivers/sdr_driver.py " + str(sdr) + " " + str(center_frequency) + " " + str(sampling_rate)

  # start the grc script with the parameters
  pro = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

  # path to the data directory according to the config file
  directoryPath = str(config['general-settings']['temp-data-directory'])

  # capture the data  
  zmqSocket = iq.startZMQClient(tcpHostPort="tcp://127.0.0.1:5557", socketType="SUB")
  iq.genSingleTraceFile(zmqSocket, directoryPath, str(file_name), windowSize=int(sampling_duration))
  iq.stopZMQClient(zmqSocket)

  # stop the grc script
  os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups

  # update the selected hash function
  config['general-settings']['temp-hash-function'] = str(hash_function)

  # select the hash function picked by the user
  if hash_function == "md5":
    hasher = hashlib.md5()
  elif hash_function == "sha1":
    hasher = hashlib.sha1()
  elif hash_function == "sha256":
    hasher = hashlib.sha256()

  # calculating the hash value and set to the config field
  with open(directoryPath + str(file_name) + '.npy', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
  config['general-settings']['temp-hash-value'] = str(hasher.hexdigest())

  # save new hash information to config file
  with open(config_file_name, 'w') as configfile:
    config.write(configfile)

  # load the data for graphing
  data = np.load(directoryPath + str(file_name) + '.npy')

  # plot the waveform graph
  graph_file_name = directoryPath + str(config['general-settings']['default-waveform-file'])
  iq.plotWaveform(data, show=0, file_name=graph_file_name, file_format='png')

  # plot the PSD graph
  graph_file_name = directoryPath + str(config['general-settings']['default-fft-file'])
  iq.plotPSD(data, show=0, file_name=graph_file_name, file_format='png')

  # plot the spectrogram graph
  graph_file_name = directoryPath + str(config['general-settings']['default-spectrogram-file'])
  iq.plotSpectrogram(data, show=0, file_name=graph_file_name, file_format='png')

  # clear the memory
  del data

  # sending a response
  return "done"


#-------------------------------------------------------------------------------
@app.route("/captured_data_view")
def captured_data_view(name=None):
  return render_template('captured_data_view_iframe.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/get_waveform", methods=['POST', 'GET'])
def get_waveform():
  return send_file('./data/temp-waveform-graph.png', mimetype='image/png')


#-------------------------------------------------------------------------------
@app.route("/get_fft")
def get_fft():
  return send_file('./data/temp-fft-graph.png', mimetype='image/png')

#-------------------------------------------------------------------------------
@app.route("/get_spectrogram")
def get_spectrogram():
  return send_file('./data/temp-spectrogram-graph.png', mimetype='image/png')


#-------------------------------------------------------------------------------
@app.route("/get_default_directory", methods=['POST', 'GET'])
def get_settings_information():
  config = configparser.ConfigParser()
  config.read(config_file_name)
  return str(config['general-settings']['temp-data-directory'])


#-------------------------------------------------------------------------------
@app.route("/get_em_data_format", methods=['POST', 'GET'])
def get_em_data_format():
  config = configparser.ConfigParser()
  config.read(config_file_name)
  return str(config['general-settings']['em-data-format'])


#-------------------------------------------------------------------------------
@app.route("/save_settings", methods=['POST', 'GET'])
def save_settings():
  # take the settings values
  capture_directory = request.form['capture_directory']
  em_data_format = request.form['em_data_format']

  config = configparser.ConfigParser()
  config.read(config_file_name)

  config['general-settings']['temp-data-directory'] = str(capture_directory)
  config['general-settings']['em-data-format'] = str(em_data_format)

  # save new settings to the config file
  with open(config_file_name, 'w') as configfile:
    config.write(configfile)
    
  return "done"

#-------------------------------------------------------------------------------
@app.route("/analyze-data", methods=['POST', 'GET'])
def analze_data():
  
  # take the choices made by the user
  dataset_choice = request.form['dataset_choice']
  iot_device_type = request.form['iot_device_type']

  # take the selected module ids as a string
  selected_modules = request.form['selected_modules']
  # split the module id string into individual id elements in an array
  selected_modules = selected_modules.split(',')

  time.sleep(2)

  print("IMPORTANT: " + dataset_choice + " " + iot_device_type)
  print(selected_modules)

  return "done"


#-------------------------------------------------------------------------------
@app.route("/cancel-analysis", methods=['POST', 'GET'])
def cancel_analysis():
  return "done"


#-------------------------------------------------------------------------------
@app.route("/get_dataset_list", methods=['POST', 'GET'])
def get_dataset_list():
  
  response_body = {
    "length" : 2,
    "1" : {
      "value" : "1",
      "text" : "Arduino case data"
    },
    "2" : {
      "value" : "2",
      "text" : "RaspberryPi case data"
    }
  }
  
  res = make_response(jsonify(response_body), 200)
  return res


#-------------------------------------------------------------------------------
@app.route("/get_iot_device_list", methods=['POST', 'GET'])
def get_iot_device_list():

  response_body = {
    "length" : 2,
    "1" : {
      "value" : "1",
      "text" : "Arduino Leonardo"
    },
    "2" : {
      "value" : "2",
      "text" : "RaspberryPi 3B+"
    }
  }
  
  res = make_response(jsonify(response_body), 200)
  return res


#-------------------------------------------------------------------------------
@app.route("/get_modules_list", methods=['POST', 'GET'])
def get_modules_list():

  response_body = {
    "length" : 4,
    "1" : {
      "module_id" : "4001",
      "module_name" : "Arduino Activity Detection"
    },
    "2" : {
      "module_id" : "4002",
      "module_name" : "Arduino Modification Detection"
    },
    "3" : {
      "module_id" : "4003",
      "module_name" : "Raspberry Pi Cryptography Detection"
    },
    "4" : {
      "module_id" : "4004",
      "module_name" : "Raspberry Pi Modification Detection"
    }
  }
  
  res = make_response(jsonify(response_body), 200)
  return res


#-------------------------------------------------------------------------------
@app.route("/add-iot-device", methods=['POST', 'GET'])
def add_iot_device():
  # take the choices made by the user
  new_iot_device_name = request.form['new_iot_device_name']
  new_iot_device_description = request.form['new_iot_device_description']

  #print("IMPORTANT: " + str(new_iot_device_name) + " " + str(new_iot_device_description))

  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # adding new IoT device
  database.addIoTDevice(db_con, new_iot_device_name, new_iot_device_description)
  # closing database connection
  database.closeDBConnection(db_con)

  return "done"

################################### Functions ######################################


#-------------------------------------------------------------------------------
def create_figure():
  fig = Figure()
  axis = fig.add_subplot(1, 1, 1)
  xs = range(100)
  ys = [random.randint(1, 50) for x in xs]
  axis.plot(xs, ys)
  axis.set_xlabel("Time (s)")
  axis.set_ylabel("Amplitude")
  return fig
  #return "Analysis page!"


#-------------------------------------------------------------------------------
def is_passwd_correct(uname, passwd):
  '''
  This function takes a username and a password as parameters and lookup in the
  database. Returns true if the username and passwords matches. Returns false otherwise.
  '''

  if uname == 'asanka' and passwd == 'emvidence':
    # open database connection
    db_con = database.createDBConnection(database.database_name)
    # updating the login timestamp
    database.updateLoginTimestamp(db_con, 1)
    # closing database connection
    database.closeDBConnection(db_con)
    return True
  else:
    return False
  
if __name__ == "__main__":
  app.run()

  
