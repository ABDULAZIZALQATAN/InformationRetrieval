import pandas as pd

def sortQueries(path):
    path = r'C:\Users\kkb19103\Desktop\new\bigram.out'
    names = 'seq t1 t2 f1 f2 fboth score'.split()
    df = pd.read_csv(path, sep=' ', names=names)
    df.sort_values(by='score', ascending=False, inplace=True)
    path = r'C:\Users\kkb19103\Desktop\new\bigramNew.out'
    df.to_csv(path, sep='\t', index=None)


def main():
    sortQueries('')

if __name__ == '__main__':
    main()