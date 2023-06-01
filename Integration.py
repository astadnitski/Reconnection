import matplotlib.pyplot as mp
import numpy as np
import pandas as pd

np.seterr(invalid = 'ignore')

def integrateEmulti(line, threshold):

    line = line.loc[line['near'] != 0]

    integrals = []
    maxnearID = int(line['near'].to_numpy().max())

    for nearID in range(maxnearID + 1):
        region = line.loc[line['near'] == nearID]
        if len(region) > threshold: integrals.append(integrateEsingle(region.reset_index()))

    return np.sum(integrals)

def integrateEsingle(line):

# # # STEP 1 | SET UP SUPPLEMENTARY DATAFRAMES # # #

    line.sort_values(by = ['y'])
    xyz = line[['x', 'y', 'z']].copy()
    E = line[['Ex', 'Ey', 'Ez']].copy()
    Elmn = E.copy().rename(columns = {'Ex': 'El', 'Ey': 'Em', 'Ez': 'En'})
    N = line[['Nx', 'Ny', 'Nz']].copy()
    #N = pd.DataFrame(0.0, index = np.arange(len(xyz)), columns = ['Nx', 'Ny', 'Nz'])
    M = N.copy().rename(columns = {'Nx': 'Mx', 'Ny': 'My', 'Nz': 'Mz'})
    L = N.copy().rename(columns = {'Nx': 'Lx', 'Ny': 'Ly', 'Nz': 'Lz'})

# # # STEP 2 | COMPUTE NEW BASES # # #

    dists = []

    for i in range(len(xyz) - 1):

        u = xyz.loc[i]
        v = xyz.loc[i + 1]
        dists.append(np.linalg.norm(v - u))
        
        m = -1 * (v - u) / dists[i]
        M.loc[i][0:3] = m
        
        if i > 0: s = -1 * (xyz.loc[i - 1] - u) /  np.linalg.norm(xyz.loc[i - 1] - u)
        else: s = -1 * (xyz.loc[i + 2] - u) / np.linalg.norm(xyz.loc[i + 2] - u)

        n = np.cross(m, s) / np.linalg.norm(np.cross(m, s))
        if n[0] < 0: n = -1 * n
        
        L.loc[i][0:3] = np.cross(m, N.loc[i][0:3]) / np.linalg.norm(np.cross(m, N.loc[i][0:3]))
 
    L.loc[len(L) - 1][0:3], M.loc[len(M) - 1][0:3], N.loc[len(N) - 1][0:3] = [0, 0, 0], [0, 0, 0], [0, 0, 0]

# # # STEP 3 | EVALUATE AND INTEGRATE ELECTRIC FIELD # # #

    Em, ig, add = [], [], 0

    for i in range(len(E) - 2):

        x, y, z = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        
        A = np.matrix([
            [np.dot(x, L.loc[i]), np.dot(x, M.loc[i]), np.dot(x, N.loc[i])], 
            [np.dot(y, L.loc[i]), np.dot(y, M.loc[i]), np.dot(y, N.loc[i])],
            [np.dot(z, L.loc[i]), np.dot(z, M.loc[i]), np.dot(z, N.loc[i])]])

        Elmn.loc[i][0:3] = np.matmul(A.T, E.loc[i][0:3])

        Em.append(Elmn.loc[i][2])

        add += Em[i] * dists[i]
        ig.append(add)

    Elmn.loc[len(E) - 1][0:3] = [0, 0, 0]

    return -1 * (ig[-1] - ig[0])

# # # MAIN # # #

hAxis = np.arange(662, 1507)
vAxis = [0] * len(hAxis)

for t in hAxis:
    line = pd.read_csv('xlinesCSV/xline' + str(t).zfill(7) + '.csv').copy()
    vAxis[t - 662] = integrateEmulti(line, 5)
    print(t, '|', vAxis[t - 662])

np.savetxt('integrals.csv', np.transpose([hAxis, vAxis]), delimiter = ',')

mp.title('Electric field integrated along x-lines')
mp.xlabel(r'$t$')
mp.xticks([662, 831, 1000, 1169, 1338, 1507]) 
mp.xlim(xmin = 650, xmax = 1519)
mp.ylabel('Integral')
mp.gcf().set_size_inches(18.5, 10.5)

lines = False
if lines:
    mp.plot(hAxis, vAxis, c = 'k')
    mp.savefig('IntegralsLinePlot.png', dpi = 600, facecolor = 'white', transparent = False)
else:
    mp.scatter(hAxis, vAxis, c = 'k', s = 1)
    mp.savefig('IntegralsScatterPlot.png', dpi = 600, facecolor = 'white', transparent = False)