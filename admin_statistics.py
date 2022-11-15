from flask import g, Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

import pandas as pd
import numpy as np
import math

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot, layout
from bokeh.embed import components
from bokeh.io import show
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap

bp= Blueprint('admin_statistics',__name__)


@bp.route('/admin_statistics')#이미지 결과페이지
def adminUpload_result():
        db_cursor = g.db.cursor()
        db_cursor.execute('SELECT * FROM result')
        table_rows = db_cursor.fetchall()
        df = pd.DataFrame(table_rows)

        source = ColumnDataSource(data=df)

        #-------------------------------
        #  부품별 불량품 건수
        #-------------------------------
        PARTS = ['덕트', '선박 배관', '선체', '케이블', '보온재']
        counts = [0 for i in range(len(PARTS))]

        valueCounts = df.value_counts('part_name')
        counts = [valueCounts[part] for part in valueCounts.index if part is not '양품']

        source = ColumnDataSource(data=dict(parts=PARTS, counts=counts))

        p1 = figure(x_range=PARTS, height=300, toolbar_location=None, title="부품별 불량품 건수")
        p1.vbar(x='parts', top='counts', width=0.9, source=source, legend_field="parts",
        line_color='white', fill_color=factor_cmap('parts', palette=Spectral6, factors=PARTS))

        p1.xgrid.grid_line_color = None
        p1.y_range.start = 0
        p1.y_range.end = max(counts)*2
        p1.legend.orientation = "horizontal"
        p1.legend.location = "top_center"


        #-------------------------------
        #  부품 불량 유형별 불량품 건수
        #-------------------------------
        df = pd.DataFrame(table_rows)
        group = df[df['part_name'] != '양품'].groupby(['part_name', 'part_category'])

        index_cmap = factor_cmap('part_name_part_category', palette=Spectral6, factors=sorted(df.part_name.unique()), end=1)

        p2 = figure(width=500, height=300, title="불량 유형별 불량품 건수",
                x_range=group, toolbar_location=None, 
                tooltips=[("count", "@inspection_number_count"), ("part_name, part_category", "@part_name_part_category")])

        p2.vbar(x='part_name_part_category', top='inspection_number_count', width=1, source=group,
        line_color="white", fill_color=index_cmap, )

        p2.y_range.start = 0
        p2.x_range.range_padding = 0.05
        p2.xgrid.grid_line_color = None
        p2.xaxis.major_label_orientation = 1.2
        p2.outline_line_color = None


        #-------------------------------
        #  Laying out in row
        #-------------------------------
        plot = layout(children=[[p1, p2]], sizing_mode='stretch_both')

        script, div = components(plot)

        kwargs = {'script1': script, 'div1': div}
        kwargs['title'] = 'bokeh-with-flask' 

        return render_template("admin_statistics.html", **kwargs)



