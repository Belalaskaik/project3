import random
import time
import matplotlib.pyplot as plt


# 1st Test 10x10
arr1 = [[0 for _ in range(10)] for _ in range(10)]

# 2nd Test 12x12
arr2 = [[0 for _ in range(12)] for _ in range(12)]

# 3rd Test 14x14
arr3 = [[0 for _ in range(14)] for _ in range(14)]

# 4th Test 16x16
arr4 = [[0 for _ in range(16)] for _ in range(16)]

# 5th Test 18x18
arr5 = [[0 for _ in range(18)] for _ in range(18)]

# 6th Test 20x20
arr6 = [[0 for _ in range(20)] for _ in range(20)]

masterArr = [arr1, arr2, arr3, arr4, arr5, arr6]

for i in range(len(masterArr)):
    # Add 11 random "1" values to the array
    count = 0
    while count < 11:
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        if masterArr[i][x][y] == 0:
            masterArr[i][x][y] = 1
            count += 1


grid = masterArr[0]
rows = len(grid)
cols = len(grid[0])
n = rows + cols - 2


# Input: Recieves a binary number (note that it has the 0b prefix) representing a single candidate
# Output: Return 1 for finding successful path with candidate or 0 if not found
def verify(candidate):
    # Split up the binary number into list of chars while also removing the 0b prefix
    candidate = list(candidate)[2:]

    i, j = 0, 0

    # Want to loop through entire length of a candidate string. 15 is the number of moves required for any valid solution
    for k in range(len(candidate)):
        # Move down
        if candidate[k] == "0":
            i += 1
            # ERROR: Found an opponent or went outside of boundary
            if (i > rows - 1) or (grid[i][j] == 1):
                return 0
        # Move right
        if candidate[k] == "1":
            j += 1
            # ERROR: Found an opponent or went outside of boundary
            if (j > cols - 1) or (grid[i][j] == 1):
                return 0

    # Determine if bit combination led us to bottom right corner
    if (i == rows - 1) and (j == cols - 1):
        return 1
    else:
        return 0


# Input: NULL
# Output: Returns an integer representing how many successful candidates were found
# Description: This is an exhaustive search function that generates every possible bit
#              string candidate and verifies if each one 'crosses the field'
def exsearch():
    moves = 2**n - 1
    counter = 0

    # Looping through every possible bit string
    # Add one since range() is exclusive on endpoints
    for i in range(1, moves + 1):
        candidate = bin(i)
        counter += verify(candidate)

    return counter


# Input:
# Output:
# Description:
def dynsearch():
    # Starting square has an opponent: NOT VALID
    if grid[0][0] == 1:
        return 0
    dyngrid = [[0 for x in range(cols)] for y in range(rows)]

    # Base Case
    dyngrid[0][0] = 1

    for i in range(0, rows):
        for j in range(0, cols):
            # Opponent found: Any paths ending up here are NOT VALID
            if grid[i][j] == 1:
                dyngrid[i][j] = 0
                continue
            above = 0
            left = 0
            # Calculate the above element in the new grid
            if i > 0 and grid[i][j] == 0:
                above = dyngrid[i - 1][j]
            # Calculate the left element from the new grid
            if j > 0 and grid[i][j] == 0:
                left = dyngrid[i][j - 1]
            dyngrid[i][j] += above + left

    return dyngrid[rows - 1][cols - 1]


exhXvalues = []
dynXvalues = []
exhYvalues = []
dynYvalues = []

for i in range(len(masterArr)):
    grid = masterArr[i]
    rows = len(grid)
    cols = len(grid[0])
    n = rows + cols - 2

    print(f"N-value is {n}")
    start_time = time.time()
    exsearch()
    end_time = time.time()

    time1 = end_time - start_time

    start_time = time.time()
    dynsearch()
    end_time = time.time()

    time2 = end_time - start_time

    print(f"Time 1: {time1}, Time 2: {time2}\n")

    exhXvalues.append(n)
    dynXvalues.append(n)
    exhYvalues.append(time1)
    dynYvalues.append(time2)

fig, (ax1, ax2) = plt.subplots(ncols=2)

ax1.scatter(exhXvalues, exhYvalues)
ax1.set_title("Exhaustive Search")
ax1.set_xlabel("Values of N")
ax1.set_ylabel("Time (ms)")

ax2.scatter(dynXvalues, dynYvalues)
ax2.set_title("Dynamic Programming")
ax1.set_xlabel("Values of N")
ax1.set_ylabel("Time (ms)")

plt.savefig("scatterplots.png")
