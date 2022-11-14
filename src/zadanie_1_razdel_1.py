import openpyxl
import math
# библиотеки для работы с статистическими данными
import numpy as np
import matplotlib.pylab as plt
from scipy.stats import norm, chi2
import scipy

def vk(data: list, start: float, end: float):
    '''подсчет количества элементов выборки в интервале'''
    count = 0
    for x in data:
        if (start < x <= end):
            count += 1
    return count

def normal_dist(x: float):
    '''функция плотности стандартного нормального распределения'''
    prob_density = (np.exp(-0.5 * (x)**2)) / math.sqrt(2 * np.pi)
    return prob_density

# открыть файл для чтения
book = openpyxl.open('r2z2.xlsx', read_only=True)
# позиционирование на листе
sheet = book.active
# коприуем данные из листа в список
data = []
for row in range(2, sheet.max_row + 1):
    data.append(sheet[row][0].value)

# построение гистограммы
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot()
n, bins, pitches = ax.hist(data, bins=7, density=True)
ax.xaxis.set_major_locator(plt.IndexLocator(base=(max(data) - min(data)) / 7, offset=0))
for i in pitches:
    height = round(i.get_height(), 3)
    ax.annotate(height, (i.get_x() + 0.05, height+0.001))
ax.grid()

# выборочное среднее
sum = 0
for x in data:
    sum += x
mean = round(sum / len(data), 3)
print("Выборочное среднее ", mean)

#выборочная дисперсия
sum = 0
for x in data:
    sum += (x - mean)**2
disp = round(sum / len(data), 3)
print("Выборочная дисперсия ", disp)

# Выборочное стандартное отклонение
sigma = round(math.sqrt(disp), 3)
print("Выборочное стандартное отклонение", sigma)


# график теоретичесой функции плотности
x_axis = np.arange(min(data), max(data), 0.001)
plt.plot(x_axis, norm.pdf(x_axis, mean, sigma))
plt.show()

step = round((max(data) - min(data)) / math.ceil(len(data)/10), 3)
r = math.ceil(len(data)/10)
T = 0
count = 1
n = len(data)
left = min(data) - 0.001
right = left + step
while count <= r:
    if count == 1:
        pk = norm(loc = mean, scale = sigma).cdf(right)
        T += ((vk(data, left, right) - n * pk) ** 2) / (n * pk)
    elif count == r:
        pk = 1 - norm(loc = mean, scale = sigma).cdf(left)
        T += ((vk(data, left, right) - n * pk) ** 2) / (n * pk)
    else:
        pk = norm(loc = mean, scale = sigma).cdf(right) - norm(loc = mean, scale = sigma).cdf(left)
        T += ((vk(data, left, right) - n * pk) ** 2) / (n * pk)
    left = right
    right += step
    count += 1
print("Статистика хи-квадрат ", round(T, 2))
# вычисление критической константы
print("Критическая константа ", round(chi2.ppf(0.9, r-3), 2))
# р-значение
print("p1-value", round(1 - chi2.cdf(T, r-3), 3))
print("p2-value", round(1 - chi2.cdf(T, r-1), 3))