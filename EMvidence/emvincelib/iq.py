# Reference: http://witestlab.poly.edu/~ffund/el9043/labs/lab1.html


# includes core parts of numpy, matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftfreq, fftshift
from sklearn import preprocessing
import os
import zmq
import random
import time


sampleRate=20000000.0

'''
# practice reading in complex values stored in a file
# Read in data that has been stored as raw I/Q interleaved 32-bit float samples
dat = np.fromfile("./data/with-aes.cfile", dtype="float32")
sampleRate=20000000

# Turn the interleaved I and Q samples into complex values
# the syntax "dat[0::2]" means "every 2nd value in 
# array dat starting from the 0th until the end"
dat = dat[0::2] + 1j*dat[1::2]

# Note: a quicker way to turn the interleaved I and Q samples  into complex values
# (courtesy of http://stackoverflow.com/a/5658446/) would be:
# dat = dat.astype(np.float32).view(np.complex64)
'''
#########################################################################

###############################################################################
#           Functions to acquire data from GRC through ZMQ sockets            #
###############################################################################

# Ref: https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pushpull.html

def startZMQClient(tcpHostPort="tcp://127.0.0.1:5557", socketType="PULL"):
    '''
    Start a ZMQ client socket connection in order to listen to a ZMQ
    server socket which is usually from a ZMQ Sink block in GRC.
    '''

    if socketType=="PULL":
        #print("PULL socket")
        consumer_id = random.randrange(1,10005)
        print("I am consumer #%s" % (consumer_id))
        context = zmq.Context()
        # recieve work
        consumer_receiver = context.socket(zmq.PULL)
        consumer_receiver.connect(tcpHostPort)
        return consumer_receiver

    elif socketType=="SUB":
        #print("SUB socket")
        subscriber_id = random.randrange(1,10005)
        print("I am subscriber #%s" % (subscriber_id))
        context = zmq.Context()
        subscriber_receiver = context.socket(zmq.SUB)
        subscriber_receiver.setsockopt_string(zmq.SUBSCRIBE, "")
        subscriber_receiver.connect(tcpHostPort)
        return subscriber_receiver
    
    else:
        print("Socket type not recognized.")
        return -1


def stopZMQClient(zmqClientSocket):
    '''
    Stop the ZMQ client socket.
    '''
    zmqClientSocket.close()
    print("Stopping client...")
    return 1

def genTraceFiles(zmqClientSocket, directoryPath, fileName, numFiles, sampleRate=20e6, initSequenceNumber=1, windowSize=10, windowStepSize=10):
    '''
    This function reads data from a ZMQ Client socket and generate EM trace
    files.
    windowSize = 10ms
    windowStepSize = 10ms
    sampleRate=20MHz
    '''
    # The data segment which we need to be filled
    # sample-rate x windowSize = num-samples
    # 20MHz X 10ms = 200000
    complexSampleLimit = int(sampleRate * (windowSize * 0.001))
    # initializing segment buffer
    segment = np.empty([0,0])

    fileCount = initSequenceNumber
    while True:
        buff = zmqClientSocket.recv()
        data = np.frombuffer(buff, dtype="float32")
        data = data[0::2] + 1j*data[1::2]        
        segment = np.append(segment, data)

        if(len(segment) >= complexSampleLimit):
            tempFileName= directoryPath + "/" + fileName + "." + str(fileCount) + ".npy"
            np.save(tempFileName, segment[0:complexSampleLimit])            
            # Reset the segment
            segment = np.empty([0,0])
            # incrementing the counter
            fileCount = fileCount + 1            
            
        if (fileCount > numFiles):
            return 1


