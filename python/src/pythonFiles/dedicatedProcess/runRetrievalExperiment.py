import src.classes.general as gen
import src.classes.bash as sh
import src.pythonFiles.dedicatedProcess.evaluateResults as eval

def getModelLine (model,coefficient):
    # -spl -spl.c $c - -bm25 -bm25.b $b -bm25.k1 1.2
    switcher = {
        'BM25':'-bm25 -bm25.b %s -bm25.k1 1.2',
        'PL2':'-spl -spl.c %s',
        'LMD':'-qld -qld.mu %s',
    }
    result = switcher.get(model,'None')
    return result % coefficient

def  getExpCmd (exp, docs, terms, beta):
#    -rm3 -rm3.fbTerms $fbTerms -rm3.fbDocs $fbDocs -rm3.originalQueryWeight $beta /
#    -axiom -axiom.n $fbDocs -axiom.top $fbTerms -axiom.beta $beta -axiom.deterministic -rerankCutoff 20
    switcher = {
        'ax':'-axiom -axiom.n %d -axiom.top %d -axiom.beta %0.2f -axiom.deterministic -rerankCutoff 20',
        'rm3':'-rm3 -rm3.fbDocs %d -rm3.fbTerms %d -rm3.originalQueryWeight %0.2f'
    }
    result = switcher.get(exp.lower(),'')
    if (result != ''):
        result = result % (docs,terms,beta)
    return result

def printCSV (root ,line):
    file = root + '\Test.csv'
    file = gen.getLinuxPath(file)
    # corpus	qryExpansion	beta	model	fbTerms	fbDocs	RetrievalCoefficient Elapsed
    f = open(file,'a')
    f.write(line)
    f.close()

def runRetrievalExperiment (exp ,docs,terms,beta, corpus,bias,model,coefficient):
    # %index - %qry - %hits - %modelLine - %out
    global ctr
    index = gen.getIndex(corpus)
    if bias:
        qry = '200K'
        hits = '100'
    else:
        qry = '50'
        hits = '1000'
    corpus = gen.getCorpus(corpus)
    qry = '%s/%sXML.qry' % (corpus,qry)
    root = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini'
    root = gen.getLinuxPath(root)
    file = root + '/bash/runRetrieval.sh'
    modelLine = getModelLine(model,coefficient)
    exp = exp.upper()
    if (exp == 'B'):
        exp = 'Baseline'
# def getOutputResName(exp,corpus,model,coefficient,beta,docs,terms):
    out = gen.getOutputResName(exp,corpus,model,coefficient,bias,beta,docs,terms)
    expcmd = getExpCmd(exp, docs, terms, beta)
    out = '~/anserini/revertedIndex/BiasRes/' + out
    f = open(file,'r')
    lines = f.read()
    replacements = {
        '%index':index,
        '%qry':qry,
        '%hits':hits,
        '%out':out,
        '%modelLine':modelLine,
        '%exp':expcmd
    }
    for old,new in replacements.items():
        lines = lines.replace(old,new)
    f.close()
    #     root = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini'
    newFile = file.replace('.sh','New.sh')
    f = open(newFile,'w')
    f.write(lines)
    f.close()
    newFile = newFile.replace(root,'~/anserini')
    t1 = gen.getCurrentTime()
    print(ctr , '- Processing: ',out , ' at :' , t1)
    sh.runBashFileFromPython(newFile)
    t2 = gen.getCurrentTime()
    print('Done: ',out , ' at :' , gen.getCurrentTime())
    elapsed = t2 - t1
    elapsed = gen.elapsedToString(elapsed)
    line = '%s,' * 8
    line = line[:-1]
    file = out.replace('~/anserini',root)
    gainfile = gen.getGainFile(corpus)
    evallist = eval.evaluateResults(file,gainfile,corpus[0],bias)
    line = line % (corpus,exp,beta,model,terms, docs,coefficient,elapsed)
    if (bias):
        l1 = ','.join([line,'0']+evallist[:3]) + '\n'
        l2 = ','.join([line,'0.5']+evallist[3:]) + '\n'
        line = l1 + l2
    else:
        line += ','.join(evallist)
    print(ctr,line)
    ctr += 1
    printCSV (root , line)

def runExperiments1():
    # exp ,docs,terms,beta, corpus,bias,model,coefficient
    global ctr
    ctr = 1
    exp = 'ax' # ax - rm3 - b
    docs = 10 # default - 10
    terms = 10 # default - 10
    beta = 0.5
    corpus = 'a'
    bias = True
    model = 'BM25' # BM25 - PL2 - LMD

    # Baseline
    for corpus in 'a c w'.split():
        coefficient = 0.1
        while coefficient <= 1:
            runRetrievalExperiment(exp ,docs,terms,beta, corpus,bias,model,coefficient)
            coefficient += 0.1

if __name__ == '__main__':
    runExperiments1()