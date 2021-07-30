# !pip install pingouin
# General Functions - Important to Run First
# Read Google Files
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import pingouin as pg
# from google.colab import drive
# drive.mount('/content/drive', force_remount=True)


rootFolder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\\'

def read_all_fields (corpus):
    corpus = corpus[0].upper()
    corpus = getCorpus(corpus)
    # AQUAINTFields
    memory = False
    fileName = rootFolder + corpus + 'Fields.csv'
    df = pd.read_csv(fileName,low_memory=memory)
    return df

def read_ret_values(corpus):
    corpus = getCorpus(corpus[0])[:2]
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\RetFiles\\'
    # AQ-AX-0.4-05-05.csv
    fileName =  '%s%s-AX-0.4-05-05.csv' % (folder,corpus)
    df = pd.read_csv(fileName)
    return df

def getCorpus (c):
    switcher = {
        'A':'AQUAINT' ,
        'C': 'CORE17' ,
        'W': 'WAPO'
    }
    return switcher.get(c[0].upper(),'')

def read_performance_file():
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\CSV'
    fileName = folder + '\\Ex2Per.csv'
    df = pd.read_csv(fileName)
    return df

def read_fairness_file ():
    fileName = rootFolder + 'Fairness.csv'
    df = pd.read_csv(fileName)
    return df

def setTicks(aplt):
    ticks = np.arange(0,0.8,0.1)
    aplt.yticks(ticks)
    print('Here')

def showFigure(title , xLabel , yLabel):
    [fSize, fWeight] = [17,500]
    plt.title(title,size=fSize,weight=fWeight)

    # setTicks(plt)
    # ticks = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
    ticks = np.arange(0.01,0.065 , 0.005)
    plt.yticks (ticks)
    # Set Axis Labels
    plt.xlabel(xLabel,size=fSize,weight=fWeight)
    plt.ylabel(yLabel,size=fSize,weight=fWeight)
    plt.show()

def printColumns(df):
    cols = df.columns.values
    for i in cols :
        print(i)

def compute_percent(v):
    total_v = np.sum(v)
    percent_v = np.divide(v , total_v)

    return percent_v

def compute_fairness_score(a, b):
    c = np.subtract(a,b)  # substract
    c = np.power(c,2) # square
    c = np.sum(c) # sum
    score = np.power(c, 0.5) #square root
    return score