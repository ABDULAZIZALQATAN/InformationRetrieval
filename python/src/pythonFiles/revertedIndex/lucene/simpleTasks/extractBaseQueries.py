import src.pythonFiles.dedicatedProcess.isStopword as iss
def extractBaseQueries (inFile , outFile , df):
    # Extract Base Queries given specific df limit
    # Input Format is Anserini Format (DF is second Column)
    f = open(inFile,'r',encoding='utf-8')
    f2 = open(outFile,'w',encoding='utf-8')
    outLine = 'qryID\tqry\n'
    f2.write(outLine)
    seq = 1
    i = 1
    for line in f:
        parts = line.split('\t')
        numDf = int(parts[1])
        term = parts[0]

        if (numDf > df):
            if (iss.validTerm(term)):
                outLine = '%d\t%s\n' % (seq , parts[0])
                f2.write(outLine)
                seq += 1
            else:
                print(i,term)
                i+=1
    f.close()
    f2.close()

if __name__ == '__main__':
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources\AQUAINT\\'
    inFile = folder + 'df-Original-A.txt'
    df = 10
    outFile = folder + 'df-Original-A-out.txt'
    extractBaseQueries (inFile , outFile , df)