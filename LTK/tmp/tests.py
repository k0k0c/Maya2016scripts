dct = {}

keys = ['a', 'b', 'c', 'd']

vA = [1, 0, 0, 4, 5]
vB = [0, 1, 0, 2]
vC = [0, 0, 0]
vD = [0]

nn = (vA, vB, vC, vD)

for key in keys:
    for n in nn:
        for i in n:
            if i != 0:
                dct.setdefault(key, []).append(i)

print dct