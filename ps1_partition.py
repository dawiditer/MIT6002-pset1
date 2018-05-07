# From codereview.stackexchange.com                    
def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b

def get_partitions(set_):
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]

#The above solution was creating set partitions which cannot contain duplicates, with the following conditions:
##The empty set has exactly one partition, namely emptyset .
##For any nonempty set X, P = {X} is a partition of X, called the trivial partition.
##Particularly, every singleton set {x} has exactly one partition, namely { {x} }.
##For any non-empty proper subset A of a set U, the set A together with its complement form a partition of U, namely, {A, U \ A}.
##The set { 1, 2, 3 } has these five partitions (one partition per item):
###{ {1}, {2}, {3} }, sometimes written 1|2|3.
###{ {1, 2}, {3} }, or 12|3.
###{ {1, 3}, {2} }, or 13|2.
###{ {1}, {2, 3} }, or 1|23.
###{ {1, 2, 3} }, or 123 (in contexts where there will be no confusion with the number).
##The following are not partitions of { 1, 2, 3 }:
###{ {}, {1, 3}, {2} } is not a partition (of any set) because one of its elements is the empty set.
###{ {1, 2}, {2, 3} } is not a partition (of any set) because the element 2 is contained in more than one block.
###{ {1}, {2} } is not a partition of {1, 2, 3} because none of its blocks contains 3; however, it is a partition of {1, 2}.

#this solution however creates 'list_partitions'
#allowing a list to contain duplicates.
def list_partitions(list_):
    """
    Requires a sorted list from smallest to largest
    else will produce redundant data
    """
    sorted_list = sorted(list_)
    if not sorted_list:
        yield []
        return
    for i in range(2**len(sorted_list)//2):
        parts = [list(), list()]
        for item in sorted_list:
            parts[i&1].append(item)
            i >>= 1
        for b in list_partitions(parts[1]):
            yield [parts[0]]+b

def get_list_partitions(list_):
    #produces redundant data but is faster
    for partition in list_partitions(list_):
        yield [list(elt) for elt in partition]
        
    #takes care of redundancy but is slower
##    distinct_partitions = []
##    for partition in list_partitions(list_):
##        sorted_partition = sorted(partition)
##        if sorted_partition not in distinct_partitions:
##            distinct_partitions.append(sorted_partition)        
##            yield [list(elt) for elt in sorted_partition]
