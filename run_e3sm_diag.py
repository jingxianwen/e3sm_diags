import os

from acme_diags.parameter.core_parameter import CoreParameter
from acme_diags.run import runner


param = CoreParameter()

param.run_type='model_vs_obs' #available: 'model_vs_obs'(default), 'model_vs_model', 'obs_vs_obs'

#============= reference =============
param.reference_data_path = '/global/project/projectdirs/acme/acme_diags/obs_for_e3sm_diags/climatology/'
param.reference_title = 'OBS'# will show on plots
#param.reference_data_path = '/global/cscratch1/sd/xianwen/acme_scratch/cori-knl/E3SMv2_standard_PresSST_UMRadALLoff/climo_2yr/'
#param.reference_title = 'E3SMv2_standard'# will show on plots


#============= test =============
#param.test_data_path = '/global/project/projectdirs/acme/acme_diags/test_model_data_for_acme_diags/climatology/'
param.test_data_path = '/global/cscratch1/sd/xianwen/E3SM_simulations/E3SM_v2_UMRad_CMIP6_20TRS.ne30_oEC.cori-knl/climo/'
param.test_name = 'E3SM_v2_UMRad_CMIP6_20TRS.ne30_oEC.cori-knl' #match output file name
param.test_title = 'E3SMv2_modified'# will show on plots (central upper)
param.short_test_name = ' '# will show on plots (central left)

#============= difference =============
param.diff_name = "E3SMv2_modified_OBS"
param.diff_title = "E3SMv2_modified-Standard"

#prefix = '/compyfs/www/zhan429/doc_examples/'
prefix = '/global/cscratch1/sd/xianwen/e3sm_diags/results/'
param.results_dir = os.path.join(prefix, 'E3SMv2_UMRad_CMIP_vs_obs')

#============= MPI ==============
param.multiprocessing = True
param.num_workers = 32

#param.variables=["PRECT"]
param.save_netcdf=False

#use below to run all core sets of diags:
runner.sets_to_run = ['lat_lon','zonal_mean_xy', 'zonal_mean_2d', 'polar', 'cosp_histogram', 'meridional_mean_2d']
#use below to run lat_lon map only
#runner.sets_to_run = ['lat_lon']

param.seasons = ["ANN","DJF", "JJA"]   #all seasons ["ANN","DJF", "MAM", "JJA", "SON"] will run,if comment out"

runner.run_diags([param])
