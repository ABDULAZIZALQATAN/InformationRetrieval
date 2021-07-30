import src.classes.trec  as trec
import src.classes.CWL as cwl
import src.classes.clsRetrievabilityCalculator as rc

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