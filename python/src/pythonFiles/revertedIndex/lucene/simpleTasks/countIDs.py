def countIDs(path):
    # Count ids in specific input file
    f = open(path,'r')
    ctr = 0
    for line in f:
        if line.__contains__('"id"'):
            ctr += 1
            print ("id",ctr)
    f.close()

if __name__ == '__main__':
    path = ''
    countIDs(path)