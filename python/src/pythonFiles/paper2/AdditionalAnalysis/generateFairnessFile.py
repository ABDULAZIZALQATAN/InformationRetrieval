import os
import pandas as pd
import pythonFiles.paper2.AdditionalAnalysis.generateRetFile as genret
import pythonFiles.paper2.AdditionalAnalysis.measureFairness as measure
import pythonFiles.paper2.AdditionalAnalysis.generateCSV as gencsv
import classes.general as gen


def getFileName(line):
    # WAPO,AX,0.4,BM25,25,25,0,0.75,0.471616151,13750,29207300
    # AQ-BM25-UI-300K-C100-AX-fbdocs05-fbterms05-b0.75.res
    parts = line.split(',')
    corpus = parts[0][:2]
    exp = parts[1]
    beta = parts[2]
    terms = '{:02d}'.format(int(parts[4]))
    docs = '{:02d}'.format(int(parts[5]))
    fName = '%s-BM25-UI-300K-C100-%s-fbdocs%s-fbterms%s-b0.75.res' % (corpus,exp,docs,terms)
    outName = '%s' * 5
    outName = '-'.join(outName) % (corpus,exp,beta,docs,terms) + '.csv'
    return [fName , outName]

def generateRetFile (line):
    folder = r'D:\Backup 29-04-2021\2nd Experiment - RM3\AllRes\Bias Measurement'
    [inFile, outFile] = getFileName(line)
    file = folder + '\\' + inFile
    if os.path.isfile(file):
        [corpus,exp,beta,docs,terms] = file.split('-')
        terms = terms.replace('.csv','')
        # docs = getTwoNumbers(docs)
        # terms = getTwoNumbers(terms)
        path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\DocLength Analysis\DocLength Analysis\RetFiles'
        df = genret.getRetrievabilityResults(corpus,exp,0,docs,terms)
        df2 = genret.getRetrievabilityResults(corpus,exp,0.5,docs,terms)
        df = df.merge(df2,'inner','docid')
        df.to_csv(path + '\\' + outFile,index=None)
        df = None
        df2 = None
        print('File Done:', file)

def requiredLine(line,targetCorpus,targetB):
    parts = line.split(',')
    corpus = parts[0][0].upper()
    exp = parts[1]
    beta = parts[2]
    model = parts[3]
    b = parts[6]
    valid = corpus == targetCorpus[0]  and model == 'BM25' and b == str(targetB) and \
            ((exp == 'AX' and beta == '0.4') or (exp == 'RM3' and beta == '0.5'))
    return valid


def processLine(line,group,b):
    parts = line.split(',')
    corpus = parts[0][:2]
    exp = parts[1]
    terms = measure.getTwoNumbers(parts[4])
    docs = measure.getTwoNumbers(parts[5])
    result = [group] + measure.process(group,corpus,exp,docs,terms,b)
    result = line.replace('\n' , ','  + ','.join(result) + '\n')
    return result

def process(corpus,group , b):
    corpus = corpus.upper()
    csvFile = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\CSV\Ex2Ret.csv'
    f = open(csvFile)
    file = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\concat\%s-%s-b%s.csv' % (corpus, group,str(b))
    outf = open(file, 'w', encoding='utf-8')
    header = f.readline()
    additionalHeader = ',group,rel_count_exposure,rel_sum_exposure,size_exposure,grp_exposure\n'
    header = header.replace('\n', additionalHeader)
    outf.write(header)
    for line in f:
        if requiredLine(line, corpus , b):
            newLine = processLine(line, group , b)
            print(newLine)
            outf.write(newLine)
    outf.close()

def getGroupList(corpus):
    file = gencsv.getMainFile(corpus)
    df = pd.read_csv(file)
    result =  list(df.columns.values)
    df = None
    for grp in 'docid rel_sum rel_count length'.split():
        result.remove(grp)
    return result


def main():
    # Generate Fairness File based on input and
    # To merge Main Dataframe and Ret File (to get Retrievability Values )
    # corpus = 'aq'
    # group = 'author TRAILER'
    # groupList = group.split()

    for c in 'a c w'.split():
        groupList = getGroupList(c)
        c = gen.getCorpus(c)
        for grp in groupList:
            for b in [0 , 0.5]:
                process(c,grp , b)
            print('Done' , c)
        print('Done' , c , 'All groups' , b)
if __name__ == '__main__':
    main()