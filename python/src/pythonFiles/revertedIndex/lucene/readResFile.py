import python.src.classes.trec  as trec
import python.src.classes.CWL as cwl
import python.src.classes.clsRetrievabilityCalculator as rc
import python.src.classes.general as gen

def evaluateResults(resFile,gainFile,corpus,bias):
    # Use trec method in Eval Class to evaluate The Final Results File

    if bias:
        result = []
        for b in [0,0.5]:
            c = 100
            temp =  rc.calculate(resFile,b,c,corpus, '')
            result += [str(x) for x in temp]
    else:
        trecResults =  trec.getTrecData(resFile,gainFile) # map , bpref , P.10 , ndcg'
        cwlResults = cwl.getMetricsValues(resFile,gainFile) # [Map,NDCG, P10,R4, R6, R8]
        result = trecResults + cwlResults
        # result = trecResults
    return result



def readResFile(resFile,corpus,bias):
    gainFile = gen.getGainFile(corpus)
    eval = evaluateResults(resFile,gainFile,corpus,bias)
    print(eval)


def main():
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\revertedIndex\BiasRes\\'
    resFile = 'REV-WA-BM25-b0.75-beta0.25-docs10-terms15.res'
    test =  r'D:\Backup 29-04-2021\3rd Experiment - Reverted Index\BiasRes\Test.res'


    corpus = resFile.split('-',2)[1][0]
    # corpus = gen.getCorpus(corpus[0])
    resFile = folder + resFile
    resFile = gen.getLinuxPath(resFile)
    test = gen.getLinuxPath(test)
    bias = True
    gen.copyFile(resFile, test)

    readResFile(resFile,corpus,bias)
if __name__ == '__main__':
    main()