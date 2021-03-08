import numpy
from numpy import cov, std
from scipy.stats import rankdata


def spearman_index(target, predicted):
    '''
    Compute the correlation between the given value
    :param target: gold value
    :param predicted: my value
    :return: value of the spearman's index
    '''
    target = numpy.array(target).astype(numpy.float)
    predicted = numpy.array(predicted).astype(numpy.float)
    return cov(rankdata(target), rankdata(predicted))[0][1] / (std(rankdata(target)) * std(rankdata(predicted)))


def pearson_index(target, predicted):
    '''
        Compute the correlation between the given value
        :param target: gold value
        :param predicted: my value
        :return: value of the pearson's index
    '''
    target = numpy.array(target).astype(numpy.float)
    predicted = numpy.array(predicted).astype(numpy.float)
    return cov(target, predicted)[0][1] / (std(target)*std(predicted))