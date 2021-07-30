'''
Input Format :
QryID - Qry

Output Format
---------------------------------------
<top>
<num> Number: QryID </num>
<title>
Query</title>
<desc>

</desc>
<narr>

</narr>
</top>

-----------------------------------
'''
def generateXMLTopics(sourceFile , destFile):
    sep = '\t'
    XMLFormat =    '<top>\n' + \
                  '<num> Number: #qryid </num>\n'  + \
                  '<title>\n#query\n</title>\n' + \
                  '<desc>\n\n</desc>\n<narr>\n\n</narr>\n</top>\n'

    en = 'utf-8'
    fSource = open(sourceFile,'r',encoding=en)
    fDest = open(destFile,'w',encoding=en)
    # fSource = open(sourceFile, 'r')
    # fDest = open(destFile, 'w')
    # fSource.readline()
    for line in fSource:
        [qryid,qry] = line.replace('\n','').split(sep)
        outLine = XMLFormat.replace('#qryid',qryid).replace('#query',qry)
        fDest.write(outLine)
    fSource.close()
    fDest.close()
    # print('Generating XML Queries is Done')

if __name__ == '__main__':
    # AQUAINT - WAPO - CORE17
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources\WAPO\\'
    sourceFile = folder + '200K.qry'
    # destFile = folder + '\WA-BaseQueries-100KXML.qry'
    destFile = sourceFile.replace('.qry','XML.qry')
    generateXMLTopics(sourceFile,destFile)