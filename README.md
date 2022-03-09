# wordleBot :video_game:
### A python based wordle game.

Guess the WORDE in six tries.
Each guess must be a valid five-letter word. Hit the enter button to submit.
After each guess, the color of the tiles will change to show how close your guess was to the word.
This wordle game has three modes, **BOT mode** check the efficiency of the algorithm uses provided word lists, **GAME mode** allows the user to play the game, **TEST mode** allows user to test wordleBot to test a valid five letter word from the provided word list.

## USAGE:
```bash
 bash:~/$ python3 wordleBot.py <word length>* <mode>* <word-list-1>* <word-list-2>*
```
      
   ### where :
        word length, N(int): length of words to be played against
        mode(int): [1] bot mode, testing mode, Runs for all the words in list 1.
                   [2] game mode, playing mode for user.
                   [3] test mode, test wordleBot for a five letter word.
        word-list-1(str): File name having all posible N-letter-words.
        word-list-2(str): File name having filltered N-letter-words.

   ### Example :
```bash
  python3 wordleBot.py 5 2 allFiveLetterWords.txt filteredFiveLetterWords
```
![wordleBot](https://user-images.githubusercontent.com/53552871/157276033-8fbfef4f-9c6c-4da9-8e53-a3b819c8fdfb.gif)

 
## Authors
- [@AbhijeetKaran](https://github.com/AbhijeetKaran)
