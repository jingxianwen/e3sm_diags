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
import datetime
import numpy
from calendar import monthrange



def createTimeAxisYear(year):
    import pdb
    pdb.set_trace()
    fmt = '%Y.%m.%d %H:%M:%S'
    BOUNDS=[]
    ss = '{:04d}.01.01 00:00:00'.format(year) 
    date = datetime.datetime.strptime(ss, fmt) 
    BOUNDS.append(date.timetuple().tm_yday-1) 
    ss = '{:04d}.12.31 23:59:59'.format(year) 
    date = datetime.datetime.strptime(ss, fmt) 
    BOUNDS.append(date.timetuple().tm_yday-1)  
    ### Compute center time
    CENTER=(BOUNDS[0]+BOUNDS[1])/2. -1
    time = cdms2.createAxis([CENTER])
    time.units = 'days since {:04d}'.format(year)
    time._bounds_ = numpy.array(BOUNDS)
    time.designateTime()
    time.id = "time"
    return time

def createTimeAxisSeasons(startYear, endYear):
    fmt = '%Y.%m.%d %H:%M:%S'
    BOUNDS=[]
    for year in range(startYear, endYear, extended=False):
        # Start in January 
        for i in range(1,4): 
            if i is 1 and year == startYear:
                nbMonths = 2
            else:
                nbMonths = 3

            monthbounds=[]
            # [1, 3, 6, 9]
            startSeasonMonth =  (i-1) * nbMonths
            if startSeasonMonth == 0:  
                startSeasonMonth = 1 

            s = '{:04d}.{:02d}.01 00:00:00'.format(year, startSeasonMonth) 
            date = datetime.datetime.strptime(s, fmt) 
            monthbounds.append(date.timetuple().tm_yday-1) 
            # Exception: JF first season of the star tyear
            s = '{:04d}.{:02d}.01 00:00:00'.format(year, startSeasonMonth + nbMonths) 
            date = datetime.datetime.strptime(s, fmt) 
            monthbounds.append(date.timetuple().tm_yday-1)  
            BOUNDS.append(monthbounds)
        ### add last bounds 
        BOUNDS.append([BOUNDS[-1][1], 365])
        BOUNDS=numpy.array(BOUNDS)
        print(BOUNDS)
        ### Compute center time
        CENTER=(BOUNDS[:,0]+BOUNDS[:,1])/2. -1 

        time = cdms2.createAxis(CENTER)
        time.units = 'days since {:04d}'.format(year)
        time._bounds_ = BOUNDS
        time.designateTime()
        time.id = "time"
    return time

def createTimeAxisMonths(year, startMonth=1, endMonth=12):
    fmt = '%Y.%m.%d %H:%M:%S'
    BOUNDS=[]
    # import pdb
    # pdb.set_trace()

    for i in range(startMonth,endMonth): 
        monthbounds=[]
        s = '{:04d}.{:02d}.01 00:00:00'.format(year, i) 
        date = datetime.datetime.strptime(s, fmt) 
        monthbounds.append(date.timetuple().tm_yday-1) 
        s = '{:04d}.{:02d}.01 00:00:00'.format(year, i+1) 
        date = datetime.datetime.strptime(s, fmt) 
        monthbounds.append(date.timetuple().tm_yday-1)  
        BOUNDS.append(monthbounds)
    if startMonth == endMonth:
        monthbounds=[]
        i = startMonth
        s = '{:04d}.{:02d}.01 00:00:00'.format(year, i)
        date = datetime.datetime.strptime(s, fmt)
        monthbounds.append(date.timetuple().tm_yday-1)
        if i+1 == 13:
            s = '{:04d}.{:02d}.31 23:59:59'.format(year, i) 
        else:
            s = '{:04d}.{:02d}.01 00:00:00'.format(year, i+1) 
        date = datetime.datetime.strptime(s, fmt) 
        monthbounds.append(date.timetuple().tm_yday-1)  
        BOUNDS.append(monthbounds)
        BOUNDS=numpy.array(BOUNDS[0])  # Only 1 bounds
        CENTER=[(BOUNDS[0]+BOUNDS[1])/2. -1 ]
    else:
        ### add last bounds 
        lastDay = monthrange(year,i+1)[1]
        s = '{:04d}.{:02d}.{:02d} 00:00:00'.format(year, i+1, lastDay) 
        date = datetime.datetime.strptime(s, fmt) 
        BOUNDS.append([BOUNDS[-1][1], date.timetuple().tm_yday-1])
        BOUNDS=numpy.array(BOUNDS)
        ### Compute center time
        CENTER=(BOUNDS[:,0]+BOUNDS[:,1])/2. -1 
    time = cdms2.createAxis(CENTER)
    time.units = 'days since {:04d}'.format(year)
    time._bounds_ = BOUNDS
    time.designateTime()
    time.id = "time"
    return time

def writeANNFiles(data, annualCycle):
    import pdb
    pdb.set_trace()
    out_file = cdms2.open(data.id+"_v0.1_ANN_climo.nc", mode='w')
    #Extrac information 
    axes, attributes, id, grid = extractMetadata(data)
    
    # Create new data with new time axis
    yearCycle = annualCycle.asma()
    yearCycle.units = data.units   #converted from mm/month
    yearCycle.id = data.id #runoff flux for cmip

    year    = data.getTime().asComponentTime()[0].year  # Get the Year from input data file
    time    = createTimeAxisYear(year)
    axes[0] = time
    outdata = TransientVariable( yearCycle, axes=axes, attributes=attributes, id=data.id, grid=grid)
    out_file.write(outdata)
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

        month = annualtime.asComponentTime()[i].month
        year  = data.getTime().asComponentTime()[0].year  # Get the Year from input data file
        time = createTimeAxisMonths(year, month, month)

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
#writeCLIMOFiles(data, annualcycle)
#writeSEASONFiles(data, seasonalcycle)
writeANNFiles(data, ANN)



