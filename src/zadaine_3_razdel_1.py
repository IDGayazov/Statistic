import openpyxl
book = openpyxl.open("r3z1.xlsx", read_only = True)
sheet = book.active
data = []
for row in range(2, sheet.max_row + 1):
    data.append(sheet[row][0].value)

n = len(data)
X = 0
for t in data:
    X += t / n
X = round(X, 3)
print("Выборочное среднее ", X)
theta = round((7/3 - X) / 2, 3)
print("Оценка параметра по методу моментов", theta)







