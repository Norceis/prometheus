import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns;

sns.set_theme()

methods = ['AM1', 'RM1', 'DFTB3', 'PM3', 'PM6']
levels = ['1', '2', '3', '4', '5']
samples = ['B', 'C']
localdir = 'directory'

# tworzenie df dla każdej próbki - B i C to średnie długości wiązania, i ich std w innym df
B = pd.DataFrame(columns=methods, index=levels, dtype=int)
C = pd.DataFrame(columns=methods, index=levels, dtype=int)
Bstd = pd.DataFrame(columns=methods, index=levels, dtype=int)
Cstd = pd.DataFrame(columns=methods, index=levels, dtype=int)

# distance, angle, rmsd
for sample in samples:
    for level in levels:
        for method in methods:
            if sample == 'B':
                df = pd.read_fwf(localdir + '/12/' + sample + level + method + '.dat')
                value = df.iloc[:, 1]
                std = df.iloc[:, 1].std()
                B.loc[level, method] = float(format(value.mean().round(3), '.3f'))
                Bstd.loc[level, method] = float(format(std.round(3), '.3f'))
            else:
                df = pd.read_fwf(localdir + '/12/' + sample + level + method + '.dat')
                value = df.iloc[:, 1]
                std = df.iloc[:, 1].std()
                C.loc[level, method] = float(format(value.mean().round(3), '.3f'))
                Cstd.loc[level, method] = float(format(std.round(3), '.3f'))
B = B.transpose()
B = np.asarray(B)
Bstd = Bstd.transpose()
Bstd = np.asarray(Bstd)
C = C.transpose()
C = np.asarray(C)
Cstd = Cstd.transpose()
Cstd = np.asarray(Cstd)

labelsB = np.asarray(["{0:.3f} ± {1:.3f}".format(float(B), float(Bstd))
                      for B, Bstd in zip(B.flatten(), Bstd.flatten())]).reshape(5, 5)
labelsC = np.asarray(["{0:.3f} ± {1:.3f}".format(float(C), float(Cstd))
                      for C, Cstd in zip(C.flatten(), Cstd.flatten())]).reshape(5, 5)

fig, ax = plt.subplots()
heatmap = sns.heatmap(B, xticklabels=levels, yticklabels=methods, annot=labelsB, fmt='', cmap='Reds_r')
heatmap = sns.heatmap(B, xticklabels=levels, yticklabels=methods, annot=labelsB, fmt='', cmap='Reds_r', vmin=3.5, vmax=4.5)
heatmap = sns.heatmap(C, xticklabels=levels, yticklabels=methods, annot=labelsC, fmt='', cmap='YlOrBr')
heatmap = sns.heatmap(C, xticklabels=levels, yticklabels=methods, annot=labelsC, fmt='', cmap='YlOrBr_r', vmin=0.87, vmax=1.13)
plt.xlabel('Model')
plt.ylabel('Metoda')
plt.yticks(rotation=0)
plt.show()

df = pd.read_fwf(localdir + '/5/Cprod.dat')
value = df.iloc[:, 1].mean()
std = df.iloc[:, 1].std()
print(str(value.round(3)) + ' ' + str(std.round(3)))

# wypełnianie tabel danymi hbonds
for sample in samples:
    for level in levels:
        for method in methods:
            if sample == 'B':
                df = pd.read_fwf(localdir + '/11/' + sample + level + method + '.dat')
                if df.empty:
                    df = pd.DataFrame(np.zeros((3,7)))
                value = df.iloc[0, 4]
                std = df.iloc[0, 5]
                B.loc[level, method] = float(format(value.round(3), '.3f'))
                Bstd.loc[level, method] = float(format(std.round(3), '.3f'))
            else:
                df = pd.read_fwf(localdir + '/11/' + sample + level + method + '.dat')
                if df.empty:
                    df = pd.DataFrame(np.zeros((3,7)))
                value = df.iloc[0, 4]
                std = df.iloc[0, 5]
                C.loc[level, method] = float(format(value.round(3), '.3f'))
                Cstd.loc[level, method] = float(format(std.round(3), '.3f'))
