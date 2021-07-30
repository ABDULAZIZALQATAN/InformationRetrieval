def findMissingQueries(resFile):
    # Find Missing sequence numbers in queryIDs of Res File
    f = open(resFile,'r')
    i = 1
    ctr = 0
    f.readline()
    for line in f:
        # qryID = line.split(' ',1)[0]
        qryID = line.split(',')[1]
        qryID = int(qryID)
        while(qryID > i):
            i+=1
            if (qryID > i):
                print(i,'is Missing')
                ctr += 1
    print('Total Missing',ctr)
    f.close()

if __name__ == '__main__':
    resFile = ''
    findMissingQueries(resFile)