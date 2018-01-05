a = ['a', 'b', 'c', 'd', 'e']
b = ['e', 'd', 'c', 'b', 'a'] #b is always listed as a in reverse.


def switch(ind1, ind2):
    '''takes the indices of the two elements in a and switches them in both lists.
       Note: switching the same index doesn't work.'''
    b_ind1 = len(a) - ind2 - 1
    b_ind2 = len(a) - ind1 - 1
    a[ind1], a[ind2] = a[ind2], a[ind1]
    move(b_ind1) #move the value at b_ind1 to the front of list.
    for _ in range(b_ind2-b_ind1-1):
        i = b_ind2-1
        move(i)
    move(b_ind2)
    for _ in range(b_ind1):
        i = b_ind2
        move(i)
    print(a)
    print(b)
        

def move(i):
    '''moves a value at a given index i to the front of list b'''
    b.insert(0, b[i])
    b.pop(i+1)
