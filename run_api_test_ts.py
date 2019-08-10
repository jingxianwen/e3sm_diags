import os
from acme_diags.parameter.core_parameter import CoreParameter
from acme_diags.run import runner

param = CoreParameter()

#param.test_data_path = '/global/project/projectdirs/acme/acme_diags/test_model_data_for_acme_diags/time-series/CESM1-CAM5_cmip/'
param.reference_data_path = '/global/project/projectdirs/acme/acme_diags/obs_for_e3sm_diags/time-series/'
param.test_data_path = '/global/project/projectdirs/acme/acme_diags/test_model_data_for_acme_diags/time-series/E3SM_v1/'
param.test_name = 'e3sm_v1'
#param.seasons = ["ANN"]
param.multiprocessing = False
param.test_timeseries_input = True
param.test_start_yr = '2002'
param.test_end_yr = '2008'
param.ref_timeseries_input = True
param.ref_start_yr = '2002'
param.ref_end_yr = '2008'


#param.num_workers =  16
prefix = '/global/project/projectdirs/acme/www/nadeau1/runs_with_api'
param.results_dir = os.path.join(prefix, 'area_mean_time_series_e3sm_v1_vs_obs_new_mask2')

# We're passing in this new object as well, in
# addtion to the CoreParameter object.

runner.sets_to_run = ['area_mean_time_series']
runner.run_diags([param])
