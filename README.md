# Initial Skin Phantom Experiments

The code in this folder is to setup and run the first skin phantom optical simulations. 

It works by setting up an experiment folder (e.g. Exp1 etc). In that folder, there should be a file called experiment.json. This specifies the parameters in that run of the experiment (e.g. wavelengths, vessel radii, vessel depth, SO2, nx, ny, nz, dx, epidermis thickness, epidermis start, the file for the default parameters, the melanin coefficients and the background haematocrit). I think all of those parameters are fairly self-explanatory except background haematocrit.

The background haematocrit parameter changes the non-blood vessel part of the volume. The background is defined as a water-blood mixture with the specified haematocrit.

