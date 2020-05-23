import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from emvincelib import iq, ml, stat
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from scipy.fftpack import fft
from sklearn import preprocessing
from joblib import dump, load
from statistics import mode

# update the module name
module_name = "mod-visualizer"

moduleId = 0
emTracePath = ""
resultsDirectory = ""
mlModelPath = ""

def initialize(module_id, em_trace_path, results_directory):
    print("initializing...")

    global moduleId
    global emTracePath
    global resultsDirectory
    global mlModelPath

    moduleId = int(module_id)
    emTracePath = em_trace_path
    # creating a directory to store output results of this module
    Path(results_directory + "/" + str(module_id)).mkdir(parents=True, exist_ok=True)
    resultsDirectory = results_directory  + "/" + str(module_id)
    mlModelPath = "./modules/" + str(module_name) + "/ml-model.joblib"

##############################################################################################

def getResults():

    #--------------------------------------------------
    # textual results of the module
    #--------------------------------------------------
    f = open(resultsDirectory + "/results.txt","w+")

    f.write("Visualizations of the data are illustrated in the following figures.")
    
    f.close() 
    #--------------------------------------------------


    #--------------------------------------------------
    # graphical results of the module
    #--------------------------------------------------
    # load the EM data
    data = np.load(emTracePath, mmap_mode='r')
    # take only a segment to plot
    #data = data[0:20000]

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


    results = "Produced waveform, power spectral density (PSD) and spectrogram figures."
    return results
