# wordleBot :video_game:
A python based wordle game 

## USAGE:
```bash
 bash:~/$ python3 wordleBot.py <word length> <mode> <word list 1> <word list 2>
```
      
   ### where :
        word length, N(int): length of words to be played against
        mode(int): [1] bot mode, testing mode, Runs for all the words in list 2
                   [2] game mode, playing mode for user.       
        word list 1(str): File name having all posible N-letter-words
        word list 2(str): File name having filltered N-letter-words

   ### Example :
```bash
  python3 wordleBot.py 5 1 allFiveLetterWords.txt filteredFiveLetterWords
                                    ***or***
  python3 wordleBot.py 5 2 allFiveLetterWords.txt filteredFiveLetterWords
```
![ezgif com-gif-maker](https://user-images.githubusercontent.com/53552871/157242350-342a0949-2352-4f3a-bae6-86c3c8122f35.gif)![ezgif com-gif-maker](https://user-images.githubusercontent.com/53552871/157242268-05d4a5b6-77f3-4c85-8f6d-3a8537d2da00.gif)
 
## Authors
- [@AbhijeetKaran](https://github.com/AbhijeetKaran)
