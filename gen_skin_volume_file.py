import numpy as np
from pymcx import gen_volume_file


def gen_skin_vol_file(nx, ny, nz, dx, vessel_d, vessel_r, epidermis_min, epidermis_max, output_file):
    volume = np.ones((nx, ny, nz))
    Y, X, Z = np.mgrid[0:ny, 0:nx, 0:nz] * dx
    volume[(Z >= epidermis_min) & (Z <= epidermis_max)] = 2  # Melanin layer
    volume[Z > epidermis_max] = 3  # Background
    vessel_centre_y = dx * ny / 2
    vessel_centre_z = epidermis_max + vessel_d + vessel_r
    volume[(Y - vessel_centre_y) ** 2 + (Z - vessel_centre_z) ** 2 < vessel_r ** 2] = 4  # Blood
    gen_volume_file(volume, output_file)
    return volume
