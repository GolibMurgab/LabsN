x1 = int(input())
x2 = int(input())
x3 = int(input())
x4 = (x2 * x2) - (4 * x1 * x3)
if x4 < 0:
    print("Нет корней")
if x4 == 0:
    print("X = " + str((b * -1) / (2 * a)))
if x4 > 0:
    print("X1 = " + str(((b * -1) + d ** 0.5) / (2 * a)) + "\n" + "X2 = " + str(((b * -1) - d ** 0.5) / (2 * a)))