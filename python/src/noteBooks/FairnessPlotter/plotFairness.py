import src.noteBooks.FairnessPlotter.General as fgen
import matplotlib.pyplot as plt

# Parameters
#@title Plot Results By fbTerms or fbDocs
group_corpus = "SLUG-A" #@param ['DOCTYPE-A', 'DATE_TIME-A', 'SLUG-A', 'author-A', 'TRAILER-A', 'doc.copyright-holder-C', 'doc.copyright-year-C', 'descriptor-C', 'types_of_material-C', 'taxonomic_classifier-C', 'general_descriptor-C', 'date_publication-C', 'title-C', 'author-C', 'slug-C', 'publication_day_of_month-C', 'publication_month-C', 'publication_year-C', 'publication_day_of_week-C', 'dsk-C', 'print_page_number-C', 'print_section-C', 'print_column-C', 'online_sections-C', 'banner-C', 'author-W', 'pubDate-W', 'kicker-W', 'byLine-W']
exp = "AX" #@param ["RM3", "AX"]
baseField = "fbTerms" #@param ["fbTerms", "fbDocs"]
b = 0 #@param ["0", "0.5"] {type:"raw"}
xField = "TrecMAP" #@param ["fbTerms", "fbDocs",'TrecMAP','TrecBref','TrecP10','TrecNDCG','CWLMAP','CWLNDCG','CWLP10','CWLRBP0.4','CWLRBP0.6','CWLRBP0.8']
yField = "rel_sum" #@param ["rel_sum", "rel_count", "size", "grp"]

'''
Groups :
AQUAINT : DOCTYPE - SLUG
CORE17 : 

'''

# Main
def main():
    parts = group_corpus.split('-')
    group = parts[0]
    corpus = fgen.getCorpus(parts[1])
    if (baseField == xField):
        print('Error : Base Field Must not Equal x Field')
    else:
        plotDf (corpus , group, exp , b ,  xField , yField)

def add_performance_df(df):
    df_per = fgen.read_performance_file()
    linker = list (df_per.columns[:7])
    df = df.merge(df_per,'inner', on=linker)
    return df

def plotDf (corpus , group ,exp , b ,  xField , yField):
    yField += '_exposure'
    # Get Main Df
    df = fgen.read_fairness_file()
    # Initial Filter
    corpus = fgen.getCorpus(corpus) # A = AQUAINT , C = CORE17 , W = WAPO
    criteriaList = {
        # 'corpus' : corpus ,
        'qryExpansion': exp ,
        'group' : group ,
        'RetrievabilityB' : b
    }

    criteria = df['corpus'] == corpus
    for key , value in criteriaList.items():
        criteria &= df[key] == value

    df = df[criteria]

    # Shall we merge performance DataFrame ?
    if (xField not in ['fbTerms','fbDocs']):
        df = add_performance_df(df)

    # Iterate by Base (fbDocs or fbTerms)
    # baseFld = 'fbTerms' if xField == 'fbDocs' else 'fbDocs'
    vBaseRange = range(5,35,5) # base range
    # vBaseRange = [5]

    for item in vBaseRange:
        criteria = df[baseField] == item
        # Extract sub DataFrame
        dfTemp = df[criteria]
        x = dfTemp[xField]
        y = dfTemp[yField]
        lbl = '%s-%s' % (exp,'{:02d}'.format(item))
        plt.plot (x,y,label=lbl , marker = 'X' , markersize=10)

    title = '%s - %s - %s - Base:%s\n%s Vs %s' % (corpus,exp, group,baseField, xField , yField)
    xLabel = xField
    yLabel = yField # 'Relevance Exposure'
    legend = 'Expansion-' + baseField
    plt.legend (title=legend,ncol=2)
    fgen.showFigure(title,xField , yField )


for group_corpus in  'author-A TRAILER-A'.split():
    main()