B = B*100
C = C*100
B = B.transpose()
B = np.asarray(B)
Bstd = Bstd.transpose()
Bstd = np.asarray(Bstd)
C = C.transpose()
C = np.asarray(C)
Cstd = Cstd.transpose()
Cstd = np.asarray(Cstd)

labelsB = np.asarray(["{0:.0f}, {1:.3f}".format(float(B), float(Bstd))
                      for B, Bstd in zip(B.flatten(), Bstd.flatten())]).reshape(5, 5)
labelsC = np.asarray(["{0:.0f}, {1:.3f}".format(float(C), float(Cstd))
                      for C, Cstd in zip(C.flatten(), Cstd.flatten())]).reshape(5, 5)
fig, ax = plt.subplots()
heatmap = sns.heatmap(B, xticklabels=levels, yticklabels=methods, annot=labelsB, fmt='', cmap='Reds')
heatmap = sns.heatmap(C, xticklabels=levels, yticklabels=methods, annot=labelsC, fmt='', cmap='YlOrBr')

plt.xlabel('Model')
plt.ylabel('Metoda')
plt.yticks(rotation=0)
plt.show()
df = pd.read_fwf(localdir + '/11/Cprod.dat')
value = df.iloc[0, 4]
std = df.iloc[0, 5]
value = value*100
print(str(value.round(3)) + ' ' + str(std.round(3)))

# rmsf
# mm
Bprod = pd.read_fwf(localdir + '/13/Bprod.dat')
Cprod = pd.read_fwf(localdir + '/13/Cprod.dat')
fig, ax = plt.subplots()

data = Bprod.join(Cprod['AtomicFlx'], how='right', lsuffix='Bprod', rsuffix='Cprod')
sns.lineplot(data=data, x='#Res', y='AtomicFlxBprod', color='r', linewidth=2)
sns.lineplot(data=data, x='#Res', y='AtomicFlxCprod', color='y', linewidth=2)

plt.xlabel('Numer reszty aminokwasowej')
plt.ylabel('Średnie standardowe odchylenie pozycji [Å]')
ax.legend(['DBP', 'DCP'])
plt.xticks([0, 25, 36, 50, 75, 106, 107, 130, 150, 175, 200, 225, 250, 270, 300],
           [0, 25, 'Asn38', 50, 75, 'Asp108 Trp109', '', 'Glu132', 150, 175, 200, 225, 250, 'His272', 300])
plt.yticks([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5])
plt.xlim(-5,300)
plt.show()
# qmmm
fig, ax = plt.subplots()
for sample in ['B']:
    for method in ['PM3']:
        one = pd.read_fwf(localdir + '/13/' + sample + '1' + method + '.dat')
        two = pd.read_fwf(localdir + '/13/' + sample + '2' + method + '.dat')
        three = pd.read_fwf(localdir + '/13/' + sample + '3' + method + '.dat')
        four = pd.read_fwf(localdir + '/13/' + sample + '4' + method + '.dat')
        five = pd.read_fwf(localdir + '/13/' + sample + '5' + method + '.dat')
        data = one.join(two['AtomicFlx'], how='right', lsuffix='one', rsuffix='two')
        data = data.join(three['AtomicFlx'], how='right', rsuffix='three')
        data = data.join(four['AtomicFlx'], how='right', rsuffix='four')
        data = data.join(five['AtomicFlx'], how='right', rsuffix='five')
        sns.lineplot(data=data, x='#Res', y='AtomicFlxone', color='r', linewidth=2)
        sns.lineplot(data=data, x='#Res', y='AtomicFlxtwo', color='g', linewidth=2)
        sns.lineplot(data=data, x='#Res', y='AtomicFlx', color='b', linewidth=2)
        sns.lineplot(data=data, x='#Res', y='AtomicFlxfour', color='y', linewidth=2)
        sns.lineplot(data=data, x='#Res', y='AtomicFlxfive', color='#8B008B', linewidth=2)
        plt.xlabel('Numer reszty aminokwasowej')
        plt.ylabel('Średnie standardowe odchylenie pozycji [Å]')
        ax.legend(['Model 1' + method, 'Model 2' + method, 'Model 3' + method, 'Model 4' + method, 'Model 5' + method])
        plt.xticks([0, 25, 36, 50, 75, 106, 107, 130, 150, 175, 200, 225, 250, 270, 300],
                   [0, 25, 'Asn38', 50, 75, 'Asp108 Trp109', '', 'Glu132', 150, 175, 200, 225, 250, 'His272', 300])
        plt.yticks([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5])
        plt.xlim(-5,300)

        plt.show()
        print(data)

