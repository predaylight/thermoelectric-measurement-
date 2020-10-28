from bokeh.models import ColumnDataSource, OpenURL, TapTool,LinearAxis,Range1d,HoverTool,CustomJS,Whisker,LabelSet
from bokeh.models.widgets import *
from bokeh.layouts import *
from bokeh.models.arrow_heads import *
import pandas as pd

def errorbar(fig,source,x,y,xerr,yerr,color,point_kwargs={}, error_kwargs={},):
    # Note that x,y,xerr,yerr are strings of the column name of the source
    fig.circle(x=x,y=y,line_color="color",size=3,fill_color="color",source=source,**point_kwargs,legend='legend')
    fig.line(x=x,y=y,line_width=2,color=color,source=source)
    tflabel=pd.DataFrame(source.data)
    tflabel=tflabel[tflabel['I_kpss']==False]
    # fig.square(x=tflabel[x],y=tflabel[y],fill_color=None, line_color="red")

    # labels = LabelSet(x=x, y=y, text='I_kpss',source=source, x_offset=5, y_offset=0,
    #               text_font_size="15pt",text_color="color",
    #               text_align='center') #text_font_style='bold',
    # fig.add_layout(labels)
    if len(source.data[xerr])>0:
        x_err_x = []
        x_err_y = []
        for px, py, err in zip(source.data[x], source.data[y],source.data[xerr]):
            x_err_x.append((px - err, px + err))
            x_err_y.append((py, py))

        source.add(x_err_x,'xerr_x')
        source.add(x_err_y,'xerr_y')
        fig.multi_line(xs='xerr_x', ys='xerr_y', color='color',source=source,**error_kwargs)

    if len(source.data[yerr])>0:
        y_err_x = []
        y_err_y = []
        for px, py, err in zip(source.data[x], source.data[y],source.data[yerr]):
            y_err_x.append((px, px))
            y_err_y.append((py - err, py + err))

        source.add(y_err_x,'yerr_x')
        source.add(y_err_y,'yerr_y')
        fig.multi_line(xs='yerr_x', ys='yerr_y', color='color',source=source,**error_kwargs)
