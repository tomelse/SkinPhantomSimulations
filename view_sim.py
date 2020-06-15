from pymcx import read_output_file, load_mcx_settings
import matplotlib.pyplot as plt
import numpy as np

# 0_1_09
result = read_output_file("Exp_demo/result_0_1_09.mc2", load_mcx_settings("Exp_demo/settings_0_1_09.json"))

plt.imshow(np.log(np.squeeze(result[:,100,:])))
plt.show()

