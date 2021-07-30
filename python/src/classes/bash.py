import subprocess
import src.classes.general as gen

def runBashFile(shFile):
    cmd = 'sh %s' % shFile
    bashCmd = 'bash -c \"%s\" ' % cmd
    return subprocess.getoutput(bashCmd)

def runBashCmd(cmd):
    bashCmd = 'bash -c \"%s\" ' % cmd
    subprocess.getoutput(bashCmd)

def runBashFileFromPython (file):
    # We Must have windows version and linux version ~/anserini

    newFile2 = file.replace('New.sh','New1.sh')
    cmd = r"cd ~/anserini/bash && cat %s | tr -d '\r' > %s && sh %s" % \
          (file,newFile2,newFile2)
    runBashCmd(cmd)