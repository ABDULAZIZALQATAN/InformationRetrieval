import os

def requiredFile(file):
    return True

def listFiles (root,outfile):
    ctr = 1
    writeToFile = outfile != ''
    if (writeToFile):
        f = open(outfile,'w')
    for path, subdirs, files in os.walk(root):
        for name in files:
            if requiredFile(name):
                fullpath = os.path.join(path, name) + '\n'
                print(ctr , fullpath)
                ctr += 1
                if (writeToFile):
                    f.write(fullpath)
    if (writeToFile):
        f.close()
if __name__ == '__main__':
    path = 'D:\Data Collections\CORE17\data'
    outfile = r'C:\Users\kkb19103\Desktop\CORE17Filelist.txt'
    # outfile = ''
    listFiles(path,outfile)