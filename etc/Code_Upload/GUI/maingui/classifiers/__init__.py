from scipy.fftpack import fft
from sklearn import preprocessing
import numpy as np


# helper functions for Machine learning
def sample_data_sliding_window(data_file, sequence_size: int = 100, window_size: int = 10,
                               window_step_size: int = 2, sample_rate: int = 20e6):
    """
    Implemented by Asanka Sayakkara (UCD)
    :param data_file: Data file to read
    :param sequence_size: length of each EM trace in milliseconds
    :param window_size: length of the sliding window in milliseconds
    :param window_step_size: length of the sliding window step size in milliseconds
    :param sample_rate: Sampleign rate in Hz
    :return: Array of windowed data
    """
    output_array = []  # Returned multi-dim array with windowed data
    if type(data_file) == str:
        loaded_data = np.load(data_file, mmap_mode='r')  # Load data, read only
    else:
        loaded_data = data_file

    # Calculate steps, in seconds
    samples_per_window = round(sample_rate * (window_size / 1000))  # in Sec
    samples_per_step = round(sample_rate * (window_step_size / 1000))
    trace_max_sample_length = round(20e6 * (sequence_size / 1000))

    idx = 0  # Index into trace data, start
    while idx <= (trace_max_sample_length - samples_per_window):
        feature_vector = get_feature_vector(loaded_data[idx:(idx + samples_per_window)])
        output_array.append(feature_vector)
        idx += samples_per_step
    return output_array


def get_feature_vector(data):
    """
    Implemented by Asanka Sayakkara (UCD)
    Given a data set as a complex numpy array, this function returns a 500 elements long feature vector.
    """
    N = len(data)
    # calculate the FFT of the selected sample range. But the FFT x axis contains data
    # in the range from 0 to positive values first and at the end the negative values
    # like 0, 1, 2, 3, 4, -4, -3, -2, -1
    yf = fft(data)
    # rearrange the FFT vector to have it zero-centered, e.g., -4, -3, -2, -1, 0, 1, 2, 3, 4
    new_yf = np.concatenate((yf[int(N / 2):int(N)], yf[0:int(N / 2)]))
    fftdata = np.abs(new_yf)

    # DC spike at the center due to the nature of SDR should be removed
    N = len(fftdata)
    fftdata[int(N / 2)] = 0

    # Use only the middle portion of the FFT vector as a feature vector
    # featureVector = fftdata[int(N/4):int(3*N/4)]
    # featureVector = fftdata[3*N/8:5*N/8]
    featureVector = fftdata

    # Make the feature vector small by breaking and averaging into 500 buckets.
    # lenth of the FFT vector we are considering
    L = len(featureVector)
    # number of buckets
    # l = 500
    l = 1000
    index = 0
    bucketSize = L / l
    vector = []
    while index < len(featureVector):
        # avg = sum(featureVector[index:index+int(bucketSize)])/len(featureVector[index:index+int(bucketSize)])
        # vector.append(avg)
        maxi = max(featureVector[index:index + int(bucketSize)])
        vector.append(maxi)

        index = index + int(bucketSize)

    fft_normalized = preprocessing.normalize([vector], norm='l2')

    # get the normalized numpy array (we take the first dimention which is the correct array)
    feature_vector = fft_normalized[0]
    return feature_vector[0:l]
