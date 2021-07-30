def removeCharacter(path):
    # Remove specific character from all lines in input File
    f = open(path,'r')
    lines = []
    ctr = 0
    found = 0
    targetChar = chr(28)
    for line in f :
        ctr += 1
        if line.__contains__(targetChar):
            found += 1
            newLine = line.replace(targetChar,'')
        else:
            newLine = line
        lines.append(newLine)
        print('append',ctr)
    f.close()
    path = '/mnt/c/Users/kkb19103/Desktop/test.jsonl'
    f = open(path,'w')
    ctr = 0
    for line in lines:
        ctr+=1
        f.write(line)
        print('write', ctr)
    print ('Total Found ',found)
    f.close()
    lines = None

if __name__ == '__main__':
    path = ''
    removeCharacter(path)