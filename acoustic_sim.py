import os
import visionpy.io.load_kwave as lk
import matplotlib.pyplot as plt
import subprocess
import glob
import matlab.engine
from visionpy.recon.backproject import circle_backproject
from visionpy.recon.utils import FieldOfView2D
import numpy as np

eng = matlab.engine.start_matlab()
in_folder = "Exp1"
out_folder = "Exp2_acoustic"
for file in glob.glob(os.path.join(in_folder, "*.mc2")):
    root = os.path.splitext(os.path.basename(file))[0]
    # print(root)
    if len(glob.glob(os.path.join(out_folder, root + ".mat"))) == 0:
        c = eng.acoustic_sim(os.path.join(in_folder, root + ".mc2"), os.path.join(out_folder, root + ".mat"))
    eng.close("all")

ts = []
file = glob.glob(os.path.join(out_folder, "*.mat"))[:21]
fov = FieldOfView2D(-0.01, 0.01, -0.01, 0.01, 256, 256)
for f in file:
    print(f)
    pa = lk.load_kwave(f)
    t = circle_backproject(pa, 1500, fov)
    ts.append(t)
ts = np.array(ts)

plt.plot(ts[:, 128, 128])
plt.show()

"""

plt.imshow(pa.data, aspect="auto")
plt.show()
"""
