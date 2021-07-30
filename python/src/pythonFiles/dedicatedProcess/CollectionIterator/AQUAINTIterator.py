import os
import pythonFiles.dedicatedProcess.CollectionIterator.WAPOIterator as wa
import pandas as pd

def extractValue (line,tag):
    line = line.replace(tag,'')
    tag = tag.replace('<','</',1)
    line = line.replace(tag,'').strip()

    # Filter Value
    line = wa.filterTerm(line)
    return line

def extractFields(xml):
    mainTags = '<DOCNO> <DOCTYPE> <DATE_TIME> <SLUG> <HEADLINE> <TEXT> <TRAILER>'.split()
    result = ['None'] * (len(mainTags) - 1) # reset output values
    tags = mainTags.copy()
    readTrailer = False
    readAuthor = False
    for line in xml.split('\n') :
        # ctr = 0
        line = line.strip()
        if (readTrailer):
            value = line
            value = wa.filterTerm(value)
            result[5] = value
            break
        elif (readAuthor and line[:3].lower() == 'by ' ):
            value = line[3:]
            value = wa.filterTerm(value)
            result[4] = value
            readAuthor = False
        else:
            for i in range(len(tags)):
                if line.startswith(tags[i]):
                    currentTagIndex = mainTags.index(tags[i]) # index of current Tag
                    if (currentTagIndex < 4):
                        # <DOCNO> <DOCTYPE> <DATE_TIME> <SLUG>
                        value = extractValue(line , tags[i])
                        result[currentTagIndex] = value
                        tags.remove(tags[i])
                        break
                    elif (currentTagIndex == 4): # <HEADLINE>
                        readAuthor = True
                        tags.remove(mainTags[currentTagIndex])
                        break
                    elif (currentTagIndex == 5): # <TEXT>
                        readAuthor = False
                        tags.remove(mainTags[currentTagIndex])
                        break
                    elif (currentTagIndex == 6 ):
                        readTrailer = True
                        break
    result = [result[0]] +  result[-2:]
    return ','.join(result)

# def extract_author(xml):
#     # Extract DocNo and author
#     tag = '<DOCNO> <HEADLINE> <TEXT> <TRAILER>'.split()
#     result = ['None'] * 3
#     stage = 1
#     readTrailer = False
#     for line in xml.split('\n') :
#         # ctr = 0
#         line = line.strip()
#         if readTrailer :
#             # Trailer
#             value = line.strip()
#             value = wa.filterTerm(value)
#             result[2] = value
#             break
#         if line.startswith(tag[0]) and stage == 1 :
#             # DOCNO
#             # NYT19980601.0541
#             value = extractValue(line , tag[0])
#             value = wa.filterTerm(value.strip())
#             result[0] = value
#             stage += 1
#         elif line.startswith(tag[1]) and stage > 1:
#             stage += 1
#         elif line[:3].lower() == 'by ' and stage == 3:
#             # Author
#             value = line[2:]
#             value = wa.filterTerm(value)
#             result[1] = value
#             stage += 1
#         elif line.startswith(tag[2]) and stage == 3:
#             stage+=1
#         elif line.startswith(tag[3]):
#             readTrailer = True
#
#     return ','.join(result)

def processFile (file):
    f = open(file, 'r')
    files = ''.join(f.readlines())
    files = files.split('</DOC>\n')
    lines = []
    for xml in files:
      if (xml != ''):
        line =  extractFields(xml)
        # line = extract_author(xml)
        lines.append(line)
        print('Added ',line)
    f.close()
    return '\n'.join(lines) + '\n'

def iterateGroup (groupPath,yearRange,outFile):
    f = open(outFile, 'a')
    for year in yearRange:
        folder = '%s\%d' % (groupPath, year)
        files = os.listdir(folder)
        for file in files:
            file = '%s\%s' % (folder,file)
            lines = processFile(file)
            f.write(lines)
    f.close()

def iterateFiles(collectionFolder , outFile):
    # NYT Path
    f = open(outFile,'w')
    line = 'DOCNO,DOCTYPE,DATE_TIME,SLUG\n'
    f.write(line)
    f.close()
    groupPath = collectionFolder + r'\TREC-Aquaint\disk1\nyt'
    yearRange = range(1998,2001)
    iterateGroup(groupPath,yearRange,outFile)
    folder = collectionFolder + r'\TREC-Aquaint\disk2'
    groupPath = folder + r'\apw'
    yearRange = range(1998, 2001)
    iterateGroup(groupPath,yearRange,outFile)
    groupPath = folder + r'\xie'
    yearRange = range(1996, 2001)
    iterateGroup(groupPath, yearRange, outFile)
    print('All Done')

def removeDuplicates (file):
    df = pd.read_csv(file)
    df = df.drop_duplicates()
    df.to_csv(file)

def main():
    outFile = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\AQUAINTNew.csv'
    collectionFolder = r'D:\Data Collections'
    iterateFiles(collectionFolder,outFile)
    # removeDuplicates(outFile)
    # file = r'C:\Users\kkb19103\Desktop\19980601_NYT.txt'
    # processFile(file)
    print('Done')
if __name__ == '__main__':
    main()