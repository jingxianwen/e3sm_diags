import os

from acme_diags.parameter.core_parameter import CoreParameter
from acme_diags.run import runner


param = CoreParameter()

param.run_type='model_vs_model' #available: 'model_vs_obs'(default), 'model_vs_model', 'obs_vs_obs'

#============= reference =============
#param.reference_data_path = '/global/project/projectdirs/acme/acme_diags/obs_for_e3sm_diags/climatology/'
param.reference_data_path = '/global/cscratch1/sd/xianwen/acme_scratch/cori-knl/E3SMv2_standard_PresSST_UMRadALLoff/climo/'
param.reference_title = 'E3SMv2_standard'# will show on plots


#============= test =============
#param.test_data_path = '/global/project/projectdirs/acme/acme_diags/test_model_data_for_acme_diags/climatology/'
param.test_data_path = '/global/cscratch1/sd/xianwen/acme_scratch/cori-knl/E3SMv2_UMRad_iceflag1_noEmis/climo/'
param.test_name = 'E3SMv2_UMRad_iceflag1_noEmis' #match output file name
param.test_title = 'modified(iceflag1)'# will show on plots (central upper)
param.short_test_name = ' '# will show on plots (central left)

#============= difference =============
param.diff_name = "modified_iceflag1-Standard"
param.diff_title = "modified(iceflag1)-Standard"

#prefix = '/compyfs/www/zhan429/doc_examples/'
prefix = '/global/cscratch1/sd/xianwen/e3sm_diags/results/'
param.results_dir = os.path.join(prefix, 'E3SMv2_UMRad_iceflag1_noEmis_vs_standard')

#============= MPI ==============
param.multiprocessing = True
param.num_workers = 32

#param.variables=["PRECT"]
param.save_netcdf=False

#use below to run all core sets of diags:
runner.sets_to_run = ['lat_lon','zonal_mean_xy', 'zonal_mean_2d', 'polar', 'cosp_histogram', 'meridional_mean_2d']
#use below to run lat_lon map only
#runner.sets_to_run = ['lat_lon']

param.seasons = ["ANN","DJF", "MAM", "JJA", "SON"]   #all seasons ["ANN","DJF", "MAM", "JJA", "SON"] will run,if comment out"

runner.run_diags([param])
