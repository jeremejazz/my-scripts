# demo for binary search
import math

def binarysearch(search, sortedlist):
    left = 0
    right = len(sortedlist) -1
    mid = math.ceil((right + left) / 2)
    
    while sortedlist[mid] != search:
        if search > sortedlist[mid]:
            left = mid+1
        else:
            right = mid-1
        mid = math.ceil((right + left)/2)
    return mid 

arr = [1,3,4,5,44,55,66,78,109,1000]
print(binarysearch(3,arr))
