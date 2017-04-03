#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 16:49:24 2017
@author: zhenshan
"""
import pandas as pd
import numpy as np
import util
import SentenceSegmentation
#visulization
import matplotlib.pyplot as plt



def FeatureDF(ecogTrain, sentenceTrain, nodeIdx, frequency, featureList, rawIntervals):
    '''Generate the features for the selected frequencies and nodes'''
    
    frequencyName = ['Delta', 'Theta', 'Alpha' ,'Beta' ,'Low Gamma', 'High Gamma']
    freqIdx = [frequencyName.index(freq) for freq in frequency]
    timeIntervals = SentenceSegmentation.AlignmentPoint(rawIntervals)
    
    featureDF = pd.DataFrame()
    nameInd = 0
    for nodeIdx_ in nodeIdx:
        for freqIdx_ in freqIdx:
            ecogSlice = util.EcogSlicing(ecogTrain, nodeIdx_, freqIdx_)
            subFeatureDF = FeatureDF_Helper(featureList, sentenceTrain, ecogSlice, timeIntervals)
            if nameInd == 0:
                featureDF['phone name'] = subFeatureDF['phone name']
                
            colname = [str(nodeIdx_) + " " + frequency[freqIdx_] + " " + feat for feat in featureList]
            featureDF[colname] = subFeatureDF.drop(['phone name'], axis = 1)
        
    
    return featureDF.dropna()# Remove observations with nan


def FeatureDF_Helper(featureList, sentences, ecogSlice, timeIntervals):
    '''Generate features for unit frequency&node series'''
    
    colName = ["phone name"]
    for i in featureList: colName.append(i) 
    
    totalFeatureDf = pd.DataFrame(columns = colName)
    for sen in sentences:
        '''Create the feacture matrix for each sentence'''
        sentenceAdj = util.SentenceAdjustment(sen)
        # Ecog data
        ecogSeries = ecogSlice[sentenceAdj]
        # Ecog's phone split point
        timeInterval = timeIntervals[sentenceAdj] 
        phoneSplits = SentenceSegmentation.SplitPoint(timeInterval, len(ecogSeries))
        # Ecog's phone interval 
        phoneSegmentation = SentenceSegmentation.NeuralSignalSegmentation(phoneSplits, ecogSeries, timeInterval)
        # Feature matrix creation
        sentenceFeatureDf = pd.DataFrame(columns = colName)
        phoneIdx = 0
        for word in phoneSegmentation:
            wordSegmentation = phoneSegmentation[word]
            for phone in wordSegmentation:
                obsValue = FeatureGenerator(phone["signalData"], featureList)
                obsValue.insert(0, phone["phone"])
                sentenceFeatureDf.loc[phoneIdx] = obsValue
                phoneIdx += 1
        totalFeatureDf = totalFeatureDf.append(sentenceFeatureDf)
        
    return totalFeatureDf


def FeatureGenerator(dataSeries, featureList):
    '''Generate features for unit phone series'''
    if 'mean' in featureList:
        if len(dataSeries) != 0:
            mean_ = float(Mean(dataSeries))
        else:
            mean_ = None
    else: 
        mean_ = None
    
    return [mean_]


def Mean(dataSeries):
    return np.mean(dataSeries)


def FeatureVisualCheck(featureDF_):
    '''Checking scaling accuracy: first sil phone mean is 0'''
    featureValue = featureDF_.ix[:,1:featureDF_.shape[1]].apply(np.mean, axis = 1)
    phoneList = list(featureDF_.ix[:,0])
    
    scalingSilList = list()
    
    for idx, val in enumerate(phoneList):
        if idx + 1 < len(phoneList):
            if phoneList[idx + 1] == 'sil' and val == 'sil':
                scalingSilList.append(featureValue.iloc[idx])   
    
    plt.hist(scalingSilList)
    plt.title("Gaussian Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    
    print(pd.DataFrame(scalingSilList).describe())