def genSingleTraceFile(zmqClientSocket, directoryPath, fileName, sampleRate=20e6, windowSize=10):
    '''
    This function reads data from a ZMQ Client socket and generate a single EM trace file.
    windowSize = 10ms
    windowStepSize = 10ms
    sampleRate=20MHz
    '''
    # The data segment which we need to be filled
    # sample-rate x windowSize = num-samples
    # 20MHz X 10ms = 200000
    complexSampleLimit = int(sampleRate * (windowSize * 0.001))
    # initializing segment buffer
    segment = np.empty([0,0])

    #fileCount = initSequenceNumber
    while True:
        buff = zmqClientSocket.recv()
        data = np.frombuffer(buff, dtype="float32")
        data = data[0::2] + 1j*data[1::2]        
        segment = np.append(segment, data)

        if(len(segment) >= complexSampleLimit):
            tempFileName= directoryPath + "/" + fileName + ".npy"
            np.save(tempFileName, segment[0:complexSampleLimit])            
            # Reset the segment
            segment = np.empty([0,0])
            # returning from the function
            return 1
            # incrementing the counter
            #fileCount = fileCount + 1            
         	   
        #if (fileCount > numFiles):
        #    return 1



def startSlidingWindow(zmqClientSocket, function, params, sampleRate=20e6, windowSize=10, windowStepSize=10, duration=5):
    '''
    This function reads an IQ interleaved data stream from an ZMQ socet and then extract data according
    to a sliding window. Each extracted window of data is passed to the 'function', provided by the user,
    for processing.
    windowSize = 10ms
    windowStepSize = 10ms
    sampleRate=20MHz
    duration= 5s
    '''
    # The data segment which we need to be filled
    # sample-rate x windowSize = num-samples
    # 20MHz X 10ms = 200000
    complexSampleLimit = int(sampleRate * (windowSize * 0.001))
    complexStepLimit = int(sampleRate * (windowStepSize * 0.001))    
    #print("window size: %d" % complexSampleLimit)
    #print("window step size: %d" % complexStepLimit)
    # initializing segment buffer
    segment = np.empty([0,0])
    start_time = time.time()
    
    while True:
        buff = zmqClientSocket.recv()
        data = np.frombuffer(buff, dtype="float32")
        data = data[0::2] + 1j*data[1::2]        
        segment = np.append(segment, data)

        if(len(segment) >= complexSampleLimit):
            # calling the function given as a parameter
            #function(segment, *params)            
            function(segment[0:complexSampleLimit], *params)            
            # removing a chunk of samples from the front of the buffer
            segment = np.delete(segment, np.s_[:complexStepLimit:1])
        
        if ((time.time()-start_time) > duration):
            return 1
        
def processWindow(window, a,b):
    '''
    Sample user defined function to be used with 'startSlidingWindow()' function
    '''
    print(len(window))
    print("param1: %d param2: %d" % (a,b))
    tempFileName= "./data/AES" + "." + str(time.time()) + ".npy"
    np.save(tempFileName, window)  

def getTimeDuration(fileName, fileType="cfile"):
    '''
    Calculate the total time duration represented in an I-Q file that can be in either cfile or npy format.
    '''
    if (fileType=="cfile"):
        # dealing with a cfile file format
        #Original bytes in file (offset_bytes) => array of float32 (4bytes in each element)
        #data = np.fromfile(cfileName, dtype="float32")
        #each pair of elements of the array is combined to create a single complex numpy array element.
        #data = data[0::2] + 1j*data[1::2]
        #Therefore, origina_file_size = numpy_array_length x 2 x 4
        size_bytes = os.path.getsize(fileName)
        size_index = size_bytes / ( 2 * 4 )
    
        # sample_points = time x sample_rate
        size_time = size_index / sampleRate

    elif (fileType=="npy"):
        # dealing with a numpy file format
        data = np.load(fileName, mmap_mode='r')
        numpy_array_length = len(data)
        size_time = numpy_array_length / sampleRate

    else:
        # unrecognized file type
        size_time = -1

    return size_time
    

###############################################################################
#     Functions to process cFile data saved by GRC File Sink blocks           #
###############################################################################

