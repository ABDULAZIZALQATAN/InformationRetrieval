def extractTopicListFromXML (xmlQryFile):
    numDef =  '<num> Number:'
    titleDef = '<title> '
    f = open(xmlQryFile,'r')
    outfName = xmlQryFile.replace('XML.qry','.qry')
    outf = open(outfName,'w')
    for line in f:
        if (line.startswith(numDef)):
            num = line.replace(numDef,'').strip()
        elif (line.startswith(titleDef)):
            title = line.replace(titleDef,'').strip()
            outLine = '%s %s\n' % (num,title)
            outf.write(outLine)
    f.close()
    outf.close()

if __name__ == '__main__':
    xmlFile = ''
    extractTopicListFromXML(xmlFile)