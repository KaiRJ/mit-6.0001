import hangman

secret_word = 'apple'
letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
print(hangman.is_word_guessed(secret_word, letters_guessed))
print(hangman.get_guessed_word(secret_word, letters_guessed))
print(hangman.get_available_letters(letters_guessed))