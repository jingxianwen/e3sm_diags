import os
from acme_diags.parameter.core_parameter import CoreParameter
from acme_diags.parameter.area_mean_time_series_parameter import AreaMeanTimeSeriesParameter
from acme_diags.run import runner

param = CoreParameter()

param.reference_data_path = '/global/project/projectdirs/acme/acme_diags/obs_for_e3sm_diags/climatology/'
param.test_data_path = '/global/project/projectdirs/acme/acme_diags/test_model_data_for_acme_diags/climatology/'
param.test_name = '20161118.beta0.FC5COSP.ne30_ne30.edison'
param.seasons = ["ANN"]
param.multiprocessing = False
prefix = '/global/project/projectdirs/acme/www/nadeau1/runs_with_api'
param.results_dir = os.path.join(prefix, 'multiple_sets')


# Set specific parameters for new sets
ts_param = AreaMeanTimeSeriesParameter()
ts_param.reference_data_path = '/global/project/projectdirs/acme/acme_diags/obs_for_e3sm_diags/time-series/'
ts_param.test_data_path = '/global/project/projectdirs/acme/acme_diags/test_model_data_for_acme_diags/time-series/E3SM_v1/'
ts_param.test_name = 'e3sm_v1'
ts_param.test_timeseries_input = True
ts_param.test_start_yr = '2002'
ts_param.test_end_yr = '2008'
ts_param.ref_timeseries_input = True
ts_param.ref_start_yr = '2002'
ts_param.ref_end_yr = '2008'

# We're passing in this new object as well, in
# addtion to the CoreParameter object.
# runner.sets_to_run = ['lat_lon', 'area_mean_time_series']
# runner.run_diags([param, ts_param])
runner.sets_to_run = ['lat_lon', 'area_mean_time_series']
runner.run_diags([param, ts_param])
