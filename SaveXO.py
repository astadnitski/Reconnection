# Trace generated using paraview version 5.10.1
# import paraview
# paraview.compatibility.major = 5
# paraview.compatibility.minor = 10

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

yborder, zborder = 9, 6

#for t in range(662, 1507):
for t in range(1284, 1284 + 1):

    cellData = LegacyVTKReader(registrationName = 'XOlines' + str(t).zfill(7) + '.vtk', FileNames = ['xolinesVTK/tail_XOlines_' + str(t).zfill(7) + '.vtk'])

    clip = Clip(registrationName = 'Clip', Input = cellData)
    clip.ClipType = 'Plane'
    clip.HyperTreeGridClipper = 'Plane'
    clip.Scalars = ['POINTS', 'vg_dBN_dL']
    clip.Value = -4.191525403999999e-07
    clip.ClipType.Origin = [5.320849895477295, 0.0, 0.0]
    clip.HyperTreeGridClipper.Origin = [5.320849895477295, 0.0, 0.0]
    Show3DWidgets(proxy = clip.ClipType)
    clip.ClipType = 'Box'
    clip.ClipType.Position = [0.0, -yborder, -zborder]
    clip.ClipType.Length = [10.64169979095459, 2 * yborder, 2 * zborder]

    threshold = Threshold(registrationName = 'Threshold', Input = clip)
    threshold.Scalars = ['POINTS', 'vg_dBN_dL']
    threshold.LowerThreshold = 0.0
    threshold.UpperThreshold = 1.2526222885e-06
    connectivity = Connectivity(registrationName = 'Connectivity', Input = threshold)

    SaveData('xolinesCSV/xoline' + str(t).zfill(7) + '.csv', proxy = connectivity, PointDataArrays = ['Normals', 'RegionId', 'conn_component', 'vg_J_magnitude', 'vg_dBN_dL', 'RegionId'],
        CellDataArrays = ['Normals', 'RegionId', 'conn_component', 'vg_J_magnitude', 'vg_dBN_dL', 'RegionId'],
        FieldDataArrays = ['CYCLE', 'MeshName', 'TIME', 'VolumeDependent'])
    
    print('Saved', t)
