from typing import List
arr: List[int] = [1, 3, 5, 2, 4, 6]
#arr: List[int] = [1, 5, 3, 2, 4, 6]


def count_split_inversions(left: List[int], right: List[int]) -> int:
    pass

def count_and_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    if n == 1:
        return arr
    mid = n // 2
    left = arr[:mid]
    right = arr[mid:]

    count_and_sort(left)
    count_and_sort(right)

    i = 0
    j = 0
    k = 0
    inversions: List[int] = []

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
            inversions.extend([len(left) - i])
        k += 1
    print(inversions)

count_and_sort(arr)

def count_inversions(arr: List[int]) -> int:
    n = len(arr)
    if n == 1:
        return 0
    elif n == 2:
        if arr[0] > arr[1]:
            temp = arr[0]
            arr[0] = arr[1]
            arr[1] = temp
    else:
        b = count_inversions(arr[0:(len(arr)//2)])  # left
        c = count_inversions(arr[(len(arr)//2):])   # right
        z = count_split_inversions(arr)     # split
    return b

count_inversions(arr)