# ---------------------------------
# ------- 01 Range Checker --------
# ---------------------------------

print("--- 01 Range Checker ---")
def in_range(num, start, end):
    return start <= num <= end

print("Is 3 in range (-5, 5)?", in_range(3, -5, 5))


# ------------------------------------
# -- 02 Two Lists Into a Dictionary --
# ------------------------------------

print("\n--- 02 Two Lists Into a Dictionary ---")
def lists_to_dict(list1, list2):
    return dict(zip(list1, list2))

print(lists_to_dict(['a', 'b', 'c'], [1, 2, 3]))

# ---------------------------------
# ------ 03 List of Squares -------
# ---------------------------------

print("\n--- 03 List of Squares ---")
def list_of_squares():
    return [x**2 for x in range(1, 31)]

print(list_of_squares())


# ------------------------------------
# -- 04 Editing a List Step by Step --
# ------------------------------------

print("\n--- 04 Editing a List Step by Step ---")
def editing_a_list(lst):
    lst.pop()
    lst.insert(1, 'R')
    print("List after a and b:", lst)
    val_to_remove = int(input("Enter a number to remove from the list: "))
    lst.remove(val_to_remove)
    print("List after removing the number:", lst)

editing_a_list([3, 6, 4, 0, 8])


# ------------------------------------
# ----- 05 Merge Two Dictionaries ----
# ------------------------------------

print("\n--- 05 Merge Two Dictionaries ---")
def merge_two_dictionaries(dict1, dict2):
    dict1.update(dict2)
    print("Merged dictionary:", dict1)
    
dict1 = {'a': 1, 'b': 2, 'name': 'Ahmed'}
dict2 = {'c': 3, 'name': 'Fatma'}

merge_two_dictionaries(dict1, dict2)

