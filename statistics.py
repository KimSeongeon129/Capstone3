from flask import g, Flask, render_template
from flask import jsonify,url_for,redirect,request,Blueprint
import requests
import json

import pandas as pd
import numpy as np
import math

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, MultiChoice, CustomJS, value, RangeTool
from bokeh.layouts import layout
from bokeh.embed import components
from bokeh.palettes import PuBuGn6
from bokeh.transform import factor_cmap

from parts import duct_def, pipe_def, hull_def, cable_def, lagging_def, defect_dict

bp= Blueprint('statistics',__name__)

@bp.route('/statistics')#이미지 결과페이지
def imgUpload_result():
        db_cursor = g.db.cursor()
        db_cursor.execute('SELECT * FROM result')
        table_rows = db_cursor.fetchall()
        df = pd.DataFrame(table_rows)

        PARTS = sorted(['덕트', '선박 배관', '선체', '케이블', '보온재'])

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
        p1_cmap = factor_cmap('parts', palette=PuBuGn6, factors=PARTS)
        
        p1 = figure(x_range=PARTS, width=500, height=600, toolbar_location=None, title="부품별 불량품 건수")
        p1.vbar(x='parts', top='counts', width=0.9, source=source,
                line_color='white', fill_color=p1_cmap)

        p1.xgrid.grid_line_color = None
        p1.y_range.start = 0
        p1.legend.orientation = "horizontal"
        p1.legend.location = "top_center"


        #-------------------------------
        #  부품 불량 유형별 불량품 건수
        #-------------------------------
        defect_duct = ['덕트' for defect in duct_def]
        defect_pipe = ['선박 배관' for defect in pipe_def]
        defect_hull = ['선체' for defect in hull_def]
        defect_cable = ['케이블' for defect in cable_def]
        defect_lagging = ['보온재' for defect in lagging_def]
        part_name = defect_duct + defect_pipe + defect_hull + defect_cable + defect_lagging

        defect_duct = [defect for defect in duct_def]
        defect_pipe = [defect for defect in pipe_def]
        defect_hull = [defect for defect in hull_def]
        defect_cable = [defect for defect in cable_def]
        defect_lagging = [defect for defect in lagging_def]
        part_category = defect_duct + defect_pipe + defect_hull + defect_cable + defect_lagging

        count = [0 for i in part_category]
        for p in df[df['part_name'] != '양품']['part_category'].value_counts().index:
                count[part_category.index(p)] = df[df['part_name'] != '양품']['part_category'].value_counts()[p]
        
        kor_part_category = [defect_dict[c]['한글명'] for c in part_category]
        
        df1 = pd.DataFrame({'part_name' : part_name,
                   'part_category' : kor_part_category ,
                   'count' : count})
        group = df1.groupby(['part_name', 'part_category'])
        
        p2_cmap = factor_cmap('part_name_part_category', palette=PuBuGn6, factors=PARTS, end=1)
        
        p2 = figure(width=700, height=600, title="불량 유형별 불량품 건수",
                x_range=group, toolbar_location=None,  margin = (0, 0, 0, 70),
                tooltips=[("count", "@count_max"), ("part_name, part_category", "@part_name_part_category")])
        p2.vbar(x='part_name_part_category', top='count_max', width=1, source=group,
                line_color="white", fill_color = p2_cmap)

        p2.y_range.start = 0
        p2.x_range.range_padding = 0.05
        p2.xgrid.grid_line_color = None
        p2.xaxis.major_label_orientation = 1.2
        p2.outline_line_color = None
        
        #-------------------------------
        #  총 검사 수
        #-------------------------------

        p3 = figure(width=170, height=200,
                active_drag = None,
                toolbar_location=None,
                margin = (0, 0, 0, 70))
        p3.xgrid.visible = False
        p3.ygrid.visible = False
        p3.xaxis.visible = False
        p3.yaxis.visible = False
        p3.outline_line_color = 'white'
        p3.title = "총 검사 수"
        p3.title.align = 'center'
        
        p3.text(x="x", y="y", text="text", text_align="center", text_font_size="30px", text_font=value("Verdana"),text_font_style="normal",
                source=ColumnDataSource(pd.DataFrame.from_records([dict(
                                x=100,
                                y=50,
                                text=f"{len(df)}",
                                color="black",)])))
        
        #-------------------------------
        #  총 불량품 수
        #-------------------------------
        
        p4 = figure(width=170, height=200,
                active_drag = None,
                toolbar_location=None)
        
        p4.xgrid.visible = False
        p4.ygrid.visible = False
        p4.xaxis.visible = False
        p4.yaxis.visible = False
        p4.outline_line_color = 'white'
        p4.title = "총 불량품 수"
        p4.title.align = 'center'

        p4.text(x="x", y="y", text="text", text_align="center", text_font_size="30px", text_font=value("Verdana"),text_font_style="normal",
                source=ColumnDataSource(pd.DataFrame.from_records([dict(
                                x=100,
                                y=50,
                                text=f"{len(df[df['part_name'] != '양품'])}",
                                color="black",)])))
        
        #-------------------------------
        #  불량품 수
        #-------------------------------
        
        p5 = figure(width=170, height=200,
                active_drag = None,
                toolbar_location=None)
        p5.xgrid.visible = False
        p5.ygrid.visible = False
        p5.xaxis.visible = False
        p5.yaxis.visible = False
        p5.outline_line_color = 'white'
        p5.title = "불량품 수"
        p5.title.align = 'center'
        
        p5.text(x="x", y="y", text="text", text_align="center", text_font_size="30px", text_font=value("Verdana"),text_font_style="normal",
                source=ColumnDataSource(pd.DataFrame.from_records([dict(
                                x=100,
                                y=50,
                                text=f"{len(df[df['part_name'] != '양품'])}",
                                color="black",)])))
        
        #-------------------------------
        #  시간별 불량품 수
        #-------------------------------
        
        df_time = df.copy()
        df_time['dates'] = pd.to_datetime(df['date']).dt.date
        p6_index = df_time.groupby(['dates'])['part_id'].agg(['count'])['count'].index
        p6_values = df_time.groupby(['dates'])['part_id'].agg(['count'])['count'].values

        p6_index = np.array(p6_index, dtype=np.datetime64)
        source = ColumnDataSource(data=dict(date=p6_index, count=p6_values))

        p6 = figure(height=300, width=1200, tools="xpan", toolbar_location=None,
                x_axis_type="datetime", x_axis_location="above",
                background_fill_color="#efefef",x_range=(p6_index[1], p6_index[2]),
                margin = (70, 0, 0, 0))

        p6.line('date', 'count', source=source)
        p6.yaxis.axis_label = '불량품 수'
        p6.title = "시간별 불량품 수"
        p6.title.align = 'center'

        select = figure(title="선택 박스를 드래그하여 확대할 시간대를 설정하세요",
                        height=130, width=1200, y_range=p6.y_range,
                        x_axis_type="datetime", y_axis_type=None,
                        tools="", toolbar_location=None, background_fill_color="#efefef")

        range_tool = RangeTool(x_range=p6.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2

        select.line('date', 'count', source=source)
        select.ygrid.grid_line_color = None
        select.add_tools(range_tool)
        select.toolbar.active_multi = range_tool

        #-------------------------------
        #  레이아웃
        #-------------------------------

        multi_choice = MultiChoice(value=PARTS, options=PARTS, title='parts:',width=600, height=200)

        callback = CustomJS(args=dict(source=source,
                                      p1 = p1, 
                                      p2 = p2, p2_index = group.describe().index, 
                                      p5 = p5,
                                      multi_choice=multi_choice), code="""    
                var selected = multi_choice.value;
                var p2_index_list = [];
                p1.x_range.factors = selected;
                
                for(var i=0; i<selected.length; i++){
                        for(var j=0; j<p2_index.length; j++){
                                if(p2_index[j][0] == selected[i]){
                                        p2_index_list.push(p2_index[j]);
                                }
                        }
                }
                p2.x_range.factors = p2_index_list;
                console.log(p5.text)
        """)
        multi_choice.js_on_change('value', callback)

        plot = layout(children=[[multi_choice,p3, p4, p5],
                                [p1, p2],
                                [p6],
                                [select]], sizing_mode='fixed')

        script, div = components(plot)

        kwargs = {'script1': script, 'div1': div}
        kwargs['title'] = 'bokeh-with-flask' 

        return render_template("statistics.html", **kwargs)
