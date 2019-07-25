#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   plotListenHRTF.py
#
#   Example for getting HRTF data from a sofa file
#   Plots the HRTF and convolves to obtain binaural sound
#
#   (C) Andres Perez-Lopez - Eurecat / UPF
#   30/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import *
import matplotlib.pyplot as plt
import scipy.signal
import soundfile as sf
import numpy as np

# Let's use subject_003 from the classical CIPIC database
# http://sofacoustics.org/data/database/cipic/subject_003.sofa
path = '/Users/acustica/Development_projects/matlabsofapanner/Deluxe_16384smp_Eurecat_nearfield_Koeln_anechoic.SOFA'
sofa = SOFAFile(path, 'r')

# File is actually not valid, but we can forgive them
print "\n"
print "File is valid:", sofa.isValid()

# Convention is SimpleFreeFieldHRIR
print "\n"
print "SOFA Convention:", sofa.getGlobalAttributeValue('SOFAConventions')

# Let's see the dimensions:
#   - M: 1250 (different measurement positions)
#   - R: 2 (the two ears)
#   - E: 1 (one loudspeaker)
#   - N: 200 (lenght of the HRTFs in samples)
print "\n"
print "Dimensions:"
sofa.printSOFADimensions()

# Let's see the variables as well
print "\n"
print "Variables"
sofa.printSOFAVariables()

# Let's check the position of the measurementa (Source position)
sourcePosition = sofa.getVariableValue('SourcePosition')
nof_source_positions = sofa.getDimension('M')
SOFASourcePosition_Type = sofa.getPositionVariableInfo('SourcePosition')
sourcePositions_spherical = SOFAConvertCoordinates(sourcePosition, SOFASourcePosition_Type[1], 'spherical', 'degree' if 'degree' in SOFASourcePosition_Type[0] else 'radian', 'degree')

for i in range(nof_source_positions.size):
    print(str(i+1) + ': ' + str(sourcePositions_spherical[i, :]))

# Let's inspect the first measurement
hrtf_index = input("Which HRIR do you want to plot?")
m = int(hrtf_index)-1
print "\n"
print "Source Position of measurement " + str(m)
print(str(sourcePositions_spherical[m, :]))
# which is at 82 degrees azimuth, -7 degrees elevation

# Read the data
data = sofa.getDataIR()
# and get the HRTF associated with m=0
hrtf = data[m,:,:]

# Let's check the dimensions of the hrtf
print "\n"
print "HRTF dimensions"
print hrtf.shape

# It looks fine, so let's plot it
plt.plot(hrtf[0], label="left", linewidth=0.5,  marker='o', markersize=1)
plt.plot(hrtf[1], label="right", linewidth=0.5,  marker='o', markersize=1)
plt.grid()
plt.legend()
plt.show()
# It's pretty clear, based on the ITD and ILD, that the source is located at the left,
# which on the other hand confirms the sourcePosition[0] information

binaural_process = raw_input("Do you want to binauralize a mono file with this HRTF? Y/N")

if binaural_process == 'Y':
    filename = raw_input("Please enter a filename:")

    # Let's render it with a file and listen to it
    # Open a mono wav file. I got this one from freesound
    # https://freesound.org/people/Ryntjie/sounds/365061/
    data, samplerate = sf.read(filename)

    # Convolve it with the hrtf
    binaural_left = scipy.signal.fftconvolve(data[:,0], hrtf[0])
    binaural_right = scipy.signal.fftconvolve(data[:,1], hrtf[1])
    binaural = np.asarray([binaural_left, binaural_right]).swapaxes(-1,0)

    # Write to a file, and enjoy!
    sf.write(filename[:-4] + '_binauralized.wav', binaural, samplerate)
    print(filename[:-4] + '_binauralized.wav written!')