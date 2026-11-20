"""
Some random code snippets for different Big-O runtimes
"""

#####################################################
# Constant Time O(1) ################################
#####################################################

x = 0
if not x % 2:
    print("even!")
else:
    print("odd!")
    
#####################################################
# Linear Time O(N) ##################################
#####################################################

# Example 1
N = 1_000_000
total = 0
for i in range(N):
    total += N
print(total)

# Other, more complicated, example
x = 0
if not x % 2:
    N = 1_000_000
    total = 0
    for i in range(N):
        total += N
        print(total)
else:
    print("odd!")


#####################################################
# Quadratic Time O(N^2) #############################
#####################################################

N = 1_000_000
M = 1_000
total = 0
for ii in range(N):
    for jj in range(M):
        total += ii*jj
print(total)

#####################################################
# Cubic Time O(N^3) #################################
#####################################################

N = 100
M = 100
T = 100
total = 0
for ii in range(N):
    for jj in range(M):
        for kk in range(T):
            total += ii*jj
print(total)


#####################################################
# Logarithmic Time O(log N) #########################
#####################################################

# Recursive Binary Search

def search(arr, el, rr, x):
    if rr >= el:
        mid = el + (rr - el) // 2
        if arr[mid] == x:
            return mid
        if arr[mid] > x:
            return search(arr, el, mid-1, x)
        return search(arr, mid+1, rr, x)
    return

N = 10_000
arr=list(range(0, N, 2));
print(search(arr, 0, len(arr), 26))

#####################################################
# Exponential Time O(2^N) ###########################
#####################################################

def generate_subsets(arr):
    n = len(arr)
    for i in range(1 << n): # NOTE: this is a python bit shift, a clever way of saying range(2**n)
        subset = []
        for j in range(n):
            if i & (1 << j):
                subset.append(arr[j])
        print(subset)

#####################################################
# Factorial Runtime O(N!) ###########################
#####################################################

def permute(arr, l, r):
    if l == r:
        print(arr[:r + 1])
    else:
        for i in range(l, r + 1):
            arr[l], arr[i] = arr[i], arr[l]
            permute(arr, l + 1, r)
            arr[l], arr[i] = arr[i], arr[l]

# A commented example of the above function for explanation
def permute(arr, l, r):
    if l == r:
        print(arr[:r + 1])  # found a complete permutation
    else:
        for i in range(l, r + 1):
            arr[l], arr[i] = arr[i], arr[l]   # swap current element to front
            permute(arr, l + 1, r)             # recurse on remaining elements
            arr[l], arr[i] = arr[i], arr[l]   # backtrack (swap back)
            # NOTE: N choices at first level, N-1 at next, ... → N! total permutations


#####################################################
# Coordinate Crossmatching ##########################
# O(NlogN) Runtime ##################################
#####################################################

from scipy.spatial import KDTree
import numpy as np

def crossmatch(catalog_a, catalog_b, max_sep):
    """
    Find the nearest neighbor in catalog_b for each star in catalog_a.
    catalog_a, catalog_b: arrays of (ra, dec) coordinates in degrees
    max_sep: maximum separation to count as a match (degrees)
    Returns list of (index_a, index_b, distance) for matches.
    """
    tree = KDTree(catalog_b)
    distances, indices = tree.query(catalog_a, distance_upper_bound=max_sep)

    matches = []
    for i, (dist, j) in enumerate(zip(distances, indices)):
        if dist < max_sep:
            matches.append((i, j, dist))

    return matches


def crossmatch_slow(catalog_a, catalog_b, max_sep):
    """
    Find the nearest neighbor in catalog_b for each star in catalog_a.
    catalog_a, catalog_b: arrays of (ra, dec) coordinates in degrees
    max_sep: maximum separation to count as a match (degrees)
    Returns list of (index_a, index_b, distance) for matches.
    """
    matches = []

    # Compare every star in A against every star in B — O(N^2)
    for i, star_a in enumerate(catalog_a):
        best_dist = max_sep
        best_j = None

        for j, star_b in enumerate(catalog_b):
            dist = np.sqrt((star_a[0] - star_b[0])**2 + (star_a[1] - star_b[1])**2)
            if dist < best_dist:
                best_dist = dist
                best_j = j

        if best_j is not None:
            matches.append((i, best_j, best_dist))

    return matches
