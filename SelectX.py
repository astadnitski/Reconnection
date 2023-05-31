import pytools

import matplotlib.pyplot as mp
import numpy as np
import pandas as pd

R_E = 6.371e6
dr = 1e6

def dist(p0, p1):
    x0, y0, z0 = p0[0:3]
    x1, y1, z1 = p1[0:3]
    return np.sqrt((x0 - x1)**2 + (y0 - y1)**2 + (z0 - z1)**2)

def xCoords(t):

    x_x, x_y, x_z = [], [], []
    N_x, N_y, N_z = [], [], []
    con = []

    xoline = np.loadtxt('xolinesCSV/xoline' + str(t).zfill(7) + '.csv', delimiter = ',', skiprows = 1)
    for row in xoline:
        if row[0] > 0:

            x_x.append(row[7] * R_E)
            x_y.append(row[8] * R_E)
            x_z.append(row[9] * R_E)

            mag = dist([0, 0, 0], [row[1], row[2], row[3]])
            if row[1] < 0: mag *= -1
            N_x.append(row[1] / mag)
            N_y.append(row[2] / mag)
            N_z.append(row[3] / mag)

            con.append(int(row[6]))

    return x_x, x_y, x_z, N_x, N_y, N_z, con

def checkOrder(ar):
    rgb, count = [], len(ar)
    for frac in range(count): rgb.append((1 - frac / count, 0, 1 - frac / count))
    return rgb

def cartExtract(data, t):

    x = np.arange(7 * R_E, 11 * R_E, dr)
    y = np.arange(-9 * R_E, 9 * R_E, dr)
    z = np.arange(-6 * R_E, 6 * R_E, dr)

    Y, Z = np.meshgrid(y, z)
    V_z = Y.copy()
    V_z.fill(1e7)

    for j in range(len(y)):
        for k in range(len(z)):
            loc = [0, y[j], z[k]]
            for i in range(len(x)):
                loc[0] = x[i]
                cellid = data.get_cellid(loc)
                b = data.read_variable('vg_b_vol', operator = 'z', cellids = cellid)
                if b <= 0:
                    v = data.read_variable('vg_v', operator = 'z', cellids = cellid)
                    V_z[k, j] = v
                    break

    fig, ax = mp.subplots()
    pcm = ax.pcolormesh(Y / R_E, Z / R_E, V_z, vmin = -6e5, vmax = 6e5, cmap = 'bwr')
    fig.colorbar(pcm, ax = ax, format = '%.0e', fraction = 0.046, pad = 0.04).ax.set_title(r'$V_z$')
    #np.savetxt('vlinesCSV/v' + str(t).zfill(7) + '.csv', V_z[:, 77], delimiter = ',')

def getE(data, x, y, z):
    
    E_x, E_y, E_z = [1.0] * len(x), [1.0] * len(x), [1.0] * len(x)

    fgE = data.read_fsgrid_variable('fg_e')

    delta = 1e6
    xmin, ymin, zmin = -7.04e8, -3.68e8, -3.68e8

    for i in range(len(x)):
        r = fgE[int(np.floor((x[i] - xmin) / delta)), int(np.floor((y[i] - ymin) / delta)), int(np.floor((z[i] - zmin) / delta)), 0:3]
        E_x[i] = r[0]
        E_y[i] = r[1]
        E_z[i] = r[2]

    return E_x, E_y, E_z

def main(t):

    stag = pd.DataFrame(pd.read_csv('staglinesCSV/coords' + str(t).zfill(7) + '.csv'))

    x_x, x_y, x_z, N_x, N_y, N_z, con = xCoords(t)
    near = [0] * len(x_x)

    near_y, near_z, near_con = [], [], []
    recent, current = 0, 0
    for i, point in stag.iterrows():

        idx = (np.sqrt((x_y - point[1])**2 + (x_z - point[2])**2)).argmin()

        n_y, n_z = x_y[idx], x_z[idx]
        if n_y not in near_y and n_z not in near_z:
            near_y.append(n_y)
            near_z.append(n_z)
            #near_con.append(n_con)
            if not con[idx] == recent:
                current += 1
                recent = con[idx]
            near[idx] = current

    data = pytools.vlsvfile.VlsvReader('/wrk-vakka/group/spacephysics/vlasiator/3D/EGI/bulk/dense_cold_hall1e5_afterRestart374/bulk1.' + str(t).zfill(7) + '.vlsv')  
    cartExtract(data, t) # Comment / uncomment toggles Vz background
    
    mp.title('Reconnection x-lines, t = ' + str(t))
    mp.axis('equal')
    mp.autoscale(False)

    mp.scatter(stag['y'] / R_E, stag['z'] / R_E, color = 'k', s = 1)
    mp.scatter(np.divide(x_y, R_E), np.divide(x_z, R_E), s = 1, c = 'm')
    mp.scatter(np.divide(near_y, R_E), np.divide(near_z, R_E), s = 1, c = 'c')

    mp.xlabel(r'$Y \ [R_E]$')
    mp.xticks([-9, -6, -3, 0, 3, 6, 9]) 
    mp.xlim(xmin = -9, xmax = 9)
    
    mp.ylabel(r'$Z \ [R_E]$')
    mp.yticks([-6, -3, 0, 3, 6])
    mp.ylim(ymin = -6, ymax = 6)
    
    mp.show()
    mp.savefig('xplots/xplot' + str(t).zfill(7) + '.png')
    mp.close()

    E_x, E_y, E_z = getE(data, x_x, x_y, x_z)
    np.savetxt('xlinesCSV/xline' + str(t).zfill(7) +'.csv', np.transpose([x_x, x_y, x_z, N_x, N_y, N_z, E_x, E_y, E_z, con, near]), delimiter = ',', header = 'x,y,z,Nx,Ny,Nz,Ex,Ey,Ez,id,near', comments = '')

main(1284)
#for i in range(662, 1507): main(i)
