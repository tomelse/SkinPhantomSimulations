import numpy as np
from gen_skin_volume_file import gen_skin_vol_file
from pymcx import load_mcx_settings, modify_settings_ms, write_mcx_settings
from spectra import blood_mu_a
from spectra import melanosome_mu_a
import os
import glob
from itertools import product
import pandas as pd

experiment_folder = "Exp_demo"
exp_definition = os.path.join(experiment_folder, "experiment.json")
exp_settings = load_mcx_settings(exp_definition)

l_min = exp_settings["min_wavelength"]
l_max = exp_settings["max_wavelength"]
n_lambda = exp_settings["n_wavelengths"]
wavelengths = np.linspace(l_min, l_max, n_lambda) * 1e-9

vessel_radii = exp_settings["vessel_radius"]
vessel_depths = exp_settings["vessel_depth"]
SO2s = exp_settings["SO2"]
nx = exp_settings["nx"]
ny = exp_settings["ny"]
nz = exp_settings["nz"]
dx = exp_settings["dx"]  # m
epidermis_thicknesses = exp_settings["epidermis_thickness"]
epidermis_starts = exp_settings["epidermis_start"]
melanin_coefficients = exp_settings["melanin_coefficients"]
background_haematocrits = exp_settings["background_haematocrit"]

def_param_file = os.path.join(experiment_folder, exp_settings["def_params_file"])

physical_parameters = (SO2s, melanin_coefficients, background_haematocrits)
phys_params_str = ["SO2", "Melanin", "BackgroundHaematocrit"]
physical_digits = int(np.log10(np.product(list(map(len, physical_parameters))))) + 1

vol_params_str = ["VesselDepth", "VesselRadii", "EpidermisThickness", "EpidermisStart"]
volume_parameters = (vessel_depths, vessel_radii, epidermis_thicknesses, epidermis_starts)
volume_combinations = product(*volume_parameters)
volume_digits = int(np.log10(np.product(list(map(len, volume_parameters))))) + 1

output = {}
for p in phys_params_str+vol_params_str+["Wavelength", "OutputFile", "VolumeFile", "SettingsFile"]:
    output[p] = []

for vol_num, vol_values in enumerate(volume_combinations):
    vessel_D, vessel_R, epidermis_thickness, epidermis_start = vol_values
    volume_code = str(vol_num).zfill(volume_digits)
    vol_file_stub = "volume_" + volume_code + ".bin"
    vol_file = os.path.join(experiment_folder, vol_file_stub)
    volume = gen_skin_vol_file(nx, ny, nz, dx, vessel_D, vessel_R, epidermis_start,
                               epidermis_start + epidermis_thickness,
                               vol_file)
    settings = load_mcx_settings(def_param_file)
    settings["Domain"]["VolumeFile"] = vol_file
    physical_combinations = product(*physical_parameters)
    for physical_num, physical_values in enumerate(physical_combinations):
        SO2, melanin_coeff, bg_hmt = physical_values
        physical_code = str(physical_num).zfill(physical_digits)
        mu_a_spectra = [lambda x: 0, lambda x: 1e-6, lambda x: blood_mu_a(x, haematocrit=bg_hmt)/1000,
                        lambda x: melanosome_mu_a(x, melanin_coeff)/1000, lambda x: blood_mu_a(x, SO2)/1000]
        wavelength_digits = int(np.log10(len(wavelengths))) + 1
        for wavelength_num, wavelength in enumerate(wavelengths):
            wavelength_code = str(wavelength_num).zfill(wavelength_digits)
            settings = modify_settings_ms(settings, mu_a_spectra, wavelength)
            run_code = volume_code + "_" + physical_code + "_" + wavelength_code
            output_file = "result_" + run_code
            settings["Session"]["ID"] = os.path.join(experiment_folder, output_file)
            settings_file = "settings_" + run_code + ".json"
            write_mcx_settings(settings, os.path.join(experiment_folder, settings_file))
            for p_i, p_v in enumerate(physical_values):
                output[phys_params_str[p_i]].append(p_v)
            for vol_i, vol_v in enumerate(vol_values):
                output[vol_params_str[vol_i]].append(vol_v)
            output["Wavelength"].append(wavelength)
            output["OutputFile"].append(output_file + ".mc2")
            output["VolumeFile"].append(vol_file_stub)
            output["SettingsFile"].append(settings_file)

run_output = pd.DataFrame(output)
run_output.to_csv(os.path.join(experiment_folder,"params.csv"))
run_output.to_html(os.path.join(experiment_folder, "params.html"))

files = glob.glob("Exp_demo/settings_*.json")
for i, file in enumerate(files):
    print(file)
    print(str(int(100 * i / len(files))) + "%")
    folder, json_file = os.path.split(file)
    file_stub = "_".join(os.path.splitext(json_file)[0].split("_")[1:])
    if len(glob.glob(os.path.join(folder, file_stub + ".mc2"))) == 0:
        os.system("mcxcl -f " + file + " -d 0 -U 0 -r 100")
