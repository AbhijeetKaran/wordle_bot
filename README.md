# wordleBot :video_game:
### A python based wordle game.

Guess the WORDLE in six tries.
Each guess must be a valid five-letter word. Hit the enter button to submit.
After each guess, the color of the tiles will change to show how close your guess was to the word.
This wordle game has two modes, BOT mode check the efficiency of the algorithm used provided word lists, and GAME mode allows the user to play the game.

## USAGE:
```bash
 bash:~/$ python3 wordleBot.py <word length>* <mode>* <word-list-1>* <word-list-2>*
```
      
   ### where :
        word length, N(int): length of words to be played against
        mode(int): [1] bot mode, testing mode, Runs for all the words in list 1.
                   [2] game mode, playing mode for user.       
        word-list-1(str): File name having all posible N-letter-words.
        word-list-2(str): File name having filltered N-letter-words.

   ### Example :
```bash
  python3 wordleBot.py 5 1 allFiveLetterWords.txt filteredFiveLetterWords
                                    or
  python3 wordleBot.py 5 2 allFiveLetterWords.txt filteredFiveLetterWords
```
![wordleBot](https://user-images.githubusercontent.com/53552871/157276033-8fbfef4f-9c6c-4da9-8e53-a3b819c8fdfb.gif)

 
## Authors
- [@AbhijeetKaran](https://github.com/AbhijeetKaran)
