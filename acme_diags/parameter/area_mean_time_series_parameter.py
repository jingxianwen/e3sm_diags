from .core_parameter import CoreParameter


class AreaMeanTimeSeriesParameter(CoreParameter):
    def __init__(self):
        super(AreaMeanTimeSeriesParameter, self).__init__()
        # A list of the reference names to run the diags on.
        self.ref_names = []
        self.reference_data_path = ''
        self.test_data_path = ''
        self.test_name = ''
        self.test_timeseries_input = True
        self.test_start_yr = ''
        self.test_end_yr = ''
        self.ref_timeseries_input = True
        self.ref_start_yr = ''
        self.ref_end_yr = ''
        # Granulating with regions doesn't make sense,
        # because we have multiple regions for each plot.
        # So keep all of the default values except regions.
        # self.seasons = ['ANN']
        # print(dir(self))
        self.granulate.remove('regions')
        self.granulate.remove('seasons')
        self.granulate.remove('plevs')

    def check_values(self):
        if not self.ref_names:
            msg = 'You have no value for ref_names. Caculate test data only'
            print(msg)

            #raise RuntimeError(msg)
