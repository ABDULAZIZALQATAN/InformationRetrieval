import isStopword as iss
import pandas as pd

def filterBigramFile (df):

    criteria = df['score'] >= 0
    df = df[criteria]
    df['criteria'] = df.apply( lambda row : iss.validTerm(row['w1']) and iss.validTerm(row['w2']) , axis = 1)
    df = df[df['criteria']]
    df.drop('criteria',inplace=True,axis=1)
    return df

def resortBigram (df):
    # path = r'C:\Users\kkb19103\Desktop\AQ.out'
    df.drop('seq',axis=1,inplace=True)
    df.sort_values(by='score',ascending=False,inplace=True)
    return df


def readDf (path):
    names = 'seq w1 w2 f1 f2 fboth score'.split()
    df = pd.read_csv(path,sep=' ',names=names)
    return df

def printBigrams(df, path):
    df = df.reset_index()
    df = df.rename(columns={"index":"seq"})
    df['seq'] = df.index + 1
    # df.to_csv(path,sep=' ',index=None)
    return df

def printQry(df,qryFile):
    df = df['seq w1 w2'.split()]
    df.to_csv(qryFile,' ',index=None,header=None)

if __name__ == '__main__':
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources\WAPO\BigramOut'
    inpath = folder + r'\bigram Before Filter.out'
    outpath = folder + r'\bigram After Filter.out'
    qryFile = folder + r'\200K.qry'
    pd.options.mode.chained_assignment = None  # default='warn'


    df = readDf(inpath)
    df = filterBigramFile(df)
    df = resortBigram(df)
    df = df.head(2 * 100 * 1000)
    df = printBigrams (df, outpath)
    printQry(df,qryFile)
    print('Done Sucessfully')