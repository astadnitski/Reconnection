import matplotlib.pyplot as mp
import numpy as np
import pandas as pd

def locate(t): mp.plot([t, t], [-6, 6], color = 'w')

v = np.loadtxt('vlinesCSV/v0001284.csv', delimiter = ',')
vlines = [[0] * (2 * len(v)) for i in range(2 * 845)]
ycentre = [0] * (2 * 845) 

t_ar, Z_ar = [], []
x_t, x_z = [], []
o_t, o_z = [], []

t = 0

while t < len(vlines):
    
    # Set index, scan data
    idx = int(662 + t / 2)
    v = np.loadtxt('vlinesCSV/v' + str(idx).zfill(7) + '.csv', delimiter = ',')
    d = pd.DataFrame(pd.read_csv('staglinesCSV/coords' + str(idx).zfill(7) + '.csv'))

    # Get V_z color background
    vlines[t] = v
    vlines[t + 1] = v

    # Get x-line centres for given time step
    ctrval = d.iloc[d.iloc[(d['y'] - 0).abs().argsort()[:1]].index[0]]['z'] / 6.371e6
    ycentre[t], ycentre[t + 1] = ctrval, ctrval

    # Get all x-line points within 1e6 of centre for given time step
    for x in range(len(d)):
        if np.abs(d.iloc[x, 1]) < 1e5: #1e6 is step size for cart search 
            t_ar.append(662 + t / 2)
            Z_ar.append(d.iloc[x, 2] / 6.371e6)

    xoline = np.loadtxt('xolinesCSV/xoline' + str(idx).zfill(7) + '.csv', delimiter = ',', skiprows = 1)
    for row in xoline:

        #x, y, z, vg, id, dbn_dl, what = map(float, xoline.readline().split()[1:8])
        dbn_dl, x, y, z = row[0], row[7], row[8], row[9]
        #print(dbn_dl, x, y, z)
        if np.abs(y) < 3e5 / 6.371e6 and np.abs(z) < 6:
            if dbn_dl > 0:
                x_t.append(idx)
                x_z.append(z)
            else:
                o_t.append(idx)
                o_z.append(z)

    t = t + 2

x = np.linspace(662, 1506, len(vlines) + 1)
y = np.linspace(-6, 6, len(vlines[0]) + 1)

fig, ax = mp.subplots()
cmap = ax.pcolormesh(x, y, np.transpose(vlines), cmap = 'bwr', vmin = '-600000', vmax = '600000')
fig.colorbar(cmap).ax.set_title(r'$V_z$')

ax.set_title('Dayside magnetopause centre lines, all timesteps')
ax.set_xlabel(r'$t$' + ' [s]')
ax.set_ylabel(r'$Z \ [R_E]$')
ax.set_yticks(np.linspace(-6, 6, 5))
ax.set_xticks(np.linspace(662, 1506, 5))

print(o_t)
print(o_z)

mp.scatter(x_t, x_z, color = 'm', marker = '.', s = 1, label = 'X-line')
mp.scatter(o_t, o_z, color = 'g', marker = '.', s = 1, label = 'O-line')

mp.scatter(t_ar, Z_ar, color = 'k', marker = '.')
mp.scatter(np.linspace(662, 1506, 2 * 845), ycentre, color = 'k', marker = '.')

mp.legend(loc = 'lower right', markerscale = 6)
fig.set_size_inches(18, 9, forward = True)
fig.savefig('AllPlot.png', facecolor = 'w', bbox_inches = 'tight')