def getData(cfileName):
    """
    Given a name of a *.cfile, this function extracts the interleaved
    Inphase-Quadrature data samples and convert it into a numpy array of complex
    data elements. *.cfile format has interleaved I and Q samples where each sample
    is a float32 type. GNURadio Companion (GRC) scripts output data into a file
    though a file sink block in this format.
    Read more in SDR data types: https://github.com/miek/inspectrum
    """
    # Read the *.cfile which has each element in float32 format.
    data = np.fromfile(cfileName, dtype="float32")
    # Take each consecutive interleaved I sample and Q sample to create a single complex element.
    data = data[0::2] + 1j*data[1::2]
    
    #print("data type=", type(data))
    
    # Return the complex numpy array.
    return data

def getSegmentData(fileName, offsetTime, windowTime, fileType="cfile"):
    '''
    Given a I-Q data file name, an offset value as a time, and an window time,
    this function extracts the required segment from the file and return it as
    a complx numpy array.    
    '''

    if (fileType=="cfile"):
        # dealing with a cfile file format
        data = getData(fileName)

    elif (fileType=="npy"):
        # dealing with a numpy file format
        data = np.load(fileName, mmap_mode='r')

    else:
        # unrecognized file type
        return -1

    # Segment starting offset (sample points)
    start = offsetTime * sampleRate    
    # Segment ending offset (sample points)
    end = start + (windowTime * sampleRate)
    #print("start=%d", int(start))
    #print("end=%d", int(end))
    #Return the starting index and ending index
    segment = data[int(start):int(end)]

    #return data
    return segment



###############################################################################
#             Functions to plot data in complex numpy arrays                  #
###############################################################################


def plotWaveform(data, show=1, file_name='./wavform.pdf', file_format='pdf'):
    """
    Given a data set as a complex numpy array, this function returns the waveform plot.
    """
    plt.figure()
    # Plot the waveform of the selected sample range of the numpy data array
    #plt.plot(data)
    plt.plot(np.abs(data))
    #plt.plot(np.real(data))
    #plt.plot(np.imag(data))
    
    if(show==1):
        plt.show()
    else:
        # Save the waveform into a PDF file
        plt.savefig(file_name, fotmat=file_format, bbox_inches='tight')
        
    return 1

def plotScatter(data, show=1):
    """
    Given a data set as a complex numpy array, this function returns the scatter plot.
    """
    plt.figure()
    # plot the scatter plot of the selected sample range of the numpy data array
    plt.scatter(np.real(data), np.imag(data))
    plt.title("Constellation of the 'signal' loaded from file")
    
    if(show==1):
        plt.show()
    else:
        # save the scatter plot into a PDF file
        plt.savefig('./scatter.pdf', fotmat='pdf', bbox_inches='tight')
        
    return 1

def plotPSD(data, show=1, file_name='./psd.pdf', file_format='pdf'):
    """
    Given a data set as a complex numpy array, this function returns the power spectral density (PSD) plot.
    """
    plt.figure()
    # plot the PSD of the selected sample range of the numpy data array
    plt.psd(data, NFFT=1024, Fs=sampleRate)
    
    if(show==1):
        plt.show()
    else:
        # save the PSD plot into a PDF file
        plt.savefig(file_name, fotmat=file_format, bbox_inches='tight')

    return 1

    
