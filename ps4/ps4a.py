# Problem Set 4A
# Name: Krushan
# Collaborators:
# Time Spent: x:xx

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
    
    if len(sequence) == 1:
        return list(sequence)
    
    elif len(sequence) > 1:
        perm = []
        for i in get_permutations(sequence[1:]):
            for j in range(len(sequence)):
                perm.append(i[0:j] + sequence[0] + i[j:])
        return perm



if __name__ == '__main__':
    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input2 = "pan"
    print("Input:", example_input2)
    print("Expected Output:", ["pan", "pna", "nap", "npa", "apn", "anp"])
    print("Actual Output:", get_permutations(example_input2))
    
    example_input3 = "itr"
    print("Input:", example_input3)
    print("Expected Output:", ["itr", "irt", "tir", "tri", "rit", "rti"])
    print("Actual Output:", get_permutations(example_input3))
    
    example_input4 = "kru"
    print("Input:", example_input4)
    print("Expected Output:", ["kru", "kur", "urk", "ukr", "ruk", "rku"])
    print("Actual Output:", get_permutations(example_input4))


