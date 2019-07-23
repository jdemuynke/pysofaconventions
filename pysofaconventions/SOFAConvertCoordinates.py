import numpy as np
import math as m

def SOFAConvertCoordinates(input, input_type, output_type, *args):

    if len(args) == 2:
        input_unit = args[0]
        output_unit = args[1]
    elif len(args) <= 1:
        if output_type == 'spherical':
            output_unit = 'degree'
        else:
            output_unit = 'meter'
        if len(args) == 1:
            if input_type == 'spherical':
                input_unit = 'degree'
            else:
                input_unit = 'meter'

    if input_type == 'spherical':
        if output_type == 'spherical':
            if input_unit == output_unit:
                output = input
            elif input_unit == 'degree':
                output = np.asarray([deg2rad(input[:, 0]), deg2rad(input[:, 1]), input[:, 2]].T)
            else:
                output = rad2deg(input)
        elif output_type == 'cartesian':
            if input_unit == 'degree':
                output = sph2cart(np.asarray([deg2rad(input[:, 0]), deg2rad(input[:, 1]), input[:, 2]]).T)
            else:
                output = sph2cart(input)
        else:
            exit('Output type ' + output_type + ' unknown!')
    elif input_type == 'cartesian':
        if output_type == 'cartesian':
            output = input
        elif output_type == 'spherical':
            if input_unit == 'degree':
                output = cart2sph(np.asarray([deg2rad(input[:, 0]), deg2rad(input[:, 1]), input[:, 2]]).T)
            else:
                output = cart2sph(input)
        else:
            exit('Output type ' + output_type + ' unknown!')
    else:
        exit('Input type ' + input_type + ' unknown!')
    return output


def cart2sph(input_coord):

    x = input_coord[:, 0]
    y = input_coord[:, 1]
    z = input_coord[:, 2]

    az, elev, dist = (np.empty_like(x) for _ in range(3))
    for i in range(len(x)):
        XsqPlusYsq = x[i]**2 + y[i]**2
        dist[i] = m.sqrt(XsqPlusYsq + z[i]**2)           # r
        elev[i] = m.atan2(z[i], m.sqrt(XsqPlusYsq))     # theta
        az[i] = m.atan2(y[i], x[i])                          # phi

    output_coord = np.asarray([az, elev, dist]).T
    return output_coord

def sph2cart(input_coord):

    az = input_coord[:, 0]
    elev = input_coord[:, 1]
    dist = input_coord[:, 2]

    x, y, z = (np.empty_like(az) for _ in range(3))
    for i in range(len(az)):
        x[i] = dist[i] * m.cos(az[i]) * m.cos(elev[i])
        y[i] = dist[i] * m.sin(az[i]) * m.cos(elev[i])
        z[i] = dist[i] * m.sin(elev[i])

    output_coord = np.asarray([x, y, z]).T
    return output_coord

def deg2rad(angle_deg):
    angle_rad = np.empty_like(angle_deg)
    for i in range(len(angle_deg)):
        angle_rad[i] = angle_deg[i]*np.pi/180
    return angle_rad

def rad2deg(angle_rad):
    angle_deg = np.empty_like(angle_rad)
    for i in range(len(angle_rad)):
        angle_deg[i] = angle_rad[i]*180/np.pi
    return angle_deg