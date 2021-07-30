# import pandas as pd
import src.classes.general as gen

def isStopWord(word):
    fname = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\LUCENE\anserini\bash\perBash.sh'
    # fname = r'~/anserini/bash/runRetrieval.sh'
    # fname = r'~/anserini/bash/perBash.sh'

    fname = gen.getLinuxPath(fname)
    f = open(fname,'r')
    for line in f:
        print(line)
if __name__ == '__main__':
    isStopWord('i')