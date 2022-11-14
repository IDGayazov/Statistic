# импорт библиотеки для работы с Excel
import openpyxl
import math
from scipy.stats import t
from scipy import stats as st
# открыть файл для чтения
book = openpyxl.open('r2z1.xlsx', read_only=True)
sheet = book.active
# коприуем данные из листа в список
data = []
data1 = []
data2 = []
for row in range(2, sheet.max_row + 1):
    data.append(round(sheet[row][0].value - sheet[row][1].value, 2))
    data1.append(sheet[row][0].value)
    data2.append(sheet[row][1].value)

# Student's statistic

T, m0 = 0, 0
sum, sum2 = 0, 0
n = len(data)
for x in data:
   sum += x
   sum2 += x**2
Sx = math.sqrt((sum2/n - (sum/n) ** 2))
T = (sum/n - m0)*math.sqrt(n - 1) / Sx
print("Статистика Стьюдента: " + str(round(T, 2)))

alpha = 0.025
# calculate the critical value
cv = t.ppf(alpha, n - 1)
# calculate the p-value
p = t.cdf(T, n - 1)
print("The critical value ", round(cv, 3))
print("The p-value ", p)
#print(st.ttest_rel(data1, data2, alternative = 'less'))
