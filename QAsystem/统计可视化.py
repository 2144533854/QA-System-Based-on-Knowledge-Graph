# -*- coding: utf-8 -*-
import base64
import io

import matplotlib.pyplot as plt
import matplotlib
import os

import numpy as np

from QAsystem.recomenod import DataForChart
from pyecharts import options as opts
from pyecharts.charts import Pie,Scatter

"""
绘制类，只负责绘制函数并返回给view类，通过调用数据类来获取数据
"""


class ChartForExpo:
    def __init__(self):
        self.dataclass=DataForChart()

    def savechart(self, plt):
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return plot_url

    def show1(self):
        matplotlib.rcParams['backend'] = 'TkAgg'
        '''
        backend（后端）为macosx。
        Agg支持文件写入，但不支持窗口显示（绘图），所以要改为其他GUI后端：TkAgg、Wx、QtAgg、Qt4Agg等
        '''
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(3)
        x_data,y_data=self.dataclass.get_len_and_name()
        bar_width = 0.35   #定义一个数字代表每个独立柱的宽度
        x_index = np.arange(1,8)
        print(sum(x_data))
        print(x_index)
        print(x_data,y_data)
        plt.yscale('log')
        rects1 = plt.bar(x_index, x_data, width=bar_width,color=['r','g','b', 'c', 'm', 'y'],label='legend1')            #参数：左偏移、高度、柱宽、透明度、颜色、图例
        #关于左偏移，不用关心每根柱的中心不中心，因为只要把刻度线设置在柱的中间就可以了
        plt.xticks(x_index, y_data)
        for i,j in zip(x_index,x_data): # zip 函数
            plt.text(i,j+0.01,"%d"%j,ha="center",fontsize=10)# plt.text 函数

        return self.savechart(plt)
        # print("plot_url=", plot_url)
        # # plt.show()
        # args = {"plot_url": plot_url}

    def show2(self):
        matplotlib.rcParams['backend'] = 'TkAgg'
        '''
        backend（后端）为macosx。
        Agg支持文件写入，但不支持窗口显示（绘图），所以要改为其他GUI后端：TkAgg、Wx、QtAgg、Qt4Agg等
        '''
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(3)
        x_data,y_data=self.dataclass.get_len_and_name2()
        print(sum(x_data))
        bar_width = 0.35   #定义一个数字代表每个独立柱的宽度
        x_index = np.arange(1,7)

        print(x_index)
        print(x_data,y_data)
        plt.yscale('log')
       #关于左偏移，不用关心每根柱的中心不中心，因为只要把刻度线设置在柱的中间就可以了
        plt.xticks(x_index, y_data)
        for i,j in zip(x_index,x_data): # zip 函数
            plt.text(i,j+0.01,"%d"%j,ha="center",fontsize=10)# plt.text 函数
        # plt.show()
        return self.savechart(plt)

    def show3(self):
        names,nums=self.dataclass.get_chart3_data()
        print(names)
        #创建饼图对象
        pie=Pie()
        pie.add("服装销售",[list(dic) for dic in zip(names,nums)],radius=["40%","75%"],rosetype="area")
        #设置配置信息(标题)
        pie.set_global_opts(legend_opts=opts.LegendOpts(orient='vertical',pos_top='1%',pos_left="2%"))#显示图例
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{pie}"))
        return pie.render_embed()


    def show4(self):
        x=[]
        for i in range(2004,2022):
            x.append(i)

        y1,y2 = self.dataclass.get_chart3_data()
        print(len(y1))

        # 创建散点图对象
        (
            Scatter(init_opts=opts.InitOpts(width="1600px", height="1000px"))
                .add_xaxis(xaxis_data=y1)
                .add_yaxis(
                series_name="",
                y_axis=y2,
                symbol_size=20,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .set_series_opts()
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="value", splitline_opts=opts.SplitLineOpts(is_show=True),min_=2010,max_=2023
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    min_=1,
                    max_=13
                ),
                tooltip_opts=opts.TooltipOpts(is_show=False),
            )
                .render()
        )

# ChartForExpo().show4()
