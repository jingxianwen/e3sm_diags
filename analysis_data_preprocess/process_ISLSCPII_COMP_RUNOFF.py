#This is a data conversion script to convert ISLSCPII_COMP_RUNOFF from ASCII to netcdf files
#for use with e3sm_diags package
#The data was taken from the ASCII format original data available from NASA EARTH DATA
#https://daac.ornl.gov/ISLSCP_II/guides/comp_runoff_monthly_xdeg.html
# Aug 1st, 2019 by Jill Chengzhu Zhang

import cdms2
import MV2
import glob
import numpy
import cdutil
from cdms2.tvariable import TransientVariable

def writeANNFiles(data, year):
    out_file = cdms2.open(data.id+"_v0.1_ANN_climo.nc", mode='w')
    #Extrac information 
    out_file.write(year)
    out_file.close()


def writeSEASONFiles(data, seasonalcycle):
    seasons = ['DJF','MAM','JJA','SON']
    for i in range(0,len(seasons)):
        out_file = cdms2.open(data.id+"_v0.1_"+seasons[i]+"_climo.nc", mode='w')
        #Extrac information 
        axes, attributes, id, grid = extractMetadata(seasonalcycle)
        seasonaltime = seasonalcycle.getTime()
    
        # Create new data with new time axis
        seasonalcycleMonth = seasonalcycle[i].asma()[MV2.newaxis, :]
        seasonalcycleMonth.units = data.units   #converted from mm/month
        seasonalcycleMonth.id = data.id #runoff flux for cmip

        # Extract time axis with boudns
        time = cdms2.createAxis([seasonaltime[i]])
        time.units = seasonaltime.units
        time._bounds_ = seasonaltime._bounds_[i]
        time.designateTime()
        time.id = "time"

        # Create anew cdms2 Variable
        axes[0] = time
        outdata = TransientVariable( seasonalcycleMonth, axes=axes, attributes=attributes, id=data.id, grid=grid)
        out_file.write(outdata)
        out_file.close()

def writeCLIMOFiles(data, annualcycle):
    for i in range(0,len(annualcycle.getTime())):
        out_file = cdms2.open(data.id+"_v0.1_"+"{:02d}".format(i+1)+"_climo.nc", mode='w')
        #Extrac information 
        axes, attributes, id, grid = extractMetadata(annualcycle)
        annualtime = annualcycle.getTime()
    
        # Create new data with new time axis
        annualcycleMonth = annualcycle[i].asma()[MV2.newaxis, :]
        annualcycleMonth.units = data.units   #converted from mm/month
        annualcycleMonth.id = data.id #runoff flux for cmip

        # Extract time axis with boudns
        time = cdms2.createAxis([annualtime[i]])
        time.units = annualtime.units
        time._bounds_ = annualtime._bounds_[i]
        time.designateTime()
        time.id = "time"

        # Create anew cdms2 Variable
        axes[0] = time
        outdata = TransientVariable( annualcycleMonth, axes=axes, attributes=attributes, id=data.id, grid=grid)
        out_file.write(outdata)
        out_file.close()

def extractMetadata(a, axes=None, attributes=None,
                     id=None, omit=None, omitall=False):
    """Extract axes, attributes, id from 'a', if arg is None."""
    resultgrid = None
    from cdms2.avariable import AbstractVariable
    from cdms2.avariable import AbstractRectGrid
    if isinstance(a, AbstractVariable):
        if axes is None:
            axes = a.getAxisList(omit=omit)
        if omitall:
            axes = None
        if attributes is None:
            attributes = a.attributes
        if id is None:
            id = "variable_%i" % cdms2.tvariable.TransientVariable.variable_count
            cdms2.tvariable.TransientVariable.variable_count += 1

        # If the grid is rectilinear, don't return an explicit grid: it's implicitly defined
        # by the axes.
        resultgrid = a.getGrid()
        if (resultgrid is None) or (isinstance(
                resultgrid, AbstractRectGrid)) or (axes is None):
            resultgrid = None

        # If the omitted axis was associated with the grid, the result will not
        # be gridded.
        elif (omit is not None) and (resultgrid is not None) and (a.getAxis(omit) in resultgrid.getAxisList()):
            resultgrid = None

    return axes, attributes, id, resultgrid


in_file = cdms2.open('/p/user_pub/e3sm/zhang40/analysis_data_e3sm_diags/ISLSCPII_GRDC/time_series/QRUNOFF_198601_199512.nc','r')
data=in_file('QRUNOFF')
annualcycle=cdutil.ANNUALCYCLE.climatology(data, criteriaarg = [0.99,None])
seasonalcycle = cdutil.SEASONALCYCLE.climatology(data, criteriaarg = [0.99,None])
ANN = cdutil.YEAR.climatology(data, criteriaarg = [0.99,None])
writeCLIMOFiles(data, annualcycle)
writeSEASONFiles(data, seasonalcycle)
writeANNFiles(data, ANN)



