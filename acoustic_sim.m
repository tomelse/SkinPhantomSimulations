function A=acoustic_sim(file_in, file_out)
fileID = fopen(file_in, 'r');
A = fread(fileID, 8000000,'single');
A = reshape(A, [200, 200, 200]); % this is our initial pressure distribution.
fclose(fileID);

p = zeros([400, 400]);
p(100:299, 100:299) = squeeze(sum(A, 1))*1000;
imagesc(p);
grid_size = 0.06e-3;

% =========================================================================
% SIMULATION
% =========================================================================

% create the computational grid
Nx = size(p, 1);           % number of grid points in the x (row) direction
Ny = size(p, 2);           % number of grid points in the y (column) direction
dx = grid_size;        % grid point spacing in the x direction [m]
dy = grid_size;        % grid point spacing in the y direction [m]
kgrid = kWaveGrid(Nx, dx, Ny, dy);

% define the properties of the propagation medium
medium.sound_speed = 1500;  % [m/s]
kgrid.setTime(2000,Nx*2*dx/(medium.sound_speed*2000))
source.p0 = p;

% define a centered circular sensor
sensor_radius = 10e-3;   % [m]
num_sensor_points = 512;
sensor.mask = makeCartCircle(sensor_radius, num_sensor_points);
% run the simulation
sensor_data = kspaceFirstOrder2D(kgrid, medium, source, sensor);
f_s = 1/kgrid.dt;
geometry = sensor.mask;
%%
save(file_out, 'sensor_data', 'f_s', 'geometry', '-v7.3')
A = file_out;
end