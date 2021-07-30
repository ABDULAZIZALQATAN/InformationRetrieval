# from scipy.stats import pearsonr as person
import scipy.stats as sci
import src.noteBooks.FairnessPlotter.General as fgen
import matplotlib.pyplot as plt

#@title # Scatter Plot for groups
#@markdown ##### For The Following properties:
#@markdown ##### Axiom - 5 Docs - 5 Terms

#@ For Axiom - 5 Docs & 5 Terms
group_corpus = "author-A" #@param ['DOCTYPE-A', 'DATE_TIME-A', 'SLUG-A', 'author-A', 'TRAILER-A', 'doc.copyright-holder-C', 'doc.copyright-year-C', 'descriptor-C', 'types_of_material-C', 'taxonomic_classifier-C', 'general_descriptor-C', 'date_publication-C', 'title-C', 'author-C', 'slug-C', 'publication_day_of_month-C', 'publication_month-C', 'publication_year-C', 'publication_day_of_week-C', 'dsk-C', 'print_page_number-C', 'print_section-C', 'print_column-C', 'online_sections-C', 'banner-C', 'author-W', 'pubDate-W', 'kicker-W', 'byLine-W']
b = "0.5" #@param ["0", "0.5"]
xField = "e_rel_sum" #@param ["e_ret", "e_rel_sum", "e_rel_count", "e_size", "e_grp"]
yField = "e_ret" #@param ["e_ret", "e_rel_sum", "e_rel_count", "e_size", "e_grp"]

def get_exposure_title (exp):
    switcher = {
        'e_ret' : 'Retrievability',
        'e_rel_sum' : 'Relevance Total' ,
        'e_rel_count' : 'Relevance Count' ,
        'e_size' : 'Size' ,
        'e_grp' : 'Equality'
    }
    result = switcher.get(exp) + ' Exposure'
    return result

def get_group():
    # Get group from gathered group_corpus combination
    return group_corpus.split('-')[0]

def calculate_correlation (x,y):
    '''
    # Pearson's correlation coefficient =
    covariance(X, Y) / (stdv(X) * stdv(Y))
    '''
    # Pearson's correlation
    result =  sci.pearsonr (x, y)[0]

    # Spearman’s Correlation
    # result =  sci.spearmanr(x, y)[0]

    # Kendall’s tau Correlation
    # result =  sci.kendalltau (x, y)[0]

    # result = pg.pairwise_corr(data=pd.DataFrame([x,y]), method='pearson')

    return result

def get_e_ret (dfTemp):
    '''
      Calculate Exposure_g
          For each group calculate the sum of the r(d) values
          Then workout the proportion of r(d) for each group g.  = Exposure_g
      '''
    fld = 'r' + b
    group = get_group()
    dfTemp = dfTemp.groupby(group, as_index=False).agg({fld: 'sum'})
    e_ret = fgen.compute_percent(dfTemp[fld])
    return e_ret

def get_e_rel (dfTemp , aType):
    '''
    Calculate Rel_g
      For each group, calculate the sum of the #rels for each
      group g, = Rel_g =
      sum of rels for group / total rels over the collection
    '''
    fld = 'rel_' + aType
    group = get_group()
    dfTemp = dfTemp.groupby(group, as_index=False).agg({fld: 'sum'})
    e_rel = fgen.compute_percent(dfTemp[fld])
    return e_rel

def get_e_size (dfTemp):
    '''
    Calculate Size_g
        For each group, calculate the total group member -
        i.e. the number of documents in the group = Size_g
    '''
    fld = 'docid'
    group = get_group()
    dfTemp = dfTemp.groupby(group, as_index=False).agg({fld: 'count'})
    e_size = fgen.compute_percent(dfTemp[fld])
    return e_size

def get_e_grp (dfTemp):
    '''
    Calculate Group_g
    - [GROUPs] ALL GROUPS ARE EQUAL
    For each group, Group_g = 1/(Number of groups).
    '''
    fld = 'group'
    group = get_group()
    dfTemp[fld] = 1
    dfTemp = dfTemp.groupby(group, as_index=False).agg({fld: 'count'})
    e_grp = fgen.compute_percent(dfTemp[fld])

    return e_grp

def get_exposure (df , e_type):
    # Calculate Exposure based on given Type

    if (e_type == 'e_ret'):
        result = get_e_ret(df)
    elif (e_type == 'e_rel_sum'):
        result = get_e_rel(df,'sum')
    elif (e_type == 'e_rel_count'):
        result = get_e_rel(df,'count')
    elif (e_type == 'e_size'):
        result = get_e_size(df)
    elif (e_type == 'e_grp'):
        result = get_e_grp(df)

    return result

def main():
    if (xField == yField):
        print('xField and yField should be different')
        return

    parts = group_corpus.split('-')
    corpus = parts[1]

    # Step 1 : Get All Static Fields Based on Corpus
    df = fgen.read_all_fields(corpus)
    # Step 2 : Get Ret List Based on (Corpus , Exp , docs , terms )
    dfTemp = fgen.read_ret_values(corpus)
    # Merge Two Dfs based on docid
    df = df.merge(dfTemp,'left','docid')
    # Fill None Values with zeroes
    df['r0'].fillna(0, inplace=True)

    # Get Values based on input Field (ret - rel - size - grp)
    x = get_exposure(df,xField)
    y = get_exposure(df,yField)

    # Calculate Correlation value
    # 3 Types available default Pearson
    corr = calculate_correlation(x,y)
    print('\nCorrelation = ' , corr)

    # Extract Title from input Field e_ret = Retrievability Exposure
    xTitle = get_exposure_title(xField)
    yTitle = get_exposure_title(yField)

    # Format main title
    corpus = fgen.getCorpus(corpus)
    group = get_group()
    line = '%s - Group: %s - b:%s\n%s Vs %s ' % (corpus , group.upper() ,b ,xTitle,yTitle)
    # Configure Plot
    plt.title(line)
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    plt.scatter(x,y )
    plt.show()
    # Print total number of plotted values
    print ('Total Values : ' , len(x))

# Call Main Function
main()