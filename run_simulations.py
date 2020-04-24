import os
import glob

files = glob.glob("Exp*/settings_*.json")
for i, file in enumerate(files):
    print(file)
    print(str(int(100 * i / len(files))) + "%")
    folder, json_file = os.path.split(file)
    file_stub = "_".join(os.path.splitext(json_file)[0].split("_")[1:])
    if len(glob.glob(os.path.join(folder, "result_" + file_stub + ".mc2"))) == 0:
        os.system("mcxcl -f " + file + " -d 0 -U 0 -r 10")
