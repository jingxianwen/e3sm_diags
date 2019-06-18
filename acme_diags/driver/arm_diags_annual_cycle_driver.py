import os
import collections
import cdms2
import cdutil
import acme_diags
from acme_diags.driver import utils
from acme_diags.metrics import mean
from acme_diags.plot.cartopy import area_mean_time_series_plot

RefsTestMetrics = collections.namedtuple('RefsTestMetrics', ['refs', 'test', 'metrics'])

def create_metrics(ref_domain):
    """
    For this plotset, calculate the mean of the
    reference data and return a dict of that.
    """
    return {'mean': mean(ref_domain)}


def run_diag(parameter):
    variables = parameter.variables
    regions = parameter.regions
    ref_names = parameter.ref_names

    # Both input data sets must be time-series files.
    # Raising an error will cause this specific set of
    # diagnostics with these parameters to be skipped.
    #if test_data.is_climo() or ref_data.is_climo():
    #    msg = 'Cannot run the plotset regional_mean_time_series '
    #    msg += 'because both the test and ref data need to be time-series files.'
    #    raise RuntimeError(msg)

    for region in regions:
        # The regions that are supported are in acme_diags/derivations/default_regions.py
        # You can add your own if it's not in there.
        print("Selected region: {}".format(region))
        regions_to_data = collections.OrderedDict()

        for var in variables:
            print('Variable: {}'.format(var))
            test_data = utils.dataset.Dataset(parameter, test=True)
            test = test_data.get_timeseries_variable(var)
            
            # Make sure data have correct montly Bounds
            cdutil.setTimeBoundsMonthly(test)
            print('test shape',test.shape, test.units)

            parameter.viewer_descr[var] = getattr(test, 'long_name', var)
            # Get the name of the data, appended with the years averaged.
            parameter.test_name_yrs = utils.general.get_name_and_yrs(parameter, test_data)

            refs = []

            for ref_name in ref_names:    
                setattr(parameter, 'ref_name', ref_name)
                ref_data = utils.dataset.Dataset(parameter, ref=True)
            
                parameter.ref_name_yrs = utils.general.get_name_and_yrs(parameter, ref_data)

                ref = ref_data.get_timeseries_variable(var)

                cdutil.setTimeBoundsMonthly(ref)
 
                
                # TODO: Will this work if ref and test are timeseries data,
                # but land_frac and ocean_frac are climo'ed.
                print(ref_name)
                test_domain = utils.general.select_point(region, test)
                ref_domain = utils.general.select_point(region, ref)

                test_domain_year = cdutil.ANNUALCYCLE(test_domain)
                ref_domain_year = cdutil.ANNUALCYCLE(ref_domain)
                ref_domain_year.ref_name = ref_name

                refs.append(ref_domain_year)

            # metrics_dict = create_metrics(ref_domain)
            metrics_dict = ref_domain_year.mean()
            # print(test_domain_year.getTime().asComponentTime())
            # print(test.getTime().asComponentTime())

            result = RefsTestMetrics(test=test_domain_year, refs=refs, metrics=metrics_dict)
            regions_to_data[region] = result
 
        area_mean_time_series_plot.plot(var, regions_to_data, parameter)
        # TODO: How will this work when there are a bunch of plots for each image?
        # Yes, these files should be saved.
        # utils.general.save_ncfiles(parameter.current_set,
        #                     mv1_domain, mv2_domain, diff, parameter)
    return parameter

