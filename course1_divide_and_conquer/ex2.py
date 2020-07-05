from typing import List


def count_inversions(arr: List[int]) -> int:
    n = len(arr)
    inv_count: int = 0
    if n == 1:
        return 0
    elif n > 1:
        mid = n // 2
        left = arr[:mid]
        right = arr[mid:]

        inv_count += count_inversions(left)  # left
        inv_count += count_inversions(right)   # right

        i = 0
        j = 0
        k = 0

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
        return inv_count


# test cases
arr: List[int] = [1, 20, 6, 4, 5]
print(f'Array before: {arr}')
print(f'Number of inversions is: {count_inversions(arr)}')
print(f'Array after: {arr}')

arr: List[int] = [1, 3, 5, 2, 4, 6]
print(f'Array before: {arr}')
print(f'Number of inversions is: {count_inversions(arr)}')
print(f'Array after: {arr}')

# answer to exercise
ex_arr: List[int] = []
with open('int_array.txt', 'r') as f:
    for line in f:
        ex_arr.append(int(line))

print(f'Number of inversions is: {count_inversions(ex_arr)}')