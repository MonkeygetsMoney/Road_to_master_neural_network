import numpy as np

a = np.array([1, 2, 3])
# print(a[0], a[2]) # can access like a list
# print(a) # print out the array

b = np.array([a, [4, 5, 6]]) # can pass existing array into new one
# print(b)

c = np.full((2,2), 7) # a constant array of 7
d = np.eye(2) # 2x2 identity matrix

# can slicing index
a = np.array([[1, 2, 3, 4], 
              [5, 6, 7, 8], 
              [9, 10, 11, 12]]) # 3x4 matrix

b = a[:2, 1:3] # rows (horizontal) and columns (vertical)

row1 = a[1, :] # rank 1 view of the second row | shape (4,)
row2 = a[1:2, :] # rank2 view of the second row | shape (1, 4)
# rank usually refer to the number of axes of an array
# we can see this further in the column examples

col1 = a[:, 1]
col2 = a[:, 1:2]
print(col1)
print(col2)

# array indexing
ex1 = [a[[0, 1, 2], [0, 1, 0]]]
ex2 = [a[0, 0], a[1, 1], a[2, 0]] # these two are equivalent
# print(np.arange(4))

# boolean array indexing
a = np.array([[1, 2], [3, 4], [5, 6]])
bool_idx = a > 2 
# print(bool_idx)
# print(a[bool_idx])

# Datatypes
x = np.array([1, 2], dtype=np.int64)
# data types of int64
# explicitly defined to save memory

# sum
x = np.array([[1, 2], [3, 4]])
# print(np.sum(x))
# print(np.sum(x, axis = 0)) # compute sum of each column
# print(np.sum(x, axis=1)) # compute sum of each row

# Broadcasting
x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
v = np.array([1, 0, 1])
y = x + v # v can behave like a 4x3 as long it had the same columns or rows
print(y)
vv = np.tile(v, (4, 1)) # stack v in 4 rows and 3 columns

y = x + vv # add v to each row of x
