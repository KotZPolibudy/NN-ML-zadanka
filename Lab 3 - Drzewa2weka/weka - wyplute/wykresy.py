import glob
import os
import matplotlib.pyplot as plt
import numpy as np

#path = "ograniczone_do_naszych_kryteriow/binarysplitsTrue/"
path = "Wszystkie_Kryteria/binarysplitsTrue/"
path = "dane_por-crossWalidacja/"
wykresy = {}
wykresy['tMMC'] = {}
wykresy['fMMC'] = {}
wykresy['tROC'] = {}
wykresy['fROC'] = {}
wykresy['tAVG'] = {}
wykresy['fAVG'] = {}
best = {}
best['MMC'] = [0, 0, 0, 0]
best['ROC'] = [0, 0, 0, 0]
best['AVG'] = [0, 0, 0, 0]
best['cci'] = [0]
best['ici'] = [0]

m = [0, 5, 10, 20]
xc = []

for filename in os.listdir(path):
    if "Min0" in filename:
        c = filename[10:-4]
        c = "0." + c
        c = float(c)
        xc.append(c)
        #xm = filename[3:-11]
        #print(m)
#xc.remove(xc[-1])
#print(xc)
for M in m:
    for wykres in wykresy:
        wykresy[wykres][M] = []
#print(wykresy)
for filename in os.listdir(path):

    file_path = os.path.join(path, filename)
    check = 0
    file = open(file_path, 'r')
    if "Min0" in filename:
        i = 0
    elif "Min5" in filename:
        i = 5
    elif "Min10" in filename:
        i = 10
    elif "Min20" in filename:
        i = 20
    else:
        continue
    for line in file:
        check -= 1
        if 'Correctly Classified Instances' in line:
            dane = line.split()
            dane = int(dane[3])
            if dane > best['cci'][0]:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['cci'] = [dane, i, c, 't']
        if 'Incorrectly Classified Instances' in line:
            dane = line.split()
            dane = int(dane[3])
            if dane > best['cci'][0]:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['ici'] = [dane, i, c, 't']
        if "F-Measure  MCC      ROC Area" in line:
            #print(filename)
            check = 3
        if check == 0:

            #print(line.split())
            dane = line.split()
            m = "0." + dane[-3][2:]
            m = float(m)
            #print(i, c, m)
            r = "0." + dane[-2][2:]
            r = float(r)
            f = "0." + dane[-4][2:]
            f = float(f)
            if best['MMC'][0] < m:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['MMC'] = [m, i, c, 1]
            if best['ROC'][0] < r:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['ROC'] = [r, i, c, 1]
            if best['AVG'][0] < f:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['AVG'] = [f, i, c, 1]
            wykresy['tAVG'][i].append(f)
            wykresy['tROC'][i].append(r)
            wykresy['tMMC'][i].append(m)
"""
#path = "Wszystkie_Kryteria/binaryspitsfalse/"
path = "ograniczone_do_naszych_kryteriow/binaryspitsfalse/"
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    check = 0
    file = open(file_path, 'r')
    if "Min0" in filename:
        i = 0
    elif "Min5" in filename:
        i = 5
    elif "Min10" in filename:
        i = 10
    elif "Min20" in filename:
        i = 20
    for line in file:
        check -= 1
        if 'Correctly Classified Instances' in line:
            dane = line.split()
            dane = int(dane[3])
            if dane > best['cci'][0]:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['cci'] = [dane, i, c]
        if 'Incorrectly Classified Instances' in line:
            dane = line.split()
            dane = int(dane[3])
            if dane > best['cci'][0]:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['ici'] = [dane, i, c]
        if line == "                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class\n":
            check = 3
        if check == 0:
           # print(line.split())
            dane = line.split()
            m = "0." + dane[-3][2:]
            if '.,' in m:
                m = float('-0.'+m[3:])
            else:
                m = float(m)
            r = "0." + dane[-2][2:]
            r = float(r)
            f = "0." + dane[-4][2:]
            f = float(f)
            wykresy['fAVG'][i].append(f)
            wykresy['fROC'][i].append(r)
            wykresy['fMMC'][i].append(m)
            if best['MMC'][0] < m:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['MMC'] = [m, i, c]
            if best['ROC'][0] < r:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['ROC'] = [r, i, c]
            if best['AVG'][0] < f:
                c = filename[10:-4]
                c = "0." + c
                c = float(c)
                best['AVG'] = [f, i, c]
"""

print(best['MMC'])
print(best['ROC'])
print(best['AVG'])

print("Jaki wykres wariacie?")
co = input()
#co = 1
if co == 'm':
    co = 'tMMC'
    plt.ylabel('MMC')
    plt.suptitle('Zależność MMC od confidenceFactor dla binarySplits = true')
elif co == 'fm':
    co = 'fMMC'
    plt.ylabel('MMC')
    plt.suptitle('Zależność MMC od confidenceFactor dla binarySplits = false')
elif co == 'fr':
    co = 'fROC'
    plt.ylabel('ROC Area')
    plt.suptitle('Zależność ROC od confidenceFactor dla binarySplits = false')
elif co == 'ab':
    co = 'tAVG'
    plt.ylabel('F-Measure')
    plt.suptitle('Zależność średniej F-Measure od confidenceFactor dla binarySplits = true')
elif co == 'fab':
    co = 'fAVG'
    plt.ylabel('F-Measure')
    plt.suptitle('Zależność średniej F-Measure od confidenceFactor dla binarySplits = false')
else:
    co = 'tROC'
    plt.ylabel('ROC Area')
    plt.suptitle('Zależność ROC od confidenceFactor dla binarySplits = true')
points0 = np.array(wykresy[co][0])
points5 = np.array(wykresy[co][5])
points10 = np.array(wykresy[co][10])
points20 = np.array(wykresy[co][20])
xpoints = np.array(xc)
print(xpoints, xc)
print(points0, wykresy[co][0])
plt.xlabel('confidenceFactor')
plt.plot(xpoints, points0, 'o', linestyle = 'dotted', label='minNumObj = 0')
plt.plot(xpoints, points5, 'o', linestyle = 'dotted', label='minNumObj = 5')
plt.plot(xpoints, points10, 'o', linestyle = 'dotted', label='minNumObj = 10')
plt.plot(xpoints, points20, 'o', linestyle = 'dotted', label='minNumObj = 20')
plt.legend()
plt.show()

