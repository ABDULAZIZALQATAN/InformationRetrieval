import os
def removeDashes (path):
    files = os.listdir(path)
    for file in files:
        file = path + '/' + file
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        lines = ''.join(lines)
        lines = lines.replace('-','')
        f = open(file,'w')
        f.write(lines)
        f.close()
        print('Dashes Removed From File :', file)

if __name__ == '__main__':
    path = ''
    removeDashes(path)