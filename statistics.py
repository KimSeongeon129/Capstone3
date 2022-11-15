from flask import g, Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

import pandas as pd
import numpy as np
import math

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, MultiChoice, CustomJS
from bokeh.layouts import row, column, gridplot, layout
from bokeh.embed import components
from bokeh.io import show
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap

bp= Blueprint('statistics',__name__)

@bp.route('/statistics')#이미지 결과페이지
def imgUpload_result():
        db_cursor = g.db.cursor()
        db_cursor.execute('SELECT * FROM result')
        table_rows = db_cursor.fetchall()
        df = pd.DataFrame(table_rows)

        PARTS = ['덕트', '선박 배관', '선체', '케이블', '보온재']

        #-------------------------------
        #  부품별 불량품 건수
        #-------------------------------
        counts = [0 for i in range(len(PARTS))]

        valueCounts = df[df['part_name'] != '양품'].value_counts('part_name')
        for part in PARTS:
                try:
                        counts[PARTS.index(part)] = valueCounts[part]
                except:
                        pass

        source = ColumnDataSource(data=dict(parts=PARTS, counts=counts))
        p1_cmap = factor_cmap('parts', palette=Spectral6, factors=PARTS)
        
        p1 = figure(x_range=PARTS, height=600, toolbar_location=None, title="부품별 불량품 건수")
        p1.vbar(x='parts', top='counts', width=0.9, source=source, legend_field="parts",
                line_color='white', fill_color=p1_cmap)

        p1.xgrid.grid_line_color = None
        p1.y_range.start = 0
        p1.legend.orientation = "horizontal"
        p1.legend.location = "top_center"


        #-------------------------------
        #  부품 불량 유형별 불량품 건수
        #-------------------------------
        
        group = df[df['part_name'] != '양품'].groupby(['part_name', 'part_category'])
        
        p2_cmap = factor_cmap('part_name_part_category', palette=Spectral6, factors=PARTS, end=1)

        p2 = figure(width=500, height=600, title="불량 유형별 불량품 건수",
                x_range=[['케이블','Cable Damage']], toolbar_location=None, )
#tooltips=[("count", "@inspection_number_count"), ("part_name, part_category", "@part_name_part_category")]
        p2.vbar(x='part_name_part_category', top='inspection_number_count', width=1, source=group,
                line_color="white", fill_color=p2_cmap)

        p2.y_range.start = 0
        p2.x_range.range_padding = 0.05
        p2.xgrid.grid_line_color = None
        p2.xaxis.major_label_orientation = 1.2
        p2.outline_line_color = None


        #-------------------------------
        #  Laying out in row
        #-------------------------------

        multi_choice = MultiChoice(value=PARTS, options=PARTS, title='parts:')

        callback = CustomJS(args=dict(source=source, p1 = p1, p2 = p2, multi_choice=multi_choice), code="""    
                var selected = multi_choice.value;
                p1.x_range.factors = selected;
                p2.x_range.factors = selected;
        """)
        multi_choice.js_on_change('value', callback)

        plot = layout(children=[multi_choice,
                                [p1, p2]], sizing_mode='stretch_both')

        script, div = components(plot)

        kwargs = {'script1': script, 'div1': div}
        kwargs['title'] = 'bokeh-with-flask' 

        return render_template("statistics.html", **kwargs)
