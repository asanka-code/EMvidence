import numpy as np
from scipy.stats import ttest_ind, ttest_1samp

def getCorrelationCoefficient(variable1, variable2):
    '''
    This function returns the correlation coefficient of two python lists
    '''
    correlation = np.corrcoef(variable1, variable2)[1,0]
    return correlation

def getMeasurement90Confidence(measurements):
    '''
    When a list of values, where each value is an indipendent measurement, this
    function returns the mean of the measurements and the +/- value range within
    which the true value lies with a 90% confidence.
    '''
    measurements = np.array(measurements)
    mean = measurements.mean()
    probabilityRange90Percent = measurements.std() * 1.64
    return mean, probabilityRange90Percent


def getMeasurement95Confidence(measurements):
    '''
    When a list of values, where each value is an indipendent measurement, this
    function returns the mean of the measurements and the +/- value range within
    which the true value lies with a 95% confidence.
    '''
    measurements = np.array(measurements)
    mean = measurements.mean()
    probabilityRange95Percent = measurements.std() * 1.96
    return mean, probabilityRange95Percent


def getMeasurement99Confidence(measurements):
    '''
    When a list of values, where each value is an indipendent measurement, this
    function returns the mean of the measurements and the +/- value range within
    which the true value lies with a 99% confidence.
    '''
    measurements = np.array(measurements)
    mean = measurements.mean()
    probabilityRange99Percent = measurements.std() * 2.58
    return mean, probabilityRange99Percent


def getRepeatedMeasurements90Confidence(means):
    '''
    When a list of values given, where each value is a mean of repeated measurements,
    this function returns the mean of the means and the +/- value range within which
    the true value lies with a 90% confidence.
    '''
    means = np.array(means)
    mean = means.mean()
    probabilityRange90Percent = (means.std() * 1.64)/np.sqrt(len(means))
    return mean, probabilityRange90Percent

def getRepeatedMeasurements95Confidence(means):
    '''
    When a list of values given, where each value is a mean of repeated measurements,
    this function returns the mean of the means and the +/- value range within which
    the true value lies with a 95% confidence.
    '''
    means = np.array(means)
    mean = means.mean()
    probabilityRange95Percent = (means.std() * 1.96)/np.sqrt(len(means))
    return mean, probabilityRange95Percent

def getRepeatedMeasurements99Confidence(means):
    '''
    When a list of values given, where each value is a mean of repeated measurements,
    this function returns the mean of the means and the +/- value range within which
    the true value lies with a 99% confidence.
    '''
    means = np.array(means)
    mean = means.mean()
    probabilityRange99Percent = (means.std() * 2.58)/np.sqrt(len(means))
    return mean, probabilityRange99Percent

def getPvalue_twoSampledTtest(sampDistribution1, sampDistribution2):
    '''
    This function returns the p-value. It is the probability of making an error
    when selecting the alternative hypothesis (HA).
    
    HA = the mean of the two distribtuions are different.
    H0 = the mean of the two distributions are the same.
    
    Therefore,
    if p-value <= alpha: accept HA (two distributions are different)
    if p-value > alpha: reject HA (two distributions are the same)
    
    Alpha (significance) is the maximum acceptable probability of making an error
    when selecting the alternative hypotheis.
    alpha=0.05 for 95% confidence selecting HA
    alpha=0.01 for 99% confidence selecting HA
    '''
    t, p = ttest_ind(sampDistribution1, sampDistribution2)
    return p

def getPvalue_oneSampledTtest(sampDistribution, expectedPopulationMean):
    '''
    This function returns the p-value, that is the probability of making an error
    when selecting the alternative hypothesis (HA).
    
    HA = Sample distribution mean is different from the expected value
    H0 = Sample distribution mean is equal to the expected value
    
    Therefore,
    if p-value <= alpha: accept HA (sample distribution's mean is different from the expected value)
    if p-value > alpha: reject HA (sample distribution's mean is equal to the expected value)
    
    Alpha (significance) is the maximum acceptable probability of making an error
    when selecting the alternative hypotheis.
    alpha=0.05 for 95% confidence selecting HA
    alpha=0.01 for 99% confidence selecting HA
    '''
    t, p = ttest_1samp(sampDistribution, expectedPopulationMean)    
    return p



