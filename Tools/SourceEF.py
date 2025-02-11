import datetime
from typing import Union

import efinance as ef
import pandas as pd
from pandas import DataFrame, Series

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 更改为支持中文的字体，例如 "SimHei"
matplotlib.rcParams['font.family'] = 'SimHei'  # 使用黑体（SimHei）
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为乱码问题
matplotlib.use('TkAgg')  # 或者选择一个适合的后端

pd.set_option('display.max_columns', None)  # None表示不限制列数
pd.set_option('display.width', 1000)  # 设置显示宽度，确保在一行内显示完整内容


class SourceEF:
    def __init__(self):
        '''
        data_type:
        ['股票代码', '股票名称', '涨跌幅', '最新价', '最高', '最低', '今开', '涨跌额', '换手率', '量比', '动态市盈率',
        '成交量', '成交额', '昨日收盘', '总市值', '流通市值', '行情ID', '市场类型', '更新时间', '最新交易日']
        '''
        self.stock_df = ef.stock.get_realtime_quotes()  # 最新所有的股票代码
        self.stock_code_list = self.stock_df['股票代码'].tolist()
        self.data_type = self.stock_df.columns.tolist()
        self.today = self.stock_df['最新交易日'].values[0]

        self.init_print()

    def init_print(self):
        print(f'最新交易日为：{self.today}')

    def get_stock_data(self, stock_code: Union[str, list[str]], start_date=None, end_date=None, klt=None):
        """
        获取指定股票代码的历史数据
        :param stock_code: 股票代码/代码列表
        :param start_date: 起始日期（可选）
        :param end_date: 结束日期（可选）
        :param kit: 其中 1 代表1分钟K线，5 代表5分钟K线，15 代表15分钟K线，30 代表30分钟K线，
        60 代表1小时K线，D 代表日线，W 代表周线，M 代表月线。
        :return: 股票数据的DataFrame
        """
        if not str(start_date).isdigit() or not str(end_date).isdigit():
            print("日期格式错误")
            return None
        # 判断是否为列表
        if isinstance(stock_code, list):
            if set(stock_code).issubset(set(self.stock_code_list)):
                return ef.stock.get_quote_history(stock_code, beg=start_date, end=end_date)
            else:
                print(f"股票代码列表存在非法股票代码")
                return None
        # 判断是否为单个股票代码
        if stock_code not in self.stock_code_list:
            print(f"股票代码{stock_code}不存在")
            return None
        if klt == None:  # 如果klt为空，则默认为日线
            try:
                return ef.stock.get_quote_history(stock_code, beg=start_date, end=end_date)
            except Exception as e:
                print(f"获取数据失败: {e}")
        else:  # 如果klt不为空，获取分钟数据
            try:
                return ef.stock.get_quote_history(stock_code, klt=klt)
            except Exception as e:
                print(f"获取数据失败: {e}")

    def get_name_by_code(self, stock_code):
        return self.stock_df.loc[self.stock_df['股票代码'] == stock_code]

    def export_to_csv(self, file_name=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")):
        self.stock_df.to_csv(file_name)

