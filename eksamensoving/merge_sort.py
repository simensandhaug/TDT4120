from math import floor, inf

def merge(A, L, R, n):
    i = j = 0
    for k in range(n):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1

def merge_sort(A, n):
    if n > 1:
        mid = floor(n/2)
        L = A[:mid] # Left half of A
        R = A[mid:] # Right half of A
        merge_sort(L, len(L)) 
        merge_sort(R, len(R))
        merge(A, L + [inf], R + [inf], n)

# Test the function
A = [1, 3, 5, 2, 4, 6]
print("Original array:", A)
merge_sort(A, len(A))
print("Sorted array:", A)
