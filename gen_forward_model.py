import visionpy.recon.linear_model as linear_model
from visionpy.recon.utils import FieldOfView2D
from pymcx import load_mcx_settings
import numpy as np

domain_settings = load_mcx_settings("default_settings.json")
__, ny, nz = domain_settings["Domain"]["Dim"]
length_unit = domain_settings["Domain"]["LengthUnit"]
fov = FieldOfView2D(-length_unit * (ny - 1) / 2, length_unit * (ny - 1) / 2,
                    -length_unit * (nz - 1) / 2, length_unit * (nz - 1) / 2, ny, nz)
t = np.arange(256) * 2 * np.pi
geometry = np.array([0.04 * np.cos(t), 0.04 * np.sin(t)]).T
linear_model.gen_model(fov, geometry, "skin_phantom_model.json", verbose=True)
