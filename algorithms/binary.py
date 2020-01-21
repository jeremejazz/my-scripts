# demo for binary search
import math

def binarysearch(search, sortedlist):
    left = 0
    right = len(sortedlist) -1
    mid = math.ceil(right / 2)
    
    while sortedlist[mid] != search:
        if search > sortedlist[mid]:
            left = mid+1
        else:
            right = mid-1
        mid = left + math.ceil((right - left)/2)
    print(mid)
    

arr = [1,3,44,55,66,78,109]
binarysearch(78,arr)
