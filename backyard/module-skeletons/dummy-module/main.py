import os
import numpy as np
from pathlib import Path
from emvincelib import iq, ml, stat

moduleId = 0
emTracePath = ""
resultsDirectory = ""

def initialize(module_id, em_trace_path, results_directory):
    print("initializing...")

    global moduleId
    global emTracePath
    global resultsDirectory

    moduleId = int(module_id)
    emTracePath = em_trace_path
    # creating a directory to store output results of this module
    Path(results_directory + "/" + str(module_id)).mkdir(parents=True, exist_ok=True)
    resultsDirectory = results_directory  + "/" + str(module_id)
    
def preprocess(em_trace):
    print("preprocess() called.")
    
def classify():
    print("classify() called.")

def getResults():
    print("getResults() called.")

    print("EM trace path: " + emTracePath)
    print("Results directory: " + resultsDirectory)

    #--------------------------------------------------
    # textual results of the module
    #--------------------------------------------------
    f = open(resultsDirectory + "/results.txt","w+")

    for i in range(10):
        f.write("This is line %d\r\n" % (i+1))

    f.close() 
    #--------------------------------------------------


    #--------------------------------------------------
    # graphical results of the module
    #--------------------------------------------------
    # load the EM data
    data = np.load(emTracePath, mmap_mode='r')
    # take only a segment to plot
    data = data[0:20000]

    # plot the waveform graph
    new_graph_file_name = resultsDirectory + "/waveform.png"
    iq.plotWaveform(data, show=0, file_name=new_graph_file_name, file_format='png')

    # plot PSD graph
    new_graph_file_name = resultsDirectory + "/psd.png"
    iq.plotPSD(data, show=0, file_name=new_graph_file_name, file_format='png')

    # plot spectrogram
    new_graph_file_name = resultsDirectory + "/spectrogram.png"
    iq.plotSpectrogram(data, show=0, file_name=new_graph_file_name, file_format='png')
    #--------------------------------------------------

    #if os.path.isfile(em_trace): # checking if the file exists
    #    data_size = os.path.getsize(em_trace)
    #    results = "I can access data file with " + str(data_size) + " bytes."
    #else:
    #    results = "I cannot access data file"

    results = "Here's the results of the analysis.\n Classification accuracy: 99%"
    return results

def getConfusionMatrix():
    print("getConfusionMatrix() called.")