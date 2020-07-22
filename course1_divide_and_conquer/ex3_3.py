'''
Find test cases at
https://github.com/beaunus/stanford-algs/blob/master/testCases/course1/assignment3Quicksort
'''

from typing import List, Optional

class QuickSort(object):

    def __init__(self, choice):
        self.comparisons = 0
        self.choice = choice
        self.median = 0     # for debugging
        self.mid = 0    # for debugging

    def determine_median(self, arr: List[int]) -> int:
        '''
        Returns the value of the median of arr.
        The assumption here is that arr is of length 3
        '''
        # check length
        assert len(arr) == 3, "length must be equal to 3"

        max_ind: int = 0
        max_num: int = 0
        min_ind: int = 0
        min_num: float = float('inf')
        for i in range(3):
            if arr[i] > max_num:
                max_num = arr[i]
                max_ind = i
            if arr[i] < min_num:
                min_num = arr[i]
                min_ind = i
        mid_index = list(set([0, 1, 2]).difference(set([min_ind, max_ind])))[0]
        return arr[mid_index]

    def choose_pivot(self, arr: List[int], left: int, right: int) -> None:
        if self.choice == "left":
            piv = left
        elif self.choice == "right":
            piv = right - 1
        elif self.choice == "median":
            if (right - left) % 2 == 0:
                mid: int = (left + (right - left) // 2) - 1
            else:
                mid: int = left + (right - left) // 2

            #mid: int = left + (right - left)//2
            # determine median value
            mid_value = self.determine_median([arr[left], arr[mid], arr[right-1]])
            self.mid = arr[mid]         # for debugging
            self.median = mid_value     # for debugging
            piv = arr.index(mid_value)
        else:
            raise ValueError('Invalid choice')

        arr[left], arr[piv] = arr[piv], arr[left]

    def partition(self, arr: List[int], left: int, right: int) -> int:
        pivot: int = arr[left]
        i: int = left + 1

        for j in range(left + 1, right):
            try:
                if arr[j] < pivot:
                    arr[j], arr[i] = arr[i], arr[j]
                    i += 1
            except IndexError:
                break

        arr[left], arr[i-1] = arr[i-1], arr[left]
        return i-1

    def quicksort(self, arr: List[int], left: int, right: int) -> Optional[List[int]]:
        if (left >= right):
            return None
        self.choose_pivot(arr, left, right)
        pivot = self.partition(arr, left=left, right=right)
        self.comparisons += right - left - 1
        #print(f'Select {self.median} from left: {arr[left]} middle: {self.mid} right: {arr[right-1]}'
        #      f'\nComparisons: {self.comparisons} right-left: {right-left}')

        self.quicksort(arr, left=left, right=pivot)
        self.quicksort(arr, left=(pivot+1), right=right)

    def get_num_of_comparisons(self) -> int:
        return self.comparisons

# test median choice
# arr = [8, 2, 4, 5, 7, 1]
# arr1 = [1, 6, 8, 10, 7, 5, 2, 9, 4, 3]
# arr2 = [2,1,12,13,16,10,9,5,18,8,17,20,19,3,4,11,14,6,7,15]
# qs = QuickSort(choice='median')
# qs.choose_pivot(arr, left=0, right=len(arr))
# assert arr[0] == 4
# qs.choose_pivot(arr1, left=0, right=len(arr1))
# assert arr1[0] == 3
# qs.choose_pivot(arr2, left=0, right=len(arr2))
# assert arr2[0] == 8

# my tests
arr = [4, 5, 2, 3, 1]
arr1 = [1, 6, 8, 10, 7, 5, 2, 9, 4, 3]
arr2 = [2,1,12,13,16,10,9,5,18,8,17,20,19,3,4,11,14,6,7,15]     # with 'median' should be 56 comparisons
arr3 = [2, 20, 1, 15, 3, 11, 13, 6, 16, 10, 19, 5, 4, 9, 8, 14, 18, 17, 7, 12]

qs = QuickSort(choice='median')
qs.quicksort(arr2, left=0, right=(len(arr2)))
print(arr2)
assert qs.get_num_of_comparisons() == 56

# debug on the first 100 elements
comp_arr: List[int] = []
with open('quicksort.txt', 'r') as f:
    for line in f:
        comp_arr.append(int(line))
comp_arr = comp_arr[0:100]

qs = QuickSort(choice='median')
qs.quicksort(comp_arr, left=0, right=len(comp_arr))



# final test cases for all 3 parts
# arr
arr = [4, 5, 2, 3, 1]
qs = QuickSort(choice='left')
qs.quicksort(arr, left=0, right=(len(arr)))
assert arr == sorted(arr)
assert qs.get_num_of_comparisons() == 7

arr = [4, 5, 2, 3, 1]
qs = QuickSort(choice='right')
qs.quicksort(arr, left=0, right=(len(arr)))
assert arr == sorted(arr)
assert qs.get_num_of_comparisons() == 8

arr = [4, 5, 2, 3, 1]
qs = QuickSort(choice='median')
qs.quicksort(arr, left=0, right=(len(arr)))
assert arr == sorted(arr)
assert qs.get_num_of_comparisons() == 6

# arr1
arr1 = [1, 6, 8, 10, 7, 5, 2, 9, 4, 3]
qs = QuickSort(choice='left')
qs.quicksort(arr1, left=0, right=(len(arr1)))
assert arr1 == sorted(arr1)
assert qs.get_num_of_comparisons() == 26

arr1 = [1, 6, 8, 10, 7, 5, 2, 9, 4, 3]
qs = QuickSort(choice='right')
qs.quicksort(arr1, left=0, right=(len(arr1)))
assert arr1 == sorted(arr1)
assert qs.get_num_of_comparisons() == 21

arr1 = [1, 6, 8, 10, 7, 5, 2, 9, 4, 3]
qs = QuickSort(choice='median')
qs.quicksort(arr1, left=0, right=(len(arr1)))
assert arr1 == sorted(arr1)
assert qs.get_num_of_comparisons() == 21

# test on file
comp_arr: List[int] = []
with open('quicksort.txt', 'r') as f:
    for line in f:
        comp_arr.append(int(line))

qs = QuickSort(choice='left')
qs.quicksort(comp_arr, left=0, right=len(comp_arr))
print(qs.get_num_of_comparisons())

comp_arr: List[int] = []
with open('quicksort.txt', 'r') as f:
    for line in f:
        comp_arr.append(int(line))

qs = QuickSort(choice='right')
qs.quicksort(comp_arr, left=0, right=len(comp_arr))
print(qs.get_num_of_comparisons())

comp_arr: List[int] = []
with open('quicksort.txt', 'r') as f:
    for line in f:
        comp_arr.append(int(line))

qs = QuickSort(choice='median')
qs.quicksort(comp_arr, left=0, right=len(comp_arr))
print(qs.get_num_of_comparisons())