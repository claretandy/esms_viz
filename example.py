from bokeh.plotting import figure, show, reset_output
from bokeh.models import CustomJS, DatePicker
from bokeh.models import ColorBar, LinearColorMapper
import bokeh.palettes
import iris
from iris.time import PartialDateTime
import datetime as dt


file = '/scratch/abradley/Impacts_Toolbox/Data/Heat-Stress/WBGT_era5_global_day_tseries.nc'
wbgt = iris.load_cube(file)
bbox = {'xmin': -74, 'ymin': -11, 'xmax': -66, 'ymax': -6.5}  # [-74, -11, -66, -6.5]
subset = wbgt.intersection(longitude=(bbox['xmin'], bbox['xmax']), latitude=(bbox['ymin'], bbox['ymax']))
subset.coord('latitude').guess_bounds(0)
subset.coord('longitude').guess_bounds(0)


def make_plot(i):
    p = figure(width=400, height=400)
    p.x_range.range_padding = p.y_range.range_padding = 0
    mapper = LinearColorMapper(palette="Viridis256", low=20, high=40)

    # must give a vector of image data for image parameter
    img_xmin = subset.coord('longitude').bounds[0][0]
    img_ymin = subset.coord('latitude').bounds[-1][1]
    img_xmax = subset.coord('longitude').bounds[-1][1]
    img_ymax = subset.coord('latitude').bounds[0][0]
    p.image(image=[subset[i].data], x=img_xmin, y=img_ymin, dw=img_xmax - img_xmin, dh=img_ymax - img_ymin, color_mapper=mapper, level="image")  # palette=bokeh.palettes.viridis(256)
    p.grid.grid_line_width = 0.5
    color_bar = ColorBar(color_mapper=mapper, padding=0, ticker=p.xaxis.ticker, formatter=p.xaxis.formatter)
    p.add_layout(color_bar, 'below')

    show(p)


start_yr = dt.datetime(2021, 1, 1)
end_yr = dt.datetime(2021, 12, 31)

tcon = iris.Constraint(time=lambda cell: PartialDateTime(year=start_yr.year, month=start_yr.month,
                                                         day=start_yr.day) <= cell.point < PartialDateTime(
    year=end_yr.year, month=end_yr.month, day=end_yr.day))
acre_2021 = acre_subset.extract(tcon)

date_picker = DatePicker(title='Select date', value="2019-09-20", min_date="2019-08-01", max_date="2019-10-30")
date_picker.js_on_change("value", CustomJS(code="""
    console.log('date_picker: value=' + this.value, this.toString())
"""))

show(date_picker)
