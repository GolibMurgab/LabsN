x1 = int(input())
x2 = int(input())
x3 = int(input())
x4 = (x2 * x2) - (4 * x1 * x3)
if x4 < 0:
    print("Нет решений")
if x4 == 0:
    print("a = " + str((x2 * -1) / (2 * x1)))
if x4 > 0:
    print("a1 = " + str(((x2 * -1) + x4 ** 0.5) / (2 * x1)) + "\n" + "a2 = " + str(((x2 * -1) - x4 ** 0.5) / (2 * x1)))
