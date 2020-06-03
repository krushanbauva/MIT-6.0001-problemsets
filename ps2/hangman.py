# Problem Set 2, hangman.py
# Name: Krushan Bauva
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    result = True
    for i in secret_word:
        if i not in letters_guessed:
            result = False
            break
    return result



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ""
    for i in secret_word:
        if i in letters_guessed:
            guessed_word += i
        else:
            guessed_word += "_ "
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ""
    for i in string.ascii_lowercase:
        if i not in letters_guessed:
            available_letters += i
    return available_letters



def initialize_hangman(secret_word, warnings_remaining):
    '''
    secret_word: string, the secret word to guess.
    warnings_remaining: the number of warnings the user is left with
    
    Starts the game by printing the initial welcome messages.
    '''
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have", warnings_remaining, "warnings left.")



def print_dashed_lines():
    '''
    Prints a trail of dashed lines for better visibility.
    '''
    print("-------------------------------")



def is_vowel(letter):
    if letter in "aeiou":
        return True
    return False



def number_of_unique_letters(word):
    number = 0
    letters = []
    for i in word:
        if i not in letters:
            number += 1
            letters.append(i)
    return number



def penalty(secret_word, letters_guessed, warnings_remaining, guesses_remaining, type_of_error):
    '''
    secret_word: string, the secret word to guess.
    letters_guessed: list (of letters), which letters have been guessed so far
    warnings_remaining: the number of warnings the user is left with
    guesses_remaining: the number of guesses the user is left with
    type_of_error: the actual type of error committed by the user which is suppossed to be printed to the console.
    
    Penalizes the user for a wrong input and prints the type of error committed by the user
    '''
    if warnings_remaining == 0:
        print("Oops! " + type_of_error + " You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
        guesses_remaining -= 1
    elif warnings_remaining == 2:
        warnings_remaining -= 1
        print("Oops! " + type_of_error + " You have 1 warning left:", get_guessed_word(secret_word, letters_guessed))
    else:
        warnings_remaining -= 1
        print("Oops! " + type_of_error + " You have", warnings_remaining, "warnings left:", get_guessed_word(secret_word, letters_guessed))
    return (warnings_remaining, guesses_remaining)

    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    
    initialize_hangman(secret_word, warnings_remaining)
    
    while(guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed)):
        print_dashed_lines()
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters: " + get_available_letters(letters_guessed), end='')
        letter = input("Please guess a letter: ")
        if str.isalpha(letter):
            lower_letter = str.lower(letter)
            if lower_letter in letters_guessed:
                type_of_error = "You've already guessed that letter."
                (warnings_remaining, guesses_remaining) = penalty(secret_word, letters_guessed, warnings_remaining, guesses_remaining, type_of_error)
            else:
                letters_guessed.append(lower_letter)
                if lower_letter in secret_word:
                    print("Good guess:", get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! That letter in not in my word.")
                    print("Please guess a letter:", get_guessed_word(secret_word, letters_guessed))
                    if is_vowel(lower_letter):
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1
        else:
            type_of_error = "This is not a valid letter."
            (warnings_remaining, guesses_remaining) = penalty(secret_word, letters_guessed, warnings_remaining, guesses_remaining, type_of_error)
    
    print_dashed_lines()
    
    if is_word_guessed(secret_word, letters_guessed):
        total_score = guesses_remaining * number_of_unique_letters(secret_word)
        print("Congratulations, you won!")
        print("Your total score for this game is:", total_score)
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)
    


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    letters_guessed = []
    for i in my_word:
        if str.isalpha(i):
            if i not in letters_guessed:
                letters_guessed.append(i)
    i = 0
    j = 0
    result = True
    while(i<len(other_word) and j<len(my_word)):
        if str.isalpha(my_word[j]):
            if other_word[i] == my_word[j]:
                i += 1
                j += 1
            else:
                result = False
                break
        elif my_word[j] == "_":
            if other_word[i] in letters_guessed:
                result = False
            j += 2
            i += 1
        else:
            result = False
    if(i < len(other_word) or j < len(my_word)):
        result = False
    return result



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    hint = ""
    for word in wordlist:
        if match_with_gaps(my_word, word):
            hint = hint + word + " "
    if hint == "":
        hint = "No matches found"
    print(hint)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    
    initialize_hangman(secret_word, warnings_remaining)
    
    while(guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed)):
        print_dashed_lines()
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters: " + get_available_letters(letters_guessed), end='')
        letter = input("Please guess a letter: ")
        if str.isalpha(letter):
            lower_letter = str.lower(letter)
            if lower_letter in letters_guessed:
                type_of_error = "You've already guessed that letter."
                (warnings_remaining, guesses_remaining) = penalty(secret_word, letters_guessed, warnings_remaining, guesses_remaining, type_of_error)
            else:
                letters_guessed.append(lower_letter)
                if lower_letter in secret_word:
                    print("Good guess:", get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! That letter in not in my word.")
                    print("Please guess a letter:", get_guessed_word(secret_word, letters_guessed))
                    if is_vowel(lower_letter):
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1
        elif letter == '*':
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        else:
            type_of_error = "This is not a valid letter."
            (warnings_remaining, guesses_remaining) = penalty(secret_word, letters_guessed, warnings_remaining, guesses_remaining, type_of_error)
    
    print_dashed_lines()
    
    if is_word_guessed(secret_word, letters_guessed):
        total_score = guesses_remaining * number_of_unique_letters(secret_word)
        print("Congratulations, you won!")
        print("Your total score for this game is:", total_score)
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
