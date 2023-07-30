###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

# ================================
# Part B: Golden Eggs
# ================================

Eggs = tuple[int, ...]
Memo = dict[int, int]


# Problem 1
def dp_make_weight(egg_weights: Eggs,
                   target_weight: int,
                   memo: Memo = {0: 0}) -> int:
    """
    Find number of eggs to bring back, using the smallest number of eggs.
    Assumes there is an infinite supply of eggs of each weight, and there is
    always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest
                  to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to
           use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    if target_weight in memo:
        return memo[target_weight]

    values = []
    for weight in sorted(egg_weights):
        if weight <= target_weight:
            values.append(dp_make_weight(egg_weights,
                                         target_weight - weight,
                                         memo))
    memo[target_weight] = min(values) + 1  # need +1 to acount for this search

    return memo[target_weight]


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
