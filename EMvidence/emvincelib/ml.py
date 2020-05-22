from scipy.fftpack import fft, fftfreq, fftshift
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import numpy as np
import os
from statistics import mode

# list variables to hold training and testing data
X = []
Y = []

# list variable to hold predicting data
#x = []


def getFeatureVector(data, featureVectorSize=1000):
    """
    Given a data set as a complex numpy array, this function returns a 500 elements long feature vector.
    """
    N = len(data)
    # calculate the FFT of the selected sample range. But the FFT x axis contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    #data = np.abs(data)
    data = np.nan_to_num(data)
    yf = fft(data)
    yf = np.nan_to_num(yf)
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
    #l = 10
    l = featureVectorSize
    #l = 500
    #l = 1000
    index = 0
    bucketSize = L/l
    vector = []
    while index<len(featureVector):
        #avg = sum(featureVector[index:index+int(bucketSize)])/len(featureVector[index:index+int(bucketSize)])
        #vector.append(avg)
        maxi = max(featureVector[index:index+int(bucketSize)])
        vector.append(maxi)    
    
        index = index + int(bucketSize)
    
    vector = np.nan_to_num(vector)
    fft_normalized = preprocessing.normalize([vector], norm='l2')

    # get the normalized numpy array (we take the first dimention which is the correct array)
    feature_vector = fft_normalized[0]
    return feature_vector[0:l]




def loadTrainingData(npyFileName, sampleRate, featureVectorSize, sliding_window, timeDuration, classLabel):
    '''
    Reads an .npy file that has This function reads raw EM traces from .npy files from the directory specified,
    Generates feature vector for each sliding window and loads them into the 2d array called X and
    fill the relevant class label in Y array.
    '''

    global X
    global Y

    #sliding_window_size = 0.01
    sliding_window_size = sliding_window

    data_npy= np.load(npyFileName, mmap_mode='r')
    #duration = iq.getTimeDuration(npyFileName, fileType="npy")
    duration = timeDuration

    print("Time duration of the npy file: " + str(duration) + " seconds")

    offset = 0

    while (offset + sliding_window_size) < duration:
       # Segment starting offset (sample points)
        start = offset * sampleRate
        # Segment ending offset (sample points)
        end = start + (sliding_window_size * sampleRate)
        segment = data_npy[int(start):int(end)]
    
        segment = np.nan_to_num(segment)
        feature_vector = getFeatureVector(segment, featureVectorSize)

        X.extend([feature_vector])
        Y.append(classLabel)
    
        offset = offset + sliding_window_size
        #print(offset)
    
    return 1

def loadPredictingData(npyFileName, sampleRate, featureVectorSize, sliding_window, timeDuration):
    '''
    Reads an .npy file that has This function reads raw EM traces from .npy files from the directory specified,
    Generates feature vector for each sliding window and loads them into the array called X.
    '''

    #global x
    x = []

    #sliding_window_size = 0.01
    sliding_window_size = sliding_window

    data_npy= np.load(npyFileName, mmap_mode='r')
    #duration = iq.getTimeDuration(npyFileName, fileType="npy")
    duration = timeDuration

    print("Time duration of the npy file: " + str(duration) + " seconds")

    offset = 0

    while (offset + sliding_window_size) < duration:
       # Segment starting offset (sample points)
        start = offset * sampleRate
        # Segment ending offset (sample points)
        end = start + (sliding_window_size * sampleRate)
        segment = data_npy[int(start):int(end)]
    
        segment = np.nan_to_num(segment)
        feature_vector = getFeatureVector(segment, featureVectorSize)

        x.extend([feature_vector])
    
        offset = offset + sliding_window_size
        #print(offset)
    
    return x


#def trainAndTest(classifier, X, Y):
def trainAndTest(classifier, X=X, Y=Y):
    '''
    The function to perform training and testing of the model
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=0)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict (X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
def tenFoldCrossValidation(classifier, X_data=X, Y_labels=Y):
    '''
    The function to perform 10 fold cross-validation
    '''
    scores = cross_val_score(classifier, X_data, Y_labels, cv=10)
    print(scores)
    return scores
    
def predictClass(classifier, x):
    y = classifier.predict(x)
    return mode(y)

def createClassifier():
    '''
    This function creates the the neural network classifier
    '''
    clf = MLPClassifier(solver='lbfgs', alpha=1e-20, hidden_layer_sizes=(10, 5), random_state=1)
    return clf

###############################################################################
#                         Depreciated function                                #
###############################################################################

def loadToXYFromEMTraces(trainingFilePath):
    '''
    This function reads raw EM traces from .npy files from the directory specified,
    generate feature vector for each and loads them into the 2d array called X and
    fill the relevant class label in Y array.
    '''
    pathToNpyFiles = trainingFilePath
    X = []
    Y = [] 
    listOfFiles = os.listdir(pathToNpyFiles)  
    #print("number of traces: %d" % len(listOfFiles))
    for fileName in listOfFiles:
        cryptoName, sequenceNumber, extension = fileName.split(".")    
        data = np.load(pathToNpyFiles+"/"+fileName)
        featureVector = getFeatureVector(data)
        #fftloaded = np.load(pathToNpyFiles+"/"+fileName)
        featureVector = featureVector.tolist()
        X.extend([featureVector])
        Y.append(cryptoName)
        #if len(X)==800:
        #    break      
    return X, Y


def loadDataToXY(trainingFilePath):
    '''
    This function loads data from .npy trace files from the directory specified
    into the 2d array called X and fill the relevant class label in Y array.
    '''
    pathToNpyFiles = trainingFilePath
    X = []
    Y = [] 
    listOfFiles = os.listdir(pathToNpyFiles)  
    #print("number of traces: %d" % len(listOfFiles))
    for fileName in listOfFiles:
        cryptoName, sequenceNumber, extension = fileName.split(".")    
        fftloaded = np.load(pathToNpyFiles+"/"+fileName)
        fftTrace = fftloaded.tolist()
        X.extend([fftTrace])
        Y.append(cryptoName)
        #if len(X)==800:
        #    break      
    return X, Y


