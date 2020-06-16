import os
import visionpy.io.load_kwave as lk
import matplotlib.pyplot as plt
import subprocess
import glob
import matlab.engine
eng = matlab.engine.start_matlab()
in_folder = "Exp1"
out_folder = "Exp2_acoustic"
for file in glob.glob(os.path.join("Exp1", "*.mc2")):
    root = os.path.splitext(os.path.basename(file))[0]
    print(root)
    if len(glob.glob(os.path.join(out_folder, root + ".mat"))) == 0:
        c = eng.acoustic_sim(os.path.join(in_folder, root + ".mc2"), os.path.join(out_folder, root + ".mat"))
    eng.close("all")

"""
pa = lk.load_kwave(os.path.join(out_folder, root + ".mat"))

plt.imshow(pa.data, aspect="auto")
plt.show()
"""