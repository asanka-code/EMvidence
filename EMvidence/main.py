from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import jsonify, make_response

import sys
import io
import random
import time
import datetime
from flask import Response
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import database

import os
import signal
import subprocess
import configparser
import hashlib
#from werkzeug import secure_filename
import zipfile
import shutil
import importlib
import importlib.util
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from os import listdir
from os.path import isfile, isdir, join

# our own external python files
from emvincelib import iq, ml, stat
import authfunctions
import dataCaptureFunctions


# initialize the config file
config_file_name = "emvidence.config"
config = configparser.ConfigParser()
config.read(config_file_name)

app = Flask(__name__, static_folder="static", template_folder="templates")
# file upload directory
app.config['UPLOAD_FOLDER'] = config['general-settings']['temp-module-directory']

#-------------------------------------------------------------------------------
@app.route("/")
def index(name=None):
  #return render_template('index.html', name=name)
  resp = make_response(render_template('login.html', name=name))
  resp.set_cookie('auth', 'new')
  return resp

#-------------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard(name=None):

  if authfunctions.is_logged_in(request.cookies.get('auth')):
    # logged-in user
    resp = make_response(render_template('dashboard.html', name=name))
  else:
    # the request is not from a logged-in user
    resp = make_response(render_template('login.html'))
    resp.set_cookie('auth', 'new')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/about")
def about(name=None):

  if authfunctions.is_logged_in(request.cookies.get('auth')):
    # logged-in user
    resp = make_response(render_template('about.html', name=name))
  else:
    # the request is not from a logged-in user
    resp = make_response(render_template('login.html'))
    resp.set_cookie('auth', 'new')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/settings")
def settings(name=None):

  if authfunctions.is_logged_in(request.cookies.get('auth')):
    # logged-in user
    resp = make_response(render_template('settings.html', name=name))
  else:
    # the request is not from a logged-in user
    resp = make_response(render_template('login.html'))
    resp.set_cookie('auth', 'new')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/upload-data")
def upload_data(name=None):

  if authfunctions.is_logged_in(request.cookies.get('auth')):
    # logged-in user
    resp = make_response(render_template('upload-data.html', name=name))
  else:
    # the request is not from a logged-in user
    resp = make_response(render_template('login.html'))
    resp.set_cookie('auth', 'new')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/capture")
def capture(name=None):

  if authfunctions.is_logged_in(request.cookies.get('auth')):
    # logged-in user
    resp = make_response(render_template('capture-data.html', name=name))
  else:
    # the request is not from a logged-in user
    resp = make_response(render_template('login.html'))
    resp.set_cookie('auth', 'new')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/analyse")
def analyse(name=None):

  if authfunctions.is_logged_in(request.cookies.get('auth')):
    # logged-in user
    resp = make_response(render_template('analyse-data.html', name=name))
  else:
    # the request is not from a logged-in user
    resp = make_response(render_template('login.html'))
    resp.set_cookie('auth', 'new')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/user-authentication", methods=['POST', 'GET'])
def authentication():

  if authfunctions.is_passwd_correct(request.form['uname'], request.form['passwd']):
    # correct password
    #return render_template('dashboard.html')
    resp = make_response(render_template('dashboard.html'))
    resp.set_cookie('auth', 'emvidence')

  else:
    # incorrect password
    #return render_template('login.html') 
    resp = make_response(render_template('login.html'))
    resp.set_cookie('auth', 'wrong-credentials')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/logout")
def logout(name=None):
  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # updating the login timestamp
  database.updateLogoutTimestamp(db_con, 1)
  # closing database connection
  database.closeDBConnection(db_con)

  #return render_template('login.html', name=name)
  resp = make_response(render_template('login.html', name=name))
  resp.set_cookie('auth', 'logged-out')
  
  return resp

#-------------------------------------------------------------------------------
@app.route("/plot")
def plot():
  fig = create_figure()
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')