#scattersy mm
Bprod = pd.read_fwf(localdir + '/6/Bprod.dat')
Cprod = pd.read_fwf(localdir + '/6/Cprod.dat')
fig, ax = plt.subplots()

data = Bprod.join(Cprod['X-C-C-X'], how='right', lsuffix='Bprod', rsuffix='Cprod')
sns.scatterplot(data=data, x='#Frame', y='X-C-C-XBprod', color='r', marker='o', linewidth=0, alpha=0.7)
sns.scatterplot(data=data, x='#Frame', y='X-C-C-XCprod', color='y', marker='o', linewidth=0, alpha=0.7)

plt.xlabel('Numer klatki')
plt.ylabel('Kąt dwuścienny X11-C7-C5-X10 [°]')
ax.legend(['DBP', 'DCP'])
figure = plt.gcf()
figure.set_size_inches(10,6)
plt.savefig("MM.png", dpi=300)
plt.show()

# scattersy qm
for sample in samples:
    for method in methods:
        plt.clf()
        fig, ax = plt.subplots()
        one = pd.read_fwf(localdir + '/6/' + sample + '1' + method + '.dat')
        two = pd.read_fwf(localdir + '/6/' + sample + '2' + method + '.dat')
        three = pd.read_fwf(localdir + '/6/' + sample + '3' + method + '.dat')
        four = pd.read_fwf(localdir + '/6/' + sample + '4' + method + '.dat')
        five = pd.read_fwf(localdir + '/6/' + sample + '5' + method + '.dat')
        data = one.join(two['X-C-C-X'], how='right', lsuffix='one', rsuffix='two')
        data = data.join(three['X-C-C-X'], how='right', rsuffix='three')
        data = data.join(four['X-C-C-X'], how='right', rsuffix='four')
        data = data.join(five['X-C-C-X'], how='right', rsuffix='five')
        sns.scatterplot(data=data, x='#Frame', y='X-C-C-Xone', color='r', marker='o', linewidth=0, alpha=0.7)
        sns.scatterplot(data=data, x='#Frame', y='X-C-C-Xtwo', color='g', marker='o', linewidth=0, alpha=0.7)
        sns.scatterplot(data=data, x='#Frame', y='X-C-C-X', color='b', marker='o', linewidth=0, alpha=0.7)
        sns.scatterplot(data=data, x='#Frame', y='X-C-C-Xfour', color='y', marker='o', linewidth=0, alpha=0.7)
        sns.scatterplot(data=data, x='#Frame', y='X-C-C-Xfive', color='#8B008B', marker='o', linewidth=0, alpha=0.7)
        plt.xlabel('Numer klatki')
        plt.ylabel('Kąt dwuścienny X11-C7-C5-X10 [°]')
        ax.legend(['Model 1' + method, 'Model 2' + method, 'Model 3' + method, 'Model 4' + method, 'Model 5' + method])
        figure = plt.gcf()
        figure.set_size_inches(10,6)
        plt.savefig(sample + method + ".png", dpi=300)
        plt.show()

