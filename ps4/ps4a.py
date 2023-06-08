# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from typing import Sequence


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    permutations = []
    if len(sequence) <= 1:
        permutations = [sequence]
    else:
        for word in get_permutations(sequence[1:]):
            # get all combinations of adding first letter back
            for i in range(len(word)+1):
                new_word = word[:i] + sequence[0] + word[i:]
                permutations.append(new_word)

    return permutations

def test_get_permutations(sequences):
    '''
    Test the get_permutations using a list of sequences and expected outputs.

    :param sequences: a list of typles containing sequences to test and their expected output
    :type sequences: list[tuple]
    '''
    test_number = 1
    for sequence, expected_output in sequences:
        print(f"Test case {test_number}")
        print(f"\tSequence: {sequence}")
        print(f"\tExpected Output: {expected_output}")
        actual_output = get_permutations(sequence)
        print(f"\tActual Output: {actual_output}")
        if actual_output.sort() == expected_output.sort():
            print("Test: PASSED\n")
        else:
            print("Test: FAILED\n")
        test_number += 1


if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    sequences = [
        ('', ['']),
        ('a', ['a']),
        ('ab', ['ab', 'ba']),
        ('abc', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    ]
    test_get_permutations(sequences)

    # get_permutations('ab')

    pass #delete this line and replace with your code here

