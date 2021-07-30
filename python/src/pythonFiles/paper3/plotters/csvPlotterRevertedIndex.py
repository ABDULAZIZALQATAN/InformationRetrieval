# This Module is For Plotting Check Bigrams Charts
import python.src.pythonFiles.plotters.csvPlotterGen as pltgen
import pandas as pd
import matplotlib.pyplot as plt
import classes.general as gen

# Import Module in G Drive

# drivePath = '/content/gdrive'
# modPath = '/My Drive/Colab Notebooks'
# from google.colab import drive
# drive.mount (drivePath )
# import sys
# sys.path.append(drivePath + modPath)
# import csvPlotterGeneral as gen

"""
 *** Start Colab Form ***
 Input Data
 @title Plot Bias & Performance Experiments
"""
inCorpus = "WAPO"  # @param ["AQUAINT", "CORE17", "WAPO","All"]
inModel = "BM25"  # @param ["BM25", "LMD", "PL2" , "All"]
## @markdown The Number of values to plot - 0 for all
# PLotValuesCount = 0  # @param {type:"slider", min:0, max:16, step:1}
## @markdown Use Predefined ticks from ticks.csv files
##PredefinedTicks = "No"  # @param ["Yes", "No"]
inBase = 'fbTerms' # @param ["fbDocs", "fbTerms",'beta','']
inXAxis = "TrecMAP"  # @param ["fbTerms",'fbDocs',"TrecMAP",'TrecNDCG' , "CWLMAP",'CWLRBP0.4','CWLRBP0.6','CWLRBP0.8','CWLP10','Time']
inYAxis = "G0"  # @param ["G0", "G0.5","TrecMAP",'TrecNDCG','TrecP10',"CWLMAP",'CWLRBP0.4','CWLRBP0.6','CWLRBP0.8']

# *** End Colab Form ***

GLegend = ''

def isBias ():
    return inYAxis.startswith('G')

def addBCriteria(measure,criteria):
    group = pltgen.getGroup(measure)
    if group == 'ret':
        criteria['RetrievabilityB'] = float(measure.replace('G', ''))
    return criteria

def getDataFrame(measure,criteria):
    exnum = 3
    file = pltgen.getFile(measure,exnum)
    df = pd.read_csv(file, ',')
    localCriteria = criteria.copy()
    localCriteria = addBCriteria(measure,localCriteria)
    df = pltgen.filterDf(df, localCriteria)
    df = pltgen.sortDf(df,exnum)
    return df


def setTicks():
    # Set Ticks
    ticks = pltgen.getTicksByAxis(inXAxis)
    plt.xticks(ticks)
    #
    ticks = pltgen.getTicksByAxis(inYAxis)
    plt.yticks(ticks)

def showFigure():
    global GLegend
    # outputFile
    # setTicks()
    # Set Legend
    line = GLegend
    plt.legend(title=line, ncol=2)

    [fFamily, fSize, fWeight] = pltgen.getFont()
    # Set Title
    # line = "%s - %s - C = 1 \n Over fbTerms[5,10,20] fbDocs=10" % (inCorpus, inModel)

    cof = 'b = 0.75' if inModel == 'BM25' else 'C = 1'
    line = "%s - %s - %s - \u03B2 = 0.25 - Expansion = REV\nOver fbTerms[05:05:30]" % (inCorpus, inModel,cof)

    # line = "%s - %s - C = 1 - \u03B2 = 0.25 \nTime Over fbTerms [30:05:50]" % (inCorpus, inModel)

    # line += '\n Removed Original Query \n Keeping the weighted queries'

    plt.title(line,size=fSize,family=fFamily,weight=fWeight)
    # Set Axis Labels
    line = pltgen.getAxisLabel(inXAxis)
    # line = 'Time'
    plt.xlabel(line,size=fSize,family=fFamily,weight=fWeight)
    line = pltgen.getAxisLabel(inYAxis)
    plt.ylabel(line,size=fSize,family=fFamily,weight=fWeight)

    plt.show()

def main():
    global GLegend
    criteria = {
        'Df>':10,
        'beta':0.25,
        'corpus':inCorpus,
        'model':inModel
        # 'fbTerms->': 29
    }
    if isBias():
        criteria['fbTerms-<'] = 31
        criteria['fbDocs-<'] = 31
        legendRange = range(5, 35, 5)
        GLegend = 'fbDocs'
    else:
        legendRange = range(5, 55, 5)
        GLegend = 'fbDocs' if inXAxis == 'fbTerms' else 'fbTerms'

    dfY = getDataFrame(inYAxis,criteria)
    if (pltgen.isKeyLabel(inXAxis) or pltgen.getGroup(inXAxis) == pltgen.getGroup(inYAxis)) :
        dfX = dfY
    else:
        dfX = getDataFrame(inXAxis,criteria)

    # marker = pltgen.getMarker(str(5))
    for item in legendRange:
        criteria = {GLegend:item}
        xValues = pltgen.filterDf(dfX,criteria)[inXAxis]
        ycol = 'G' if isBias() else inYAxis
        yValues = pltgen.filterDf(dfY,criteria)[ycol]
        marker = pltgen.getMarker(str(item))
        # plt.plot(xValues, yValues, marker=marker, markersize=8)
        plt.plot(xValues, yValues, marker=marker, markersize=8, label=item)
    pltgen.drawBaseLine(plt,inXAxis,inYAxis,inCorpus,2)
    showFigure()

    print('Done')

if __name__ == '__main__':
    main()