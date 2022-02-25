import sys
from io import StringIO
import numpy as np
import pandas as pd


class WordList:
    def __init__(self,filename,n):
        self.wordlist = self.__importWordList(filename,n)
        self.wordmatrix = self.__loadMatrix()
        self.topChar = [x.lower() for x in self.__loadTopChar()]

    def __loadTopChar(self):
        edata = pd.read_csv("alpha.tsv",sep="\t",header=None)
        elist = list(edata[0])
        return elist

    def __loadMatrix(self):
        sample = []
        for x in self.wordlist:
            sample.append(list(x))
        sample = np.array(sample)
        return sample

    def __importWordList(self,filename,n):
        fh = open(filename,'r')
        wordlist = StringIO(fh.read())
        nf = f"U{n}"
        wordlist = np.loadtxt(wordlist,dtype=nf)
        return wordlist

    def filtering(self,lc,ac,wl,wm):
        condition = (wm[:,lc] == ac)
        filt = np.where(condition)
        return wl[filt],wm[filt,:][0]

    def deepfiltering(self,ma,ml,wl,wm,cl):
        a1 = np.array([0,1,2,3,4])
        # in word filter
        for y in ma:
            cj = np.isin(wm,y)
            filt = np.where(np.any(cj, axis=1))
            if len(filt) == 0:
                continue
            wl = wl[filt]
            wm = wm[filt,:][0]
        # # out word filter
        cj = np.isin(wm,ma,invert=True)
        filt = np.where(np.any(cj, axis=1))
        if len(filt) != 0:    
            wl = wl[filt]
            wm = wm[filt,:][0]
        for z in range(0,len(ma)):
            condition = (wm[:,ml[z]] != ma[z]) 
            filt1 = np.where(condition)
            if len(filt1) == 0:
                continue
            wl = wl[filt1]
            wm = wm[filt1,:][0]
        return wl,wm

    def randomSelector(self,wl):
        rnd_ch = np.random.choice(wl,1)
        return rnd_ch
    
    def randomFirstSelector(self,wm,wl,sl):
        score = []
        ax = np.isin(wm,sl)
        asx = ax.sum(axis=1)
        axi = np.amax(asx)
        return wl[axi]

    def gameplay(self,original):
        wl = self.wordlist
        wm = self.wordmatrix
        sl = self.topChar[:10]
        nset = [x for x in range(0,5)]
        nset = set(nset)
        trials = 1
        sucess = False
        ma = []
        ml = []
        ca = []
        cl = []
        while True:
            if trials > 1:
                predicted = list(self.randomSelector(wl))[0]
            else:
                predicted = self.randomFirstSelector(wm,wl,sl)
            sucess,ma,ml,ca,cl = word_check(original,predicted,ma,ml,ca,cl)
            if sucess == True:
                break
            else:
                for x in range(0,len(ca)):
                    wl,wm = self.filtering(cl[x],ca[x],wl,wm)
                nset = nset.difference(set(cl))
                if len(ma) > 0:
                    wl,wm = self.deepfiltering(ma,ml,wl,wm,cl)
                    ma=[]
                    ml=[]
                trials = trials + 1
                wl,wm = removeThisWord(predicted,wl,wm)
        if sucess == True:
            print(f"You guessed it in {trials} trials")
        else:
            print("you failed")

def removeThisWord(pred,wl,wm):
    ind = np.where(wl == pred)
    wl = np.delete(wl,ind)
    wm = np.delete(wm,ind,axis=0)
    return wl,wm
            
def word_check(x,y,ma,ml,ca,cl):
    success_rate = 0
    for i in range(0,len(x)):
        ins = False
        pos = False
        if y[i] in x:
            ins = True
            if y[i] != x[i]:
                ma.append(y[i])
                ml.append(i) 
        if y[i] == x[i]:
            pos = True
            ca.append(y[i])
            cl.append(i)
        if ins == True and pos == True:
            print(f"\033[1;42m'{y[i]}'\033[0m",end="")
            success_rate = success_rate + 1
        elif ins == True and pos == False:
            print(f"\033[1;43m'{y[i]}'\033[0m",end="")
        else:
            print(f"\033[1;40m'{y[i]}'\033[0m",end="")
    print()
    if success_rate == len(x):
        return True,ma,ml,ca,cl
    return False,ma,ml,ca,cl


#<<Body>> 
#This is the first trial script. 
#Algorithm applied in this is without information theory and probablity.
#Hence the answer found is by randomly picking from the filtered set

s1 = "knoll"
n = int(sys.argv[1])
wl = WordList("words5.txt",n)
wl.gameplay(s1)

#this is the second trial
# getting 5 letter words from dictionary
# perl -nle 'print if /^[a-z]{5}$/' /usr/share/dict/words > words5.tx