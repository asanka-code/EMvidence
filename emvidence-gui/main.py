from flask import Flask
from flask import render_template
from flask import request

import sys
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

#-------------------------------------------------------------------------------
@app.route("/")
def index(name=None):
  #return render_template('index.html', name=name)
  return render_template('login.html', name=name)


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
