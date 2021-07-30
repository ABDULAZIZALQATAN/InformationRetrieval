def addnumberstotopic(path):
    f = open(path,'r')
    lines = []
    seq = 1
    for line in f:
        line = '%d\t%s' % (seq,line)
        seq += 1
        lines.append(line)
    f.close()
    f = open(path,'w')
    f.writelines(lines)
    f.close()

if __name__ == '__main__':
    corpus = 'AQUAINT'
    path = r'C:\Users\kkb19103\Desktop\My Files 07-08-2019\BiasMeasurementExperiments\Resources\%s\200K.qry' % corpus
    # addnumberstotopic(path)