def plotFFT(data, show=1):
    """
    Given a data set as a complex numpy array, this function returns the FFT plot.
    """

    plt.figure()

    # get the length of the selected data sample range        
    N = len(data)
    # get the time interval beteween each sample
    T = 1.0 / sampleRate
    # calculate the FFT of the selected sample range. But the FFT x axis contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    yf = fft(data)
    # get the vector with frequencies of the sample range. But the output contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    freqs = fftfreq(N, T)
    # shift the frequencies to have it zero-centered, e.g., -4, -3, -2, -1, 0, 1, 2, 3, 4
    shifted_freqs = fftshift(freqs)
    # rearrange the FFT vector to have it zero-centered, e.g., -4, -3, -2, -1, 0, 1, 2, 3, 4
    new_yf = np.concatenate((yf[int(N/2):int(N)], yf[0:int(N/2)]))
    # plot the FFT vector against the frequencies
    plt.plot(shifted_freqs, np.abs(new_yf))    
    #print('len(shifted_freqs)=%d' % len(shifted_freqs))    
    #print('len(new_yf)=%d' % len(new_yf))    

    if(show==1):
        plt.show()
    else:
        # save theFFT plot as a PDF file.
        plt.savefig('./fft.pdf', fotmat='pdf', bbox_inches='tight')
        
    return 1


def plotSpectrogram(data, show=1, file_name='./spectrogram.pdf', file_format='pdf'):
    """
    Given a data set as a complex numpy array, this function returns the spectrogram plot.
    """

    plt.figure()
    
    # plot the spectrogram of the selected sample range
    #plt.specgram(data, NFFT=4096, Fs=sampleRate, cmap=plt.cm.get_cmap("Greys"))
    plt.specgram(data, NFFT=512, Fs=sampleRate)
    #plt.specgram(data, NFFT=4096, Fs=sampleRate)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    #plt.axis('off')
    #ax = plt.axes()
    #ax.xaxis.set_visible(False)
    #ax.yaxis.set_visible(False)
    
    # zoom in to the middle of the y-axis because 4 MHz band-pass in the GRC script has caused the
    # other y-axis frequency ranges to be highly attenuated and useless.
    #plt.ylim(-2000000, 2000000)    
    
    if(show==1):
        plt.show()
    else:
        # save the spectrogram into a PDF file.
        plt.savefig(file_name, fotmat=file_format, bbox_inches='tight', pad_inches=0)
        #plt.savefig('spectrogram-from-iq.pdf', fotmat='pdf', bbox_inches='tight')
        
    return 1


###############################################################################
#                         Depreciated function                                #
###############################################################################

def getFeatureVector(data):
    """
    Given a data set as a complex numpy array, this function returns a 500 elements long feature vector.
    """
    N = len(data)
    # calculate the FFT of the selected sample range. But the FFT x axis contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    yf = fft(data)
    # rearrange the FFT vector to have it zero-centered, e.g., -4, -3, -2, -1, 0, 1, 2, 3, 4
    new_yf = np.concatenate((yf[int(N/2):int(N)], yf[0:int(N/2)]))
    fftdata = np.abs(new_yf)
    
    # DC spike at the center due to the nature of SDR should be removed
    N = len(fftdata)
    fftdata[int(N/2)] = 0
    
    # Use only the middle portion of the FFT vector as a feature vector
    #featureVector = fftdata[int(N/4):int(3*N/4)]
    #featureVector = fftdata[3*N/8:5*N/8]
    featureVector = fftdata       
       
    # Make the feature vector small by breaking and averaging into 500 buckets.   
    # lenth of the FFT vector we are considering
    L = len(featureVector)
    # number of buckets
    #l = 500
    l = 1000
    index = 0
    bucketSize = L/l
    vector = []
    while index<len(featureVector):
        #avg = sum(featureVector[index:index+int(bucketSize)])/len(featureVector[index:index+int(bucketSize)])
        #vector.append(avg)
        maxi = max(featureVector[index:index+int(bucketSize)])
        vector.append(maxi)    
    
        index = index + int(bucketSize)
    
    fft_normalized = preprocessing.normalize([vector], norm='l2')

    # get the normalized numpy array (we take the first dimention which is the correct array)
    feature_vector = fft_normalized[0]
    return feature_vector[0:l]


###############################################################################
#                         Deleted function                                #
###############################################################################

