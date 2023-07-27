# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

def plain_text_message_test(message, shift, expected_output):
    '''
    Runs a test case for the PlaintextMessage class

    message (string): the text to be encrytped
    shift (integer): the amount by which to shift every letter of the 
    alphabet. 0 <= shift < 26
    expected_output: expected output after the shifting
    '''
    plaintext = PlaintextMessage(message, shift)
    print('\t\tInput: ', message)
    print('\t\tShift: ', shift)
    print('\t\tExpected Output: ', expected_output)
    print('\t\tActual Output: ', plaintext.get_message_text_encrypted())
    
    if expected_output == plaintext.get_message_text_encrypted():
        print("\tTest PASSED")
    else:
        print("\tTest FAILED")

def cipher_text_message_test(message, expected_output):
    '''
    Runs a test case for the PlaintextMessage class

    message (string): the text to be encrytped
    shift (integer): the amount by which to shift every letter of the 
    alphabet. 0 <= shift < 26
    expected_output: expected output after the shifting
    '''
    ciphertext = CiphertextMessage(message)
    print('\t\tInput: ', message)
    print('\t\tExpected Output: ', expected_output)
    print('\t\tActual Output: ', ciphertext.decrypt_message())

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text

        self.valid_words  = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        shift_dict = {}
        for i, char in enumerate(string.ascii_lowercase):
            shift_index = (i+shift) % 26
            shift_dict[char] = string.ascii_lowercase[shift_index]
            shift_dict[char.upper()] = string.ascii_lowercase[shift_index].upper()

        return shift_dict


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        cipher = ''
        for char in self.get_message_text():
            if char.lower() in string.ascii_lowercase:
                cipher += shift_dict[char]
            else:
                cipher += char

        return cipher

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_valid_word_count = 0
        best_shift = None
        best_decrypted_message = ''

        encrypted_message = PlaintextMessage(self.get_message_text(), 0)
        for shift in range(26):
            encrypted_message.change_shift(shift)
            valid_word_count = 0
            for word in encrypted_message.get_message_text_encrypted().split():
                valid_word_count += 1 if is_word(self.get_valid_words(), word) else 0

            if valid_word_count > best_valid_word_count:
                best_valid_word_count = valid_word_count
                best_shift = 26 - shift
                best_decrypted_message = encrypted_message.get_message_text_encrypted()

        return (best_shift, best_decrypted_message)

if __name__ == '__main__':

    print("----- PlaintextMessage Tests -----")

    print("\tTEST 1:")
    plain_text_message_test('hello!', 2, 'jgnnq!')

    print("\n\tTEST 2:")
    plain_text_message_test('heLlo', 2, 'jgNnq')

    print("\n\tTEST 3:")
    plain_text_message_test('heLlo heLlo', 2, 'jgNnq jgNnq')

    print("----------------------------------\n")

    print("----- CiphertextMessage Tests -----")

    print("\tTEST 1:")
    cipher_text_message_test('jgnnq!', (2,'hello!'))

    print("\n\tTEST 2:")
    cipher_text_message_test('jgNnq', (2,'heLlo'))

    print("\n\tTEST 3:")
    cipher_text_message_test('jgNnq jgNnq', (2,'heLlo heLlo'))

    print("----------------------------------\n")
    print("----- Story Test -----")

    story = get_story_string()
    ciphertext = CiphertextMessage(story)
    print('Unencypted story:', ciphertext.decrypt_message())
