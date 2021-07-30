import xml.dom.minidom as dm
import os
import pythonFiles.dedicatedProcess.CollectionIterator.WAPOIterator as wa
import pandas as pd

def getHeader():
    # Docdata - 8 values
    line = 'docid,doc.copyright-holder,doc.copyright-year,descriptor,types_of_material,taxonomic_classifier,general_descriptor,date_publication,'
    # Title
    line += 'title,'
    # Author
    line += 'author,'
    # MetaData - 11 Value
    line += 'slug,publication_day_of_month,publication_month,publication_year,publication_day_of_week,dsk,print_page_number,print_section,print_column,online_sections,banner'
    line += '\n'
    return line

def getTextByTag (tag):
    nodelist = tag.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    result = ''.join(result)
    return result

def getTextByTagName (xml,tagName):
    tags = xml.getElementsByTagName(tagName)
    result = '' if (len(tags) < 1) else getTextByTag(tags[0])
    return result

def getByTag_Attribute(xml , tagName,attribute):
    tag = xml.getElementsByTagName(tagName)
    return '' if (len(tag) < 1) else getByAttribute(tag[0], attribute)

def getByAttribute (tag, attribute):
    return tag.attributes[attribute].value

def getTitle(xml):
    # Retrieved Fields - title
    tagName = 'title'
    result = getTextByTagName(xml,tagName)
    return [result]

def getAuthor(xml):
    tagName = 'byline'
    result = getTextByTagName(xml, tagName)
    result = result.strip()
    initial = result[:2].lower().strip()
    if (initial == 'by'):
        result = result[3:]
    return [result]

def getMeta (xml):
    '''
    Retrieved Fields : 11 Fields
    slug publication_day_of_month - publication_month - publication_year
    publication_day_of_week - dsk - print_page_number - print_section
    print_column - online_sections - banner
    '''
    tagName = 'meta'
    tags = xml.getElementsByTagName(tagName)
    targetTagNames = 'slug publication_day_of_month publication_month publication_year publication_day_of_week dsk print_page_number print_section print_column online_sections banner'.split()
    result = {}
    # Initialize Names
    for name in targetTagNames :
        result[name] = ''

    for item in tags:
        name = getByAttribute(item, 'name')
        if (result.__contains__(name)):
            value = getByAttribute(item, 'content')
            result[name] += value + ' '
    result = list(result.values())
    return result

def getDocdata (xml):
    '''
    Retrieved Fields 8 Values :
    doc-id - doc.copyright-holder - doc.copyright-year - descriptor
    types_of_material - taxonomic_classifier - general_descriptor - date_publication
    '''
    sep = '|'
    tagName = 'doc-id'
    docid = getByTag_Attribute(xml,tagName,'id-string')
    tagName = 'doc.copyright'
    copyrightHolder = getByTag_Attribute(xml,tagName,'holder')
    copyrightYear = getByTag_Attribute(xml,tagName,'year')
    # descriptor - types_of_material - taxonomic_classifier - general_descriptor
    classifiers = xml.getElementsByTagName('classifier')
    typeResults = {}
    hdrList = 'descriptor types_of_material taxonomic_classifier general_descriptor'.split()
    for item in hdrList:
        typeResults[item] = ''
    # [descriptor,material,tax,genDescriptor] = [''] * 4
    for item in classifiers:
        aType = getByAttribute(item,'type')
        if (typeResults.__contains__(aType)):
            value = getTextByTag(item) + sep
            typeResults[aType] += value

    typeResults = list(typeResults.values())
    for i in range(len(typeResults)):
        if (typeResults[i] != ''):
            typeResults[i] = typeResults[i][:-1]

    date_publication = getByTag_Attribute(xml,'pubdata','date.publication')

    result = [docid,copyrightHolder,copyrightYear] + typeResults + [date_publication]
    return result

def processFile (file):
    xml = dm.parse(file)
    result = getDocdata(xml)
    result += getTitle(xml)
    result += getAuthor(xml)
    result += getMeta(xml)

    xml = None
    for i in range (len(result)):
        result[i] = wa.filterTerm(result[i])

    print('Processed ', file)
    return [','.join(result) + '\n']

def iterateFiles (folder):
    items = os.listdir(folder)
    result = []
    for item in items:
        fullItem = folder + '/' + item
        if os.path.isdir(fullItem):
            result += iterateFiles(fullItem)
        else:
            result +=  processFile(fullItem)
    return result

def unionDf ():
    folder = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\years'
    outFile = folder + r'\AllCORE17Fields.csv'
    outf = open(outFile,'w',encoding='utf-8')
    line = getHeader()

    outf.write(line)
    for i in range(1987,2008):
        file = folder + r'\CORE17Fields%s.csv' % i
        f = open(file,'r',encoding='utf-8')
        f.readline() # Skip Header
        for line in f:
            outf.write(line)
            print('Moved: ' , line)
        f.close()
    outf.close()

def main():
    # for year in range(1987,2008):
    #     processYear(year)
    # file = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\Sample Files\1622642 Sample Core17.xml'
    # x = processFile(file)
    # print(x)
    unionDf()
    print('Done')


def processYear(year):
        year = str(year)
        print('Processing Year : %s\n' % year)
        path = r'D:\Data Collections\CORE17\data\%s' % year
        outFile = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\2nd Experiment - RM3 VS AX\Faieness Measurement\years\CORE17Fields%s.csv' % year
        lines = iterateFiles(path)
        f = open(outFile,'w',encoding='utf-8')
        line = getHeader()
        f.write(line)
        for line in lines:
            f.write(line)
        f.close()
        print('Done Year : %s\n' % year)

if __name__ == '__main__':
    main()