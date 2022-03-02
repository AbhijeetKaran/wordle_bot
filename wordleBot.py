import sys
from io import StringIO
import numpy as np
import pandas as pd


class WordList:
    def __init__(self,filename,n):
        self.wordlist = self.__importWordList(filename,n)
        self.wordmatrix = self.__loadMatrix()

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


    def deepfilteringExclude(self,nal,wl,wm):
        mcj = np.isin(wm,nal,invert=True)
        filt = np.where(np.all(mcj, axis=1))
        if len(filt) != 0:    
            wl = wl[filt]
            wm = wm[filt,:][0]
        return wl,wm


    def deepfiltering(self,ma,ml,wl,wm,cl):
        # a1 = np.array([0,1,2,3,4])
        ## FILTER ONE ## "words which all contains the alphabets"
        # if len(ma) != 5:
        for y in ma:
            cj = np.isin(wm,y)
            filt = np.where(np.any(cj, axis=1))
            if len(filt) == 0:
                continue
            wl = wl[filt]
            wm = wm[filt,:][0]
        
        ## FILTER TWO ## ""
        if len(ma) == 5 or len(wl) <= 2:
            return wl,wm

        cj = np.isin(wm,ma,invert=True)
        cjt = np.invert(cj)
        filt = np.where(np.any(cjt, axis=1))
        # filt = np.where(np.any(cj, axis=1))
        # print(cj)
        # print(filt)
        if len(filt) != 0:    
            wl = wl[filt]
            wm = wm[filt,:][0]
        # print(f"2 ma:{len(ma)} wl:{len(wl)} {wl}")
        
        ## FILTER THREE ##
        for z in range(0,len(ma)):
            condition = (wm[:,ml[z]] != ma[z]) 
            filt1 = np.where(condition)
            if len(filt1) == 0:
                continue
            wl = wl[filt1]
            wm = wm[filt1,:][0]
        return wl,wm

    def randomSelector(self,wl):
        # print(len(wl))
        rnd_ch = np.random.choice(wl,1)
        return rnd_ch

    def gameplay(self,original):
        wl = self.wordlist.copy()
        wm = self.wordmatrix.copy()
        nset = [x for x in range(0,5)]
        nset = set(nset)
        trials = 1
        sucess = False
        ma = []
        ml = []
        ca = []
        cl = []
        nal = []
        while True:
            predicted = list(self.randomSelector(wl))[0]
            sucess,ma,ml,ca,cl,nal = word_check(original,predicted,ma,ml,ca,cl,nal)
            if sucess == True:
                break
            else:
                for x in range(0,len(ca)):
                    wl,wm = self.filtering(cl[x],ca[x],wl,wm)
                nset = nset.difference(set(cl))
                if len(nal) > 0:
                    wl,wm = self.deepfilteringExclude(nal,wl,wm)
                    nal=[]
                if len(ma) > 0:
                    wl,wm = self.deepfiltering(ma,ml,wl,wm,cl)
                    ma=[]
                    ml=[]
                trials = trials + 1
                wl,wm = removeThisWord(predicted,wl,wm)
        if sucess == True and trials <=6:
            print(f"You guessed it in {trials} trials")
            return True
        else:
            print("you failed")
            return False

def removeThisWord(pred,wl,wm):
    ind = np.where(wl == pred)
    wl = np.delete(wl,ind)
    wm = np.delete(wm,ind,axis=0)
    return wl,wm
            
def word_check(x,y,ma,ml,ca,cl,nal):
    success_rate = 0
    for i in range(0,len(x)):
        ins = False
        pos = False
        if y[i] in x:
            ins = True
            if y[i] != x[i]:
                ma.append(y[i])
                ml.append(i)
        else:
            nal.append(y[i])

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
        return True,ma,ml,ca,cl,nal
    return False,ma,ml,ca,cl,nal


#<<Body>> 
#This is the first trial script. 
#Algorithm applied in this is without information theory and probablity.
#Hence the answer found is by randomly picking from the filtered set
#facing error when all alphabets are predicted yellow, pushed the word list to empty 
# s1 = "ladle"

n = int(sys.argv[1])
total_s = 0
total_l = 0
wl = WordList("possible_answers.txt",n)
copy_list = wl.wordlist.copy()
for x in copy_list:
    result = wl.gameplay(x)
    if result:
        total_s = total_s+1
    else:
        total_l = total_l+1
        print(f"true word :{x}")
        
#     # exit()
# result = wl.gameplay(s1)
print(f"Total accuracy is :{(total_s/(total_l+total_s))*100}%")
#this is the second trial
# getting 5 letter words from dictionary
# perl -nle 'print if /^[a-z]{5}$/' /usr/share/dict/words > words5.tx