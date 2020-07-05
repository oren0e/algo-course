from typing import List
#arr: List[int] = [1, 3, 5, 2, 4, 6]
arr: List[int] = [1, 5, 3, 2, 6, 4]


def count_split_inversions(left: List[int], right: List[int]) -> int:
    pass

def count_and_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    temp_arr: List[int] = [0 for _ in range(n)]
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
    inversions: int = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            temp_arr[k] = left[i]
            i += 1
        else:
            temp_arr[k] = right[j]
            j += 1
            inversions += (len(left) - i)
        k += 1
    for c in range(len(temp_arr)):
        arr[c] = temp_arr[c]

    print(inversions)


# test cases
arr: List[int] = [1,5,3,4,2,6]
arr: List[int] = [1, 20, 6, 4, 5]
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