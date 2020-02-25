from scipy.fftpack import fft, fftfreq, fftshift
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import numpy as np
import os

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

def trainAndTest(classifier, X, Y):
    '''
    The function to perform training and testing of the model
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=0)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict (X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
def tenFoldCrossValidation(classifier, X_data, Y_labels):
    '''
    The function to perform 10 fold cross-validation
    '''
    scores = cross_val_score(classifier, X_data, Y_labels, cv=10)
    print(scores)
    return scores
    
def predictClass(classifier, x):
    y = classifier.predict(x)
    return y

def createClassifier():
    '''
    This function creates the the neural network classifier
    '''
    clf = MLPClassifier(solver='lbfgs', alpha=1e-20, hidden_layer_sizes=(10, 5), random_state=1)
    return clf

