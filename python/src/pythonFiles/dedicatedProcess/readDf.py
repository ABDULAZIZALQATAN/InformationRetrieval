import pandas as pd
import src.classes.general as gen

def printResults (df,corpus,leastLimit):
    corpus = gen.getCorpus(corpus)
    print('Corpus :', corpus, '   Limit:', leastLimit)
    print('Count:', len(df))
    # print(df.head)

def getDf(corpus,leastLimit):
    path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\3rd Experiment - Reverted Index\df Comparison'
    file = path + '\df%s.txt' % corpus
    df = pd.read_csv(file, sep='\t', names=['term', 'df', 'total', 'score'])
    criteria = df['df'] >= leastLimit
    df = df[criteria]
    return df

def main():
    leastLimit = 6
    corpus = 'a'
    for corpus in 'a c w'.split():
        for leastLimit in [5,6]:
            df = getDf (corpus,leastLimit)
            printResults(df,corpus,leastLimit)

if __name__ == '__main__':
    main()