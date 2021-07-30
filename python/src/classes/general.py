from datetime import datetime
import shutil as shu

def printCurrentTime(title):
    result = timeToString(getCurrentTime())
    print(title , ": date and time =", result)
    return result

def getCurrentTime():
    return datetime.now()

def timeToString (time):
    result = time.strftime("%d/%m/%Y %H:%M:%S")
    return result

def elapsedToString (elapsed):
    hours, remainder = divmod(elapsed.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    format = '%02d:' * 3
    format = format[:-1]
    return format % (hours, minutes,seconds)

def getCorpus(c):
    switcher = {
        'A': 'AQUAINT',
        'C': 'CORE17',
        'W': 'WAPO'
    }
    return switcher.get(c.upper())

def getModelCoefficient(model):
    switcher = {
        'BM25': 'b',
        'PL2': 'c',
        'LMD': 'mu'
    }
    return switcher.get(model)

def getQryExpansion(c):
    switcher = {
        'A': 'AX',
        'B': 'Baseline',
        'R': 'RM3'
    }
    return switcher.get(c.upper())

def getResHeader():
    return ['qryID','dum','docid','rank','score','tag']

def getGainFile(c):
    # switcher = {
    #     'A': 'Aquaint-AnseriniQrel.qrel',
    #     'C': '307-690.qrel',
    #     'W': 'qrels.core18.txt'
    # }
    # result = '~/trec_eval/Qrels/' + switcher.get(c[0].upper())

    corpus = getCorpus(c[0])
    # C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\Queries\standardQueries\CORE17
    result = r'~/resource/%s/%s.qrel' % (corpus,corpus)
    return result

def copyFile (src,dest):
    # copyFile(src,dest)
    shu.copy2(src,dest)

def getLinuxPath (path):
    # Windows Path : C:\Users\kkb19103\Desktop\new\data
    # Linux Path : /mnt/c/Users/kkb19103/Desktop/new/data
    replacements = {
        'D:':'/mnt/d',
        'C:':'/mnt/c',
        '\\':'/'
        # ' ':'\ '
        # '\\':'\\'
    }
    result = path
    for key , val in replacements.items():
        result = result.replace(key,val)
    return result

def getIndex (corpus):
    switcher = {
        'A' : 'lucene-index.robust05.pos+docvectors+rawdocs',
        'C' : 'lucene-index.core17.pos+docvectors+rawdocs',
        'W': 'lucene-index.core18.pos+docvectors+rawdocs'
    }
    result = switcher.get(corpus.upper(),'None')
    return result

def getOutputResName(exp,corpus,model,coefficient,bias,beta,docs,terms):
    corpus = corpus[:2]
    qry = '200K' if bias else '50'
    modelCoefficient = getModelCoefficient(model)
    result = '%s-%s-%s-%s%1.1f-%s-beta%0s-docs%02d-terms%02d.res' % \
             ( corpus , model.upper() , exp.upper() , modelCoefficient, coefficient,qry, str(beta), docs, terms)
    return result