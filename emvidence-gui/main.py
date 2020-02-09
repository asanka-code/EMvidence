from flask import Flask
from flask import render_template
from flask import request

import sys
import io
import random
import time
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from emvincelib import iq, ml, stat

import os
import signal
import subprocess
import configparser


# initialize the config file
config = configparser.ConfigParser()
config.read('emvidence.config')

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

  # calculate hash value of the EM data file and put in the database
  if hash_function == "md5":
    pass
  elif hash_function == "sha1":
    pass
  elif hash_function == "sha256":
    pass

  # sending a response
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
    return True
  else:
    return False
  
if __name__ == "__main__":
  app.run()

  
