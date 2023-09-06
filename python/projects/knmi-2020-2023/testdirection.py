import math

def winddiff(src, dest):
    diff = dest - src
    if diff < -170:
        diff = 360 + diff
    if diff > 180:
        diff = diff - 360
    return diff

print(winddiff(10, 20))
print(winddiff(10, 0))
print(winddiff(10, 190))
print(winddiff(10, 200))

print(winddiff(20, 10))
print(winddiff(0, 10))
print(winddiff(170, 10))
print(winddiff(190, 10))
print(winddiff(200, 10))