'''  

def getTimeDuration(cFileName):
    """
    Calculate the total time duration represented in an I-Q file.
    """
    size_bytes = os.path.getsize(cFileName)

    #Original bytes in file (offset_bytes) => array of float32 (4bytes in each element)
    #data = np.fromfile(cfileName, dtype="float32")
    #each pair of elements of the array is combined to create a single complex numpy array element.
    #data = data[0::2] + 1j*data[1::2]
    #Therefore, origina_file_size = numpy_array_length x 2 x 4
    size_index = size_bytes / ( 2 * 4 )
    
    # sample_points = time x sample_rate
    size_time = size_index / sampleRate
    return size_time

def getSegment(timeOffset, window):
    """
    Given a starting time offset (seconds) and a time window (seconds), this function
    returns the starting and ending sample indexes of a complex numpy array.
    """
    # Segment starting offset (sample points)
    start = timeOffset * sampleRate
    # Segment ending offset (sample points)
    end = start + (window * sampleRate)
    #print("start=%d", int(start))
    #print("end=%d", int(end))
    #Return the starting index and ending index
    return int(start), int(end)

def getFFTVector(data, timeOffset, window):
    """
    Given a data set as a complex numpy array, a time offset (seconds), a time window (seconds)
    and a file name for the graph, this function returns the FFT vector as a numpy array.
    """
    # Get the desired starting and ending index of the numpy data array
    start, end = getSegment(timeOffset, window)    
    # get the length of the selected data sample range        
    N = len(data[start:end])
    
    print("segment length = ", N)
    
    # calculate the FFT of the selected sample range. But the FFT x axis contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    yf = fft(data[start:end])
    # rearrange the FFT vector to have it zero-centered, e.g., -4, -3, -2, -1, 0, 1, 2, 3, 4
    new_yf = np.concatenate((yf[int(N/2):int(N)], yf[0:int(N/2)]))
    # return the absolute values of the FFT vector.
    return np.abs(new_yf)


def getNormalizedFFTVector(data, timeOffset, window):
    """
    Given a data set as a complex numpy array, a time offset (seconds), a time window (seconds)
    and a file name for the graph, this function generates the FFT vector as a numpy array and
    normalize it before returning it.
    """
    # get the FFT vector as a numpy array
    fftdata = getFFTVector(data,timeOffset, window)

    # DC spike at the center due to the nature of SDR should be removed
    N = len(fftdata)
    fftdata[N/2] = 0    
    
    # normalize the numpy array (note that we input the fftdata inside []. So, the
    # input data is basically a 2-D vector)
    fft_normalized = preprocessing.normalize([fftdata], norm='l2')
    # return normalized numpy array (we take the first dimention which is the correct array)
    return fft_normalized[0]

def getFullFFTVector(data):
    """
    Given a data set as a complex numpy array, this function returns the FFT vector as a numpy array.
    """
    # get the length of the data sample        
    N = len(data)
    # calculate the FFT of the sample. But the FFT x axis contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    yf = fft(data)
    # rearrange the FFT vector to have it zero-centered, e.g., -4, -3, -2, -1, 0, 1, 2, 3, 4
    new_yf = np.concatenate((yf[N/2:N], yf[0:N/2]))
    # return the absolute values of the FFT vector.
    return np.abs(new_yf)

def getBucketedNormalizedFFTVector(data):
    # time window in seconds
    window_time = 0.01
    window_length = window_time * sampleRate
    timeOffset = ((len(data)-1) - window_length) / sampleRate
    start, end = getSegment(timeOffset, window_time)
    fftdata = getFFTVector(data,timeOffset, window_time)
    
    
    # get the FFT vector as a numpy array
    #fftdata = getFullFFTVector(data)

    # DC spike at the center due to the nature of SDR should be removed
    N = len(fftdata)
    fftdata[int(N/2)] = 0
    
    # Use only the middle portion of the FFT vector as a feature vector
    featureVector = fftdata[int(N/4):int(3*N/4)]
    #featureVector = fftdata[3*N/8:5*N/8]
    
    
    # Make the feature vector small by breaking and averaging into 500 buckets.   

    # lenth of the FFT vector we are considering
    L = len(featureVector)
    # number of buckets
    l = 500
    
    index = 0
    bucketSize = L/l
    vector = []
    while index<len(featureVector):
        avg = sum(featureVector[index:index+int(bucketSize)])/len(featureVector[index:index+int(bucketSize)])
        vector.append(avg)
        index = index + int(bucketSize)
    
    #print("len(vector)=%d" % len(vector))
    #print("vector=", vector)
    fft_normalized = preprocessing.normalize([vector], norm='l2')
        
    
    # normalize the numpy array (note that we input the fftdata inside []. So, the
    # input data is basically a 2-D vector)
    #fft_normalized = preprocessing.normalize([fftdata], norm='l2')
    
    # return normalized numpy array (we take the first dimention which is the correct array)
    return fft_normalized[0]

def getBucketedNormalizedFFTVectorFromFile():
    
    # time window in seconds
    window_time = 0.01
    window_length = window_time * sampleRate
    timeOffset = ((len(data)-1) - window_length) / sampleRate
    #fftdata = getFFTVector(data,timeOffset, window_time)
        
    # user defined variables
    offset_time = 0
    window_time = 0.01
    cFileName = "3des.dat"
    
    # converting offset and window from time to index values (sample points)
    offset_index = offset_time * sampleRate
    window_index = window_time * sampleRate
    
    # converting the offset and window index values into byte values of the I-Q data file
    offset_bytes = int(offset_index * 2 * 4)
    window_bytes = int(window_index * 2 * 4)
    
    print("offset_bytes = ", offset_bytes)
    print("window_index = ", window_index)
    print("window_bytes = ", window_bytes)
    
    # reading the required segment of bytes from the file
    f = open(cFileName, 'rb')
    f.seek(offset_bytes,1)
    segment = f.read(window_bytes)
    print("segment length = ", len(segment))

    data = np.frombuffer(segment, dtype="float32")
    data = data[0::2] + 1j*data[1::2]
    print("data type=", type(data))
    print("data length=", len(data))
    
    N = len(data)
     
    # calculate the FFT of the selected sample range. But the FFT x axis contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    yf = fft(data)
    # rearrange the FFT vector to have it zero-centered, e.g., -4, -3, -2, -1, 0, 1, 2, 3, 4
    new_yf = np.concatenate((yf[int(N/2):int(N)], yf[0:int(N/2)]))
    fftdata = np.abs(new_yf)
    
    # get the FFT vector as a numpy array
    #fftdata = getFullFFTVector(data)

    # DC spike at the center due to the nature of SDR should be removed
    N = len(fftdata)
    fftdata[int(N/2)] = 0
    
    # Use only the middle portion of the FFT vector as a feature vector
    featureVector = fftdata[int(N/4):int(3*N/4)]
    #featureVector = fftdata[3*N/8:5*N/8]
    
    
    # Make the feature vector small by breaking and averaging into 500 buckets.   

    # lenth of the FFT vector we are considering
    L = len(featureVector)
    # number of buckets
    l = 500
    
    index = 0
    bucketSize = L/l
    vector = []
    while index<len(featureVector):
        avg = sum(featureVector[index:index+int(bucketSize)])/len(featureVector[index:index+int(bucketSize)])
        vector.append(avg)
        index = index + int(bucketSize)
    
    #print("len(vector)=%d" % len(vector))
    #print("vector=", vector)
    fft_normalized = preprocessing.normalize([vector], norm='l2')
        
    
    # normalize the numpy array (note that we input the fftdata inside []. So, the
    # input data is basically a 2-D vector)
    #fft_normalized = preprocessing.normalize([fftdata], norm='l2')
    
    # return normalized numpy array (we take the first dimention which is the correct array)
    return fft_normalized[0]
'''
