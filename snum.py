import csv
import numpy as np
import scipy.signal as signal

# Number of Probes
n = 5

time = []
U = [[] for _ in range(n)]
p = [[] for _ in range(n)]

with open('test4/U.csv', mode = 'r') as file:
    reader = csv.reader(file)
    for i in range(7):
        next(reader)
    for row in reader:
        newRow = row[0].split('             ')
        for i in range(len(newRow)):
            newRow[i] = newRow[i].strip()
        time.append(float(newRow[0]))
        for i in range(1, len(newRow)):
            item = newRow[i].replace('(', '').replace(')', '').split(' ')
            U[i-1].append([float(item[0]), float(item[1]), float(item[2])])

def isBlank(s):
    return s != ''

with open('test4/p.csv', mode = 'r') as file:
    reader = csv.reader(file)
    for i in range(7):
        next(reader)
    for row in reader:
        items = row[0].split(' ')
        for i in range(len(items)):
            items[i] = items[i].strip()
        items = list(filter(isBlank, items))
        for i in range(len(items)):
            p[i-1].append(float(items[i]))

def strauhal_number(pressures, velocities, characteristic_length):
    velocity_magnitudes = [np.linalg.norm(v) for v in velocities]

    freq, Cl_amp = signal.welch(pressures, 1./(time[1]-time[0]), nperseg=2048)

    Cl_max = np.argmax(np.abs(Cl_amp))
    freq_shed = freq[Cl_max]
    s_num = freq_shed * characteristic_length / np.average(velocity_magnitudes)
    return s_num

for i in range(1, n - 1):
    print("Strauhal Number", strauhal_number(p[i], U[i], 1.0))
    
