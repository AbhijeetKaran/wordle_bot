import sys
from io import StringIO
import numpy as np
import pandas as pd
import time


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


    ## FILTER ONE ## "words which all contains the alphabets"
    def deepfiltering(self,ma,ml,wl,wm,cl):
        for y in ma:
            cj = np.isin(wm,y)
            filt = np.where(np.any(cj, axis=1))
            if len(filt) == 0:
                continue
            wl = wl[filt]
            wm = wm[filt,:][0]
        
        ## FILTER TWO ## "words which all contains the absolute alphabets at non-absolute location"
        if len(ma) == 5 or len(wl) <= 2:
            return wl,wm

        cj = np.isin(wm,ma,invert=True)
        cjt = np.invert(cj)
        filt = np.where(np.any(cjt, axis=1))
        if len(filt) != 0:    
            wl = wl[filt]
            wm = wm[filt,:][0]
        
        ## FILTER THREE ## "words which all contains the alphabets at non-absolute location"
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

    def check_dup(self,word):
        i = 0
        for a in word:
            i = word.count(a)
            if i > 1:
                return False 
        return True

    def gameplay(self,original):
        wl = self.wordlist.copy()
        wm = self.wordmatrix.copy()
        nset = [x for x in range(0,5)]
        nset = set(nset)
        trials = 1
        sucess = False
        ma = [] #present alphabets
        ml = [] #present alphabets non-locations
        ca = [] #confirm alphabets
        cl = [] #confirm location
        nal = [] #confirm non alphabets
        while True:
            if trials == 1:
                while True: 
                    predicted = list(self.randomSelector(wl))[0]
                    if self.check_dup(predicted):
                        break
            else:
                if trials == 2 and len(ma) == 0 and len(ca) == 0:
                    while True: 
                        predicted = list(self.randomSelector(wl))[0]
                        if self.check_dup(predicted):
                            break
                else:
                    predicted = list(self.randomSelector(wl))[0]
            sucess,ma,ml,ca,cl,nal = word_check(original,predicted,ma,ml,ca,cl,nal)
            if sucess == True:
                break
            else:
                for x in range(0,len(ca)):
                    wl,wm = self.filtering(cl[x],ca[x],wl,wm)
                nset = nset.difference(set(cl))
                #exclude no alphabet words 
                if len(nal) > 0:
                    wl,wm = self.deepfilteringExclude(nal,wl,wm)
                    nal=[]
                #exclude no position alphabet words
                if len(ma) > 0:
                    wl,wm = self.deepfiltering(ma,ml,wl,wm,cl)
                    ma=[]
                    ml=[]
                trials = trials + 1
                wl,wm = removeThisWord(predicted,wl,wm)
        if sucess == True and trials <=6:
            print(f"\033[1;32m SUCCESS\033[0m {trials}/6\n")
            return True
        else:
            print(f"\033[1;31m FAILED\033[0m {trials}/{6}")
            return False
    
    def askInput(self,n,wl):
        while True:
            val = input(f"\033[1;36m Your guess no. {n}: \033[0m")
            if len(val) == 5:
                if val not in wl:
                    print(f"\033[1;33m Enter another 5 letter word, this word not in list.\033[0m")
                    continue
                return val
            else:
                print(f"\033[1;31m ERROR: Length of word not equal to 5, please enter a 5 letter word.\033[0m")

    def gameModeplay(self,original):
        wl = self.wordlist.copy()
        wm = self.wordmatrix.copy()
        nset = [x for x in range(0,5)]
        nset = set(nset)
        trials = 1
        sucess = False
        ma = [] #present alphabets
        ml = [] #present alphabets non-locations
        ca = [] #confirm alphabets
        cl = [] #confirm location
        nal = [] #confirm non alphabets
        while True:
            if trials > 6:
                break
            predicted = self.askInput(trials,self.wordlist)
            sucess,ma,ml,ca,cl,nal = word_check(original,predicted,ma,ml,ca,cl,nal)
            if sucess == True:
                break
            else:
                for x in range(0,len(ca)):
                    wl,wm = self.filtering(cl[x],ca[x],wl,wm)
                nset = nset.difference(set(cl))
                #exclude no alphabet words 
                if len(nal) > 0:
                    wl,wm = self.deepfilteringExclude(nal,wl,wm)
                    nal=[]
                #exclude no position alphabet words
                if len(ma) > 0:
                    wl,wm = self.deepfiltering(ma,ml,wl,wm,cl)
                    ma=[]
                    ml=[]
                trials = trials + 1
                wl,wm = removeThisWord(predicted,wl,wm)
        if sucess == True and trials <=6:
            print(f"\033[1;32m SUCCESS\033[0m {trials}/6\n")
            return True
        else:
            print(f"\033[1;31m FAILED\033[0m {trials}/{6}")
            print(f"\033[1;45m Correct word : '{original}' \033[0m\n")
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
                pos = True
                ca.append(y[i])
                cl.append(i)
        else:
            nal.append(y[i])

        if ins == True and pos == True:
            print(f"\033[1;42m\033[1;97m {y[i]} \033[0m",end="")
            success_rate = success_rate + 1
        elif ins == True and pos == False:
            print(f"\033[1;103m\033[1;97m {y[i]} \033[0m",end="")
        else:
            print(f"\033[0;47m\033[1;97m {y[i]} \033[0m",end="")
    print()
    if success_rate == len(x):
        return True,ma,ml,ca,cl,nal
    return False,ma,ml,ca,cl,nal

#<<Body>>
start_time = time.time()
n = int(sys.argv[1])
mode = int(sys.argv[2])
file1 = sys.argv[3].strip()
file2 = sys.argv[4].strip()
total_s = 0
total_l = 0
if mode == 1:
    wl = WordList(file1,n)
    fh = open(file2,'r')
    for x in fh:
        x = x.strip()
        result = wl.gameplay(x)
        if result:
            total_s = total_s+1
        else:
            print(f"\033[1;45m Correct word : '{x}' \033[0m\n")
            total_l = total_l+1
    print(f"Total accuracy is: {round((total_s/(total_l+total_s))*100,2)}%")
    print(f"Total success: \033[1;42m{total_s}\033[0m/{total_l+total_s}")
    print(f"Total fails: \033[1;41m{total_l}\033[0m/{total_l+total_s}")
    end_time = time.time()
    print(f"Time taken : {round(end_time-start_time,2)}")
elif mode == 2:
    wl = WordList(file2,n)
    original = list(wl.randomSelector(wl.wordlist))[0]
    result = wl.gameModeplay(original)
elif mode == 3:
    wl = WordList(file1,n)
    while True:
        original = input(f"\033[1;36m Enter word to be predicted: \033[0m")
        if len(original) == 5:
            if original not in wl.wordlist:
                print(f"\033[1;33m Enter another 5 letter word.\033[0m")
                continue
            break
        else:
            print(f"\033[1;31m ERROR: Length of word not equal to 5, please enter a 5 letter word.\033[0m")
    result = wl.gameplay(original)
else:
    print(f"\033[1;31mERROR!!! Invalid mode Number\033[0m")
# perl -nle 'print if /^[a-z]{5}$/' /usr/share/dict/words > words5.tx
