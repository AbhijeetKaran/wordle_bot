import sys
from io import StringIO
import numpy as np
import pandas as pd


class WordList:
    def __init__(self,filename,n):
        self.wordlist = self.__importWordList(filename,n)
        self.wordmatrix = self.__loadMatrix()
        self.wordScore = self.__wordScorer()

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

    def __wordScorer(self):
        info = iscoreLoader()
        vowels = ['a','e','i','o','u']
        scores = []
        for x in self.wordlist:
            s = 0
            for i in x:
                if i in vowels:
                    s = s+5
                i=i.upper()
                s = s+info[i]
            scores.append(s)
        return np.array(scores)

    def filtering(self,lc,ac,wl,wm):
        condition = (wm[:,lc] == ac)
        filt = np.where(condition)
        return wl[filt],wm[filt,:][0]

    def deepfiltering(self,ma,wl,wm):
        a1 = np.array([0,1,2,3,4])
        mj = np.isin(wm,ma)
        filt = np.where(np.any(mj, axis=1))
        if len(filt) == 0:
            return wl,wm
        else:
            return wl[filt],wm[filt,:][0]

    def randomSelector(self,wl):
        rnd_ch = np.random.choice(wl,1)
        return rnd_ch

    def highScoreSelector(self,wl,sl):
        max_scorer_i = np.argmax(sl)
        if isinstance(max_scorer_i, list):
            rnd_ch = np.random.choice(list(wl[max_scorer_i]),1)
        else:
            rnd_ch = wl[max_scorer_i]
        return rnd_ch

    # def probScoreSelector(self,wl,sl):

    def gameplay(self,original):
        wl = self.wordlist
        wm = self.wordmatrix
        sl = self.wordScore
        nset = [x for x in range(0,5)]
        nset = set(nset)
        trials = 1
        sucess = False
        ma = []
        ca = []
        cl = []
        while True:
            predicted = list(self.randomSelector(wl))[0]
            # predicted = self.highScoreSelector(wl,sl)
            sucess,ma,ca,cl = word_check(original,predicted,ma,ca,cl)
            if sucess == True:
                break
            else:
                # if len(ca) == 0 or len(ma) > 0:
                #     wl,sl = removeThisWord(predicted,wl,sl)
                for x in range(0,len(ca)):
                    wl,wm = self.filtering(cl[x],ca[x],wl,wm)
                nset = nset.difference(set(cl))
                if len(ma) > 0:
                    wl,wm = self.deepfiltering(ma,wl,wm)
                    ma=[]
                trials = trials + 1
        if sucess == True:
            print(f"You guessed it in {trials} trials")
        else:
            print("you failed")

def removeThisWord(pred,wl,sl):
    ind = np.where(wl == pred)
    wl = np.delete(wl,ind)
    sl = np.delete(sl,ind)
    return wl,sl
            
def word_check(x,y,ma,ca,cl):
    success_rate = 0
    for i in range(0,len(x)):
        ins = False
        pos = False
        if y[i] in x:
            ins = True
            if y[i] not in ma:
                ma.append(y[i]) 
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
        return True,ma,ca,cl
    return False,ma,ca,cl

def iscoreLoader():
        alphascores = pd.read_csv("alpha.tsv",sep="\t",header=None)
        scoreCard = {}
        for rw in alphascores.itertuples(index=False):
            scoreCard[rw[0]] = float(rw[2])
        return scoreCard



#<<Body>> 
#This is the first trial script. 
#Algorithm applied in this is without information theory and probablity.
#Hence the answer found is by randomly picking from the filtered set

s1 = "caulk"
n = int(sys.argv[1])
wl = WordList("words5.txt",n)
wl.gameplay(s1)

# getting 5 letter words from dictionary
# perl -nle 'print if /^[a-z]{5}$/' /usr/share/dict/words > words5.tx