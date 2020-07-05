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
    if n > 1:
        mid = n // 2
        left = arr[:mid]
        right = arr[mid:]

        x = count_inversions(left)  # left
        y = count_inversions(right)   # right

        i = 0
        j = 0
        k = 0
        inv_count: int = 0

        while (i < len(left)) and (j < len(right)):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                inv_count += (len(left) - i)
                j += 1

            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
        print(inv_count)

#arr: List[int] = [83, 20, 9, 50, 115, 61, 17]
arr: List[int] = [1, 20, 6, 4, 5]
print(f'Array before: {arr}')
count_inversions(arr)
print(f'Array after: {arr}')