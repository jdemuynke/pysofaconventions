#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   plotGeometry.py
#
#   Plots the geometry of the source positions contained in a SOFA file
#
#   (C) Julien De Muynke - Eurecat
#   16/07/2019
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import *
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as plt3d
import sys

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(45, -145)
import numpy as np

path = sys.argv[1]
#path = '/Users/acustica/Development_projects/matlabsofapanner/Deluxe_KU1000_16384smp.SOFA'
sofa = SOFAFile(path, "r")


# Convention must be SimpleFreeFieldHRIR
print "\n"
print "SOFA Convention:", sofa.getGlobalAttributeValue('SOFAConventions')
if sofa.getGlobalAttributeValue('SOFAConventions') != 'SimpleFreeFieldHRIR':
    print('Convention must be SimpleFreeFieldHRIR')
    exit()

# Let's check the position of the measurements (Source position)
sourcePosition = sofa.getVariableValue('SourcePosition')
nof_source_positions = sofa.getDimension('M')
SOFASourcePosition_Type = sofa.getPositionVariableInfo('SourcePosition')

receiverPosition = sofa.getVariableValue('ReceiverPosition')
SOFAReceiverPosition_Type = sofa.getPositionVariableInfo('ReceiverPosition')

listenerView = sofa.getVariableValue('ListenerView')
listenerView_scaled = 0.5*listenerView / np.sqrt(listenerView[0][0]**2 + listenerView[0][1]**2 + listenerView[0][2]**2)

sourcePositions_spherical = SOFAConvertCoordinates(sourcePosition, SOFASourcePosition_Type[1], 'spherical', 'degree' if 'degree' in SOFASourcePosition_Type[0] else 'radian', 'degree')
sourcePositions_cartesian = SOFAConvertCoordinates(sourcePosition, SOFASourcePosition_Type[1], 'cartesian', 'degree' if 'degree' in SOFASourcePosition_Type[0] else 'radian', 'meter')
x = sourcePositions_cartesian[:, 0]
y = sourcePositions_cartesian[:, 1]
z = sourcePositions_cartesian[:, 2]

print('Source Positions:\n')

for i in range(nof_source_positions.size):
    print(str(i+1) + ': ' + str(sourcePositions_spherical[i, :]))
    ax.scatter(x[i], y[i], z[i], zdir='z', s=20, c=(0, 0, 0),  marker='.')
    ax.text(x[i], y[i], z[i]+0.1, str(i+1))

receiverPosition_cartesian = SOFAConvertCoordinates(receiverPosition, SOFAReceiverPosition_Type[1], 'cartesian')
xR = receiverPosition_cartesian[:, 0]
yR = receiverPosition_cartesian[:, 1]
zR = receiverPosition_cartesian[:, 2]


ax.scatter(xR[0], yR[0], zR[0], c='red')
ax.scatter(xR[1], yR[1], zR[1], c='red')

xLV = [0, listenerView_scaled[0][0]]
yLV = [0, listenerView_scaled[0][1]]
zLV = [0, listenerView_scaled[0][2]]
ax.scatter(xLV[1], yLV[1], zLV[1], c='red', marker='+')
line = plt3d.art3d.Line3D(xLV, yLV, zLV, c='red')
ax.add_line(line)

fig.suptitle(sofa.getGlobalAttributeValue('DatabaseName') + ' ' + sofa.getGlobalAttributeValue('ListenerShortName'))
plt.show()