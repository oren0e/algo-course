from typing import List, Optional

class QuickSort(object):

    def __init__(self, choice):
        self.comparisons = 0
        self.choice = choice

    def choose_pivot(self, arr: List[int], left: int, right: int) -> None:
        if self.choice == "left":
            piv = left
        elif self.choice == "right":
            piv = right - 1
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
                #self.comparisons += 1
                break

        arr[left], arr[i-1] = arr[i-1], arr[left]
        return i-1

    def quicksort(self, arr: List[int], left: int, right: int) -> Optional[List[int]]:
        if left >= right:
            return None
        self.choose_pivot(arr, left, right)
        pivot = self.partition(arr, left=left, right=right)
        self.comparisons += right - left - 1
        self.quicksort(arr, left=left, right=pivot)
        self.quicksort(arr, left=(pivot+1), right=right)

    def get_num_of_comparisons(self) -> int:
        return self.comparisons

# my tests
arr = [4, 5, 2, 3, 1]
arr1 = [1,6,8,10,7,5,2,9,4,3]

qs = QuickSort(choice='left')
qs.quicksort(arr, left=0, right=(len(arr)))
print(arr)
qs.get_num_of_comparisons()







qs = QuickSort(choice='left')
qs.quicksort(arr, left=0, right=(len(arr)))
assert arr == sorted(arr)
assert qs.get_num_of_comparisons() == 7

qs = QuickSort(choice='left')
qs.quicksort(arr1, left=0, right=(len(arr1)))
assert arr1 == sorted(arr1)
assert qs.get_num_of_comparisons() == 26