#-------------------------------------------------------------------------------
@app.route("/upload-the-data-file", methods=['POST', 'GET'])
def upload_the_data_file():

  #print("IMPORTANT: upload_the_data_file() called")

  # reading the configuration file
  config = configparser.ConfigParser()
  config.read(config_file_name)
  
  # take the settings sent from the UI
  sdr = request.form['sdr']
  center_frequency = request.form['center_frequency']
  center_frequency_scale = request.form['center_frequency_scale']
  sampling_rate = request.form['sampling_rate']
  hash_function = request.form['hash_function']

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

  # path to the data directory according to the config file
  directoryPath = str(config['general-settings']['temp-data-directory'])

  # saving the uploaded datafile to a temporary directory
  if request.method == 'POST':
    f = request.files['fileToUpload']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

  # convert the cFile to NumPy
  data = iq.getData(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
  # cFile file name without file extension
  file_name_without_extension = f.filename.split(".")[0]
  np.save(app.config['UPLOAD_FOLDER'] + "/" + str(file_name_without_extension) + ".npy", data)
  # moving NumPy file to the data directory
  shutil.move(app.config['UPLOAD_FOLDER'] + "/" + str(file_name_without_extension) + ".npy", directoryPath)
  # delete temporary array and temporary file
  del data
  os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

  # take file size in MB
  file_stats = os.stat(directoryPath + str(file_name_without_extension) + ".npy")
  file_size = int(file_stats.st_size / (1024 * 1024) )
  file_size = str(file_size) + "MB"

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
  with open(directoryPath + str(file_name_without_extension) + '.npy', 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
  hash_value = hasher.hexdigest()
  config['general-settings']['temp-hash-value'] = str(hash_value)

  # save new hash information to config file
  with open(config_file_name, 'w') as configfile:
    config.write(configfile)

  # load the data for graphing
  data = np.load(directoryPath + str(file_name_without_extension) + '.npy', mmap_mode='r')

  # take only a segment to plot
  data = data[0:10000]

  # set the sampling rate of the emvincelib library settings
  iq.sampleRate = int(sampling_rate)
  print("Sampling rate of emvincelib: " + str(iq.sampleRate))


  # removing old graph files
  old_graph_file_name = directoryPath + "waveform." + str(config['general-settings']['figure-sequence_number']) + ".png"
  if os.path.isfile(old_graph_file_name): # checking if the file exists
    os.remove(old_graph_file_name)
  old_graph_file_name = directoryPath + "fft." + str(config['general-settings']['figure-sequence_number']) + ".png"
  if os.path.isfile(old_graph_file_name): # checking if the file exists
    os.remove(old_graph_file_name)
  old_graph_file_name = directoryPath + "spectrogram." + str(config['general-settings']['figure-sequence_number']) + ".png"
  if os.path.isfile(old_graph_file_name): # checking if the file exists
    os.remove(old_graph_file_name)

  # removing old graph files
  #old_graph_file_name = directoryPath + "waveform." + str(config['general-settings']['figure-sequence_number']) + ".png"
  #os.remove(old_graph_file_name)
  #old_graph_file_name = directoryPath + "fft." + str(config['general-settings']['figure-sequence_number']) + ".png"
  #os.remove(old_graph_file_name)
  #old_graph_file_name = directoryPath + "spectrogram." + str(config['general-settings']['figure-sequence_number']) + ".png"
  #os.remove(old_graph_file_name)
  
  # generate a random sequence number
  sequence_number = random.randint(1,1000)

  # plot the waveform graph
  new_graph_file_name = directoryPath + "waveform." + str(sequence_number) + ".png"
  iq.plotWaveform(data, show=0, file_name=new_graph_file_name, file_format='png')

  # plot PSD graph
  new_graph_file_name = directoryPath + "fft." + str(sequence_number) + ".png"
  iq.plotPSD(data, show=0, file_name=new_graph_file_name, file_format='png')
  
  # plot spectrogram
  new_graph_file_name = directoryPath + "spectrogram." + str(sequence_number) + ".png"
  iq.plotSpectrogram(data, show=0, file_name=new_graph_file_name, file_format='png')

  # updating the figure sequence number
  config['general-settings']['figure-sequence_number'] = str(sequence_number)
  # save new settings to the config file
  with open(config_file_name, 'w') as configfile:
    config.write(configfile)

  # clear the memory
  del data

  # making database entries for the dataset and EM trace
  # TODO: Add a feature to have a single dataset ID and multiple EM trace files inside a directory structure
  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # enter the dataset entry
  dataset_id = database.addDataset(db_con, str(file_name_without_extension), "no/directory/path/currently", "no description available", 1, 1)

  # Create a directory for the dataset with the dataset ID
  os.mkdir(directoryPath + str(dataset_id))

  # move EM trace file into the dataset directory
  shutil.move(directoryPath + str(file_name_without_extension) + ".npy", directoryPath + str(dataset_id))

  # enter the EM trace entry
  database.addEMTrace(db_con, directoryPath + str(dataset_id) + "/" + str(file_name_without_extension) + '.npy', str(center_frequency), str(sampling_rate), str(hasher.hexdigest()), str(hash_function), dataset_id)
  # closing database connection
  database.closeDBConnection(db_con)

  # compose the response
  response_body = {
    "status" : "done",
    "file_name" : str(file_name_without_extension) + ".npy",
    "file_size" : file_size,
    "hash_type" : str(hash_function),
    "hash_value" : str(hash_value)
  }
  
  res = make_response(jsonify(response_body), 200)

  # sending a response
  return res
  #return "done"

#-------------------------------------------------------------------------------
@app.route("/capture-data", methods=['POST', 'GET'])
def capture_data():

  # reading the configuration file
  config = configparser.ConfigParser()
  config.read(config_file_name)
  
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


  # Check if the signal SDR device is available.
  if dataCaptureFunctions.is_device_available(sdr) is False:
    # the device is not available. We send an error message to the web front-end
    # compose the response
    response_body = {
      "status" : "The SDR device is not available",
      "file_name" : "",
      "file_size" : "",
      "hash_type" : "",
      "hash_value" : "",
    }
    res = make_response(jsonify(response_body), 200)
    # sending a response
    return res
  # Beyond this point executes only if the device is available

  # compose the command line arguments for the SDR driver
  command = "python2 ./sdr-drivers/sdr_driver.py " + str(sdr) + " " + str(center_frequency) + " " + str(sampling_rate)

  # start the grc script with the parameters
  pro = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

  # wait the specified sampling duration to capture tdata  
  time.sleep(int(sampling_duration))
  '''
  zmqSocket = iq.startZMQClient(tcpHostPort="tcp://127.0.0.1:5557", socketType="SUB")
  iq.genSingleTraceFile(zmqSocket, directoryPath, str(file_name), windowSize=int(sampling_duration))
  iq.stopZMQClient(zmqSocket)
  '''

  # stop the grc script
  os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups

  # path to the data directory according to the config file
  directoryPath = str(config['general-settings']['temp-data-directory'])

  # convert the cFile to NumPy
  data = iq.getData(directoryPath + "data.cfile")
  np.save(directoryPath + str(file_name) + ".npy", data)

  # delete temporary array and temporary file
  del data
  os.remove(directoryPath + "data.cfile")

  # take file size in MB
  file_stats = os.stat(directoryPath + str(file_name) + ".npy")
  file_size = int(file_stats.st_size / (1024 * 1024) )
  file_size = str(file_size) + "MB"

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
  hash_value = hasher.hexdigest()
  config['general-settings']['temp-hash-value'] = str(hash_value)

  # save new hash information to config file
  with open(config_file_name, 'w') as configfile:
    config.write(configfile)

  # load the data for graphing
  data = np.load(directoryPath + str(file_name) + '.npy', mmap_mode='r')

  # take only a segment to plot
  data = data[0:10000]

  # set the sampling rate of the emvincelib library settings
  iq.sampleRate = int(sampling_rate)
  print("Sampling rate of emvincelib: " + str(iq.sampleRate))


  # reading the configuration file
  #config = configparser.ConfigParser()
  #config.read(config_file_name)

  # removing old graph files
  old_graph_file_name = directoryPath + "waveform." + str(config['general-settings']['figure-sequence_number']) + ".png"
  if os.path.isfile(old_graph_file_name): # checking if the file exists
    os.remove(old_graph_file_name)
  old_graph_file_name = directoryPath + "fft." + str(config['general-settings']['figure-sequence_number']) + ".png"
  if os.path.isfile(old_graph_file_name): # checking if the file exists
    os.remove(old_graph_file_name)
  old_graph_file_name = directoryPath + "spectrogram." + str(config['general-settings']['figure-sequence_number']) + ".png"
  if os.path.isfile(old_graph_file_name): # checking if the file exists
    os.remove(old_graph_file_name)

  # generate a random sequence number
  sequence_number = random.randint(1,1000)

  # plot the waveform graph
  new_graph_file_name = directoryPath + "waveform." + str(sequence_number) + ".png"
  iq.plotWaveform(data, show=0, file_name=new_graph_file_name, file_format='png')

  # plot PSD graph
  new_graph_file_name = directoryPath + "fft." + str(sequence_number) + ".png"
  iq.plotPSD(data, show=0, file_name=new_graph_file_name, file_format='png')
  
  # plot spectrogram
  new_graph_file_name = directoryPath + "spectrogram." + str(sequence_number) + ".png"
  iq.plotSpectrogram(data, show=0, file_name=new_graph_file_name, file_format='png')

  # updating the figure sequence number
  config['general-settings']['figure-sequence_number'] = str(sequence_number)
  # save new settings to the config file
  with open(config_file_name, 'w') as configfile:
    config.write(configfile)

  # clear the memory
  del data

  # making database entries for the dataset and EM trace
  # TODO: Add a feature to have a single dataset ID and multiple EM trace files inside a directory structure
  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # enter the dataset entry
  dataset_id = database.addDataset(db_con, str(file_name), "no/directory/path/currently", "no description available", 1, 1)

  # Create a directory for the dataset with the dataset ID
  os.mkdir(directoryPath + str(dataset_id))

  # move EM trace file into the dataset directory
  shutil.move(directoryPath + str(file_name) + ".npy", directoryPath + str(dataset_id))

  # enter the EM trace entry
  database.addEMTrace(db_con, directoryPath + str(dataset_id) + "/" + str(file_name) + '.npy', str(center_frequency), str(sampling_rate), str(hasher.hexdigest()), str(hash_function), dataset_id)
  # closing database connection
  database.closeDBConnection(db_con)

  # compose the response
  response_body = {
    "status" : "done",
    "file_name" : str(file_name) + ".npy",
    "file_size" : file_size,
    "hash_type" : str(hash_function),
    "hash_value" : str(hash_value)
  }
  
  res = make_response(jsonify(response_body), 200)

  # sending a response
  return res
  #return "done"


#-------------------------------------------------------------------------------
@app.route("/captured_data_view")
def captured_data_view(name=None):
  return render_template('captured_data_view_iframe.html', name=name)


#-------------------------------------------------------------------------------
@app.route("/analysis_report_view")
def analysis_report_view(name=None):
  return render_template('analysis_report_view_iframe.html', name=name)

#-------------------------------------------------------------------------------
@app.route("/get_waveform", methods=['POST', 'GET'])
def get_waveform():

  # reading the configuration file
  config = configparser.ConfigParser()
  config.read(config_file_name)

  # path to the graph file
  graph_file = str(config['general-settings']['temp-data-directory']) + "waveform." + str(config['general-settings']['figure-sequence_number']) + ".png"

  return send_file(graph_file, mimetype='image/png')
  #return send_file('./data/temp-waveform-graph.png', mimetype='image/png')


#-------------------------------------------------------------------------------
@app.route("/get_fft")
def get_fft():
  # reading the configuration file
  config = configparser.ConfigParser()
  config.read(config_file_name)

  # path to the graph file
  graph_file = str(config['general-settings']['temp-data-directory']) + "fft." + str(config['general-settings']['figure-sequence_number']) + ".png"

  return send_file(graph_file, mimetype='image/png')
  #return send_file('./data/temp-fft-graph.png', mimetype='image/png')

#-------------------------------------------------------------------------------
@app.route("/get_spectrogram")
def get_spectrogram():
  # reading the configuration file
  config = configparser.ConfigParser()
  config.read(config_file_name)

  # path to the graph file
  graph_file = str(config['general-settings']['temp-data-directory']) + "spectrogram." + str(config['general-settings']['figure-sequence_number']) + ".png"

  return send_file(graph_file, mimetype='image/png')
  #return send_file('./data/temp-spectrogram-graph.png', mimetype='image/png')


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

  #--------------------------------------------------------------
  # save the details that are necessary to create a report later
  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # reading the configuration file
  config = configparser.ConfigParser()
  config.read(config_file_name)
  # get the IoT device name
  device_name = database.getIoTDeviceName(db_con, int(iot_device_type))
  config['report-settings']['device'] = str(device_name)
  # get the path to the selected EM trace
  emtrace_path = database.getEMTracePath(db_con, int(dataset_choice))
  config['report-settings']['em-data-file'] = str(emtrace_path)
  # get the emtrace hash function
  emtrace_hash_function = database.getEMTraceHashFunction(db_con, int(dataset_choice))
  config['report-settings']['hash-function'] = str(emtrace_hash_function)
  # get the emtrace hash value
  emtrace_hash_value = database.getEMTraceHashValue(db_con, int(dataset_choice))
  config['report-settings']['hash-value'] = str(emtrace_hash_value)
  # create timestamp
  timestamp = time.time()
  timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
  config['report-settings']['time-stamp'] = str(timestamp)
  # closing database connection
  database.closeDBConnection(db_con)
  # save the new information to config file
  with open(config_file_name, 'w') as configfile:
    config.write(configfile)
  #--------------------------------------------------------------

  # clear the 'results' directory to remove any previously generated results
  if os.path.isdir("./results"):
    shutil.rmtree("./results")
  # now, create a new 'results directory'
  Path("./results").mkdir(parents=True, exist_ok=True)

  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # get the path to the selected EM trace
  emtrace_path = database.getEMTracePath(db_con, int(dataset_choice))
  # closing database connection
  database.closeDBConnection(db_con)

  # result count
  count = 0

  # response skeleton
  response_body = {"length" : count, }

  # take the selected module ids as a string
  selected_modules = request.form['selected_modules']
  # split the module id string into individual id elements in an array
  selected_modules = selected_modules.split(',')

  # process each module
  for module_id in selected_modules:
    print("LOG: Processing module ID: " + str(int(module_id)))
    # open database connection
    db_con = database.createDBConnection(database.database_name)
    # get module name
    module_name = database.getModuleName(db_con, int(module_id))
    # closing database connection
    database.closeDBConnection(db_con)
    # prepare the module path
    module_path = str(config['general-settings']['module-directory']) + "/" + str(module_name) + "/" + "main.py"
    # loading module
    mod = loadModule(module_path)
    # calling module functions
    #mod.initialize(1)
    mod.initialize(module_id, str(emtrace_path), "./results")
    results = mod.getResults()
    print("Module results: " + str(results))

    # add this result to the JSON object
    count = count + 1
    response_body[str(count)] = {"module_name" : str(module_name), "result" : str(results)}

  # update the response count
  response_body["length"] = count

  res = make_response(jsonify(response_body), 200)
  return res
  #return "done"


#-------------------------------------------------------------------------------
@app.route("/cancel-analysis", methods=['POST', 'GET'])
def cancel_analysis():

  # clear the 'results' directory to remove any previously generated results
  if os.path.isdir("./results"):
    shutil.rmtree("./results")
  # now, create a new 'results directory'
  Path("./results").mkdir(parents=True, exist_ok=True)
  
  return "done"


#-------------------------------------------------------------------------------
@app.route("/create-report", methods=['POST', 'GET'])
def create_report():

  #--------------------------------------------------------------
  # take the details that are necessary to create the report
  # reading the configuration file
  config = configparser.ConfigParser()
  config.read(config_file_name)
  # get the IoT device name
  device_name = config['report-settings']['device']
  # get the path to the selected EM trace
  emtrace_path = config['report-settings']['em-data-file']
  # get the emtrace hash function
  emtrace_hash_function = config['report-settings']['hash-function']
  # get the emtrace hash value
  emtrace_hash_value = config['report-settings']['hash-value']
  # get the timestamp
  timestamp = config['report-settings']['time-stamp']
  #--------------------------------------------------------------

  # open database connection
  db_con = database.createDBConnection(database.database_name)

  env = Environment(loader=FileSystemLoader('.'))
  template = env.get_template("templates/report-template.html")

  # take the list of directories that contains the results of each module
  module_dirs = [d for d in listdir("./results") if isdir(join("./results", d))]
  content = ""
  for i in module_dirs:
    content = content + "<b>Module ID:</b> " + str(i) + "<br/>"
    # get the name of the module
    module_name = database.getModuleName(db_con, int(i))
    content = content + "<b>Module Name:</b> " + module_name + "<br/>"
    # get the description of the module
    module_description = database.getModuleDescription(db_con, int(i))
    content = content + "<b>Module Description:</b> " + module_description + "<br/>"

    # take the list of image files that contains the results of this module
    module_path = join("./results", str(i))
    module_files = [f for f in listdir(module_path) if isfile(join(module_path, f))]
    
    for j in module_files:
      # take the path to the file
      file_path = join(module_path, j)

      # check file extension to identify file type
      extension = str(j).split(".")[1]
      if extension == "txt":
        # display text file content
        content = content + "<b>Module Output:</b> " + "<br/>"
        f = open(file_path, "r") 
        for line in f:
          content = content + str(line) + "<br/>"
        f.close()
      elif extension == "png":
        # display the image file
        content = content + "<img src='" + file_path + "' alt='graph' width='10'/>" + "<br/>"

    content = content + "<hr/>"

  template_vars = {"title" : "EMvidence - Analysis Report"
    , "device": device_name
    , "em_data_file": emtrace_path
    , "hash_function": emtrace_hash_function
    , "hash_value": emtrace_hash_value
    , "timestamp": timestamp
    , "module_results": content}
  html_out = template.render(template_vars)

  html = HTML(string=html_out, base_url=__file__)
  css = CSS(string='@page { size: A4; margin: 2cm } img { width: 100% } ')
  html.write_pdf("./results/report.pdf", stylesheets=[css])
  
  # closing database connection
  database.closeDBConnection(db_con)

  return "done"

#-------------------------------------------------------------------------------
@app.route("/send-report", methods=['POST', 'GET'])
def send_report():
  return send_file("./results/report.pdf")

#-------------------------------------------------------------------------------
@app.route("/get_dataset_list", methods=['POST', 'GET'])
def get_dataset_list():

  # open database connection
  db_con = database.createDBConnection(database.database_name)

  # take the data
  cursor = database.getEMTraces(db_con)

  # result count
  count = 0

  # response skeleton
  response_body = {"length" : count, }

  # take first row of results
  result = cursor.fetchone()

  # process all the results
  while result is not None:
    count = count + 1
    # add the this EM trace result to the JSON object
    response_body[str(count)] = {"value" : str(result[0]), "text" : str(result[1])}
    result = cursor.fetchone()

  # update the response count
  response_body["length"] = count

  # closing database connection
  database.closeDBConnection(db_con)

  '''
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
  '''
  
  res = make_response(jsonify(response_body), 200)
  return res


#-------------------------------------------------------------------------------
@app.route("/get_iot_device_list", methods=['POST', 'GET'])
def get_iot_device_list():

  # open database connection
  db_con = database.createDBConnection(database.database_name)

  # take the data
  cursor = database.getIoTDevices(db_con)

  # result count
  count = 0

  # response skeleton
  response_body = {"length" : count, }

  # take first row of results
  result = cursor.fetchone()

  # process all the results
  while result is not None:
    count = count + 1
    # add the this IoT device result to the JSON object
    response_body[str(count)] = {"value" : str(result[0]), "text" : str(result[1])}
    result = cursor.fetchone()

  # update the response count
  response_body["length"] = count

  # closing database connection
  database.closeDBConnection(db_con)

  #print(str(response_body))
  '''
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
  '''
  
  res = make_response(jsonify(response_body), 200)
  return res


#-------------------------------------------------------------------------------
@app.route("/get_modules_list", methods=['POST', 'GET'])
def get_modules_list():

  # open database connection
  db_con = database.createDBConnection(database.database_name)

  # take the data
  cursor = database.getModules(db_con)

  # result count
  count = 0

  # response skeleton
  response_body = {"length" : count, }

  # take first row of results
  result = cursor.fetchone()

  # process all the results
  while result is not None:
    count = count + 1
    # add the this IoT device result to the JSON object
    response_body[str(count)] = {"module_id" : str(result[0]), "module_name" : str(result[1])}
    result = cursor.fetchone()

  # update the response count
  response_body["length"] = count

  # closing database connection
  database.closeDBConnection(db_con)

  #print(str(response_body))
  '''
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
  '''

  res = make_response(jsonify(response_body), 200)
  return res

#-------------------------------------------------------------------------------
@app.route("/add_module", methods=['POST', 'GET'])
def add_module():  
  if request.method == 'POST':
    f = request.files['fileToUpload']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

    # zip file name without file extension
    zip_file_name = f.filename.split(".")[0]

    # path configurations
    directory_to_extract_to = config['general-settings']['temp-module-directory']
    module_directory = config['general-settings']['module-directory']

    status = addZippedModule(directory_to_extract_to, zip_file_name, module_directory)
    if status is True:

      # read module configuration file
      temp_config = configparser.ConfigParser()
      temp_config.read(module_directory + "/" + zip_file_name + "/config.config")
      module_description = temp_config['configuration']['description']

      # open database connection
      db_con = database.createDBConnection(database.database_name)
      # add module details to the database
      database.addModule(db_con, zip_file_name, module_description, 1)
      # closing database connection
      database.closeDBConnection(db_con)

      #print("Module added successfully.")
      return "done"
    else:
      #print("Failed to add the module")
      return "failed"
  else:
    pass

#-------------------------------------------------------------------------------
@app.route("/delete_module", methods=['POST', 'GET'])
def delete_module():
  # take the choices made by the user
  module_to_delete = request.form['module_to_delete']
  
  #print("IMPORTANT: " + str(module_to_delete))

  # open database connection
  db_con = database.createDBConnection(database.database_name)

  # get module name
  module_name = database.getModuleName(db_con, int(module_to_delete))
  # path to the module files
  module_directory = config['general-settings']['module-directory'] + "/" + str(module_name)
  #print("Module path: " + str(module_directory))

  # delete module files
  shutil.rmtree(str(module_directory))

  # delete module information from the database
  database.removeModule(db_con, int(module_to_delete))

  # closing database connection
  database.closeDBConnection(db_con)

  return "done"

#-------------------------------------------------------------------------------
@app.route("/delete_dataset", methods=['POST', 'GET'])
def delete_dataset():
  # take the choices made by the user
  emtrace_to_delete = request.form['dataset_to_delete']
  
  # open database connection
  db_con = database.createDBConnection(database.database_name)

  # get the ID of the dataset
  dataset_to_delete = database.getDatasetIDofEMTrace(db_con, int(emtrace_to_delete))

  dataset_directory = config['general-settings']['temp-data-directory'] + str(dataset_to_delete)

  print("EM trace ID to be deleted: " + str(emtrace_to_delete))
  print("Dataset ID to be deleted: " + str(dataset_to_delete))
  print("The directory to be deleted: " + str(dataset_directory))

  # delete dataset files
  shutil.rmtree(str(dataset_directory))

  # delete dataset and emtrace information from the database
  database.removeDataset(db_con, int(dataset_to_delete))
  database.removeEMTrace(db_con, int(emtrace_to_delete))

  # closing database connection
  database.closeDBConnection(db_con)
  
  return "done"

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

#-------------------------------------------------------------------------------
@app.route("/delete_iot_device", methods=['POST', 'GET'])
def delete_iot_device():
  # take the choices made by the user
  iot_device_to_delete = request.form['iot_device_to_delete']
  
  print("IMPORTANT: " + str(iot_device_to_delete))

  # open database connection
  db_con = database.createDBConnection(database.database_name)
  # delete IoT device
  database.removeIoTDevice(db_con, int(iot_device_to_delete))
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
def addZippedModule(directory_to_extract_to, zip_file_name, module_directory):
    '''
    This function takes a zipped file, extracts it at the same location,
    checks if all the necessary files are included in the extracted directory.
    Then it moves the extracted directory to another specified location and delete
    to files and directories in the original location.
    '''

    # location where the uploaded zip file is
    temp_path = directory_to_extract_to + "/" + zip_file_name

    # unzip the file and save in the same directory
    with zipfile.ZipFile(temp_path + ".zip", 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

    # check whether all the necessary files are included in the zip file
    if os.path.isfile(temp_path + "/main.py") is True:
        #print("main.py file exists.")
        pass
    else:
        # delete the temporary files and exit
        os.remove(temp_path + ".zip")
        shutil.rmtree(temp_path)
        return False

    if os.path.isfile(temp_path + "/ml-model.joblib") is True:
        #print("ml-model.joblib file exists.")
        pass
    else:
        # delete the temporary files and exit
        os.remove(temp_path + ".zip")
        shutil.rmtree(temp_path)
        return False

    if os.path.isfile(temp_path + "/README.txt") is True:
        #print("README.txt file exists.")
        pass
    else:
        # delete the temporary files and exit
        os.remove(temp_path + ".zip")
        shutil.rmtree(temp_path)
        return False

    if os.path.isfile(temp_path + "/config.config") is True:
        #print("config.config file exists.")
        pass
    else:
        # delete the temporary files and exit
        os.remove(temp_path + ".zip")
        shutil.rmtree(temp_path)
        return False

    # copy the module to correct location
    shutil.move(temp_path, module_directory)
    

    # delete the temporary files
    os.remove(temp_path + ".zip")
    #os.remove(directory_to_extract_to + "/*")

    return True

#-------------------------------------------------------------------------------
def loadModule(module_path):
    spec = importlib.util.spec_from_file_location("main", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod



#-------------------------------------------------------------------------------
if __name__ == "__main__":
  #app.run()
  app.run(host="0.0.0.0")
  
