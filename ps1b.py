###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    optimal_egg_combo = _dp_minimize_using_dict(egg_weights, target_weight)

    return len(optimal_egg_combo)


def _dp_minimize_using_dict(items, target):
    table = _make_table_as_dict(items, target)
    
    for row in range(1, len(items) + 1):
        current_item = items[row-1]
        prev_item = items[row-2] if row > 1 else 0
        
        for subproblem in range(1, target + 1):
            if subproblem == current_item:
                coins_selected = [current_item]
            elif subproblem < current_item:
                coins_selected = table[prev_item, subproblem]
            else:
                take = table[current_item, subproblem - current_item][:] + [current_item]
                dont_take = table[prev_item,subproblem]

                coins_selected = take if len(take) < len(dont_take) else dont_take
                
            table[current_item, subproblem] = coins_selected
 
    return table[items[-1], target]

def _dp_minimize_using_list(items, target):
    """
    Find a list of smallest number items that can add up to target
    Uses a list of lists as a lookup table.
    Returns a list of all items selected
    """
    table = _make_table_as_list(items, target)

    for item_row in range(1, len(items) + 1):
        current_item = items[item_row-1]
        
        for subproblem in range(1, target + 1):
            if subproblem == current_item:
                items_selected = [current_item]
            elif subproblem < current_item:
                items_selected = table[item_row-1][subproblem]
            else:
                take = [current_item] + table[item_row][subproblem-current_item][:]
                dont_take = table[item_row-1][subproblem]

                items_selected = dont_take if len(dont_take) < len(take) else take

            table[item_row][subproblem] = items_selected
            
    return table[-1][-1]
    
def _make_table_as_list(items, target):
    """
    Make a look-up table whose rows are the set of items and columns
    are a set of subproblems. Cells contain the minimum number of items
    needed to make each subproblem in a target.

    Assumptions:
    - i >= 1 for all i in items
    - all subproblems from 0 to target have an increment of one such that
        column[i+1] - column[i] = 1 for all i in columns
      
    
    Parameters:
    items - a tuple of integers sorted from smallest to largest
    target - int, problem whose solution involves adding 1 or more items

    Returns: list of lists, where rows represent the items and columns 
    represent subproblems such that subproblem <= target. The first row
    represents no item, the first column represents a subproblem of 0.
    The last cell contains the minimum number of items to make target.
    """
    table = [[[] for _ in range(target + 1)] for _ in range(len(items) + 1)]

    base_row = table[0]

    #all the subproblems to target
    #assumes the best possible increment as one
    for subproblem in range(target + 1):
        base_row[subproblem] = [1]*subproblem
    
    return table

def _make_table_as_dict(items, target):
    table = {}
    for row in range(len(items) + 1):
        current_item = items[row-1] if row > 0 else 0
        
        for subproblem in range(target + 1):
            selected_items = [] if row > 0 else [1]*subproblem
                
            table[current_item,subproblem] = selected_items
    
    return table
    
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99

    
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print("Eggs(list_table):", _dp_minimize_using_list(egg_weights, n))
    print("Eggs:(dict_table)", _dp_minimize_using_dict(egg_weights, n))
    print()

    coins = (1,5,10,19,20,40)
    n1 = 24
    print("Coins = (1,5,10,19,20,40)")
    print("n1 = 24")
    print("Expected: 2 (19 + 5)")
    print("Actual output:", dp_make_weight(coins, n1))
    print("Coins(list):", _dp_minimize_using_list(coins, n1))
    print("Coins(dict):", _dp_minimize_using_dict(coins, n1))
