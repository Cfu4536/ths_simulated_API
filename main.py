import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame, Series

from Tools.SourceEF import SourceEF


def filter_stocks_by_price_change(df: DataFrame, min_change: float = None, max_change: float = None):
    '''
    过滤股票数据，只保留涨跌幅在指定范围内的股票
    :param df:
    :param min_change:
    :param max_change:
    :return:
    '''
    # 将 '涨跌幅' 列转换为浮点型
    df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')

    # 过滤涨幅在指定范围内的股票
    if min_change is None and max_change is None:
        filtered_stocks = df[(df['涨跌幅'] >= min_change) & (df['涨跌幅'] <= max_change)]
    elif min_change is None:
        filtered_stocks = df[df['涨跌幅'] <= max_change]
    elif max_change is None:
        filtered_stocks = df[df['涨跌幅'] >= min_change]
    else:
        filtered_stocks = df[(df['涨跌幅'] >= 3.0) & (df['涨跌幅'] <= 5.0)]

    # 提取股票代码
    filtered_stock_codes = filtered_stocks['股票代码'].tolist()

    return filtered_stock_codes


def filter_stocks_by_volume_ratio(df: DataFrame, min_ratio: float = None, max_ratio: float = None) -> DataFrame:
    """
    过滤股票数据，只保留量比大于或等于指定值的股票（默认大于等于1）
    :param df: 包含股票数据的DataFrame
    :param min_ratio: 最小量比
    :return: 符合条件的股票数据DataFrame
    """

    # 将 '量比' 列转换为浮点型
    df['量比'] = pd.to_numeric(df['量比'], errors='coerce')

    # 过滤量比大于或等于min_ratio的股票
    if min_ratio is not None and max_ratio is not None:
        filtered_stocks = df[(df['量比'] >= min_ratio) & (df['量比'] <= max_ratio)]
    elif max_ratio is None:
        filtered_stocks = df[df['量比'] >= min_ratio]
    elif min_ratio is None:
        filtered_stocks = df[df['量比'] <= max_ratio]
    else:
        filtered_stocks = df[(df['量比'] >= 1)]
    # 提取股票代码
    filtered_stock_codes = filtered_stocks['股票代码'].tolist()

    return filtered_stock_codes


def filter_stocks_by_turnover_rate(df: DataFrame, min_rate: float = None, max_rate: float = None) -> list:
    """
    过滤股票数据，只保留换手率在指定范围内的股票，默认5-10
    :param df: 包含股票数据的DataFrame，必须包含 '换手率' 和 '股票代码' 列
    :param min_rate: 最小换手率 （百分数形式）
    :param max_rate: 最大换手率
    :return: 符合条件的股票代码列表
    """

    # 将 '换手率' 列转换为浮点型
    df['换手率'] = pd.to_numeric(df['换手率'], errors='coerce')

    # 过滤换手率
    if min_rate is not None and max_rate is not None:
        filtered_stocks = df[(df['换手率'] >= min_rate) & (df['换手率'] <= max_rate)]
    elif max_rate is not None:
        filtered_stocks = df[(df['换手率'] <= max_rate)]
    elif min_rate is not None:
        filtered_stocks = df[(df['换手率'] >= min_rate)]
    else:
        filtered_stocks = df[(df['换手率'] >= 5) & (df['换手率'] <= 10)]

    # 提取股票代码
    filtered_stock_codes = filtered_stocks['股票代码'].tolist()

    return filtered_stock_codes


def filter_stocks_by_market_cap(df: DataFrame, min_cap: float = None, max_cap: float = None) -> list:
    """
    过滤股票数据，只保留市值在指定范围内的股票,默认大于等于50亿
    :param df: 包含股票数据的DataFrame，必须包含 '市值' 和 '股票代码' 列
    :param min_cap: 最小市值 (默认None，即没有下限)
    :param max_cap: 最大市值 (默认None，即没有上限)
    :return: 符合条件的股票代码列表
    """
    # 将 '市值' 列转换为浮点型
    df['总市值'] = pd.to_numeric(df['总市值'], errors='coerce')

    # 过滤总市值
    if min_cap is not None and max_cap is not None:
        filtered_stocks = df[(df['总市值'] >= min_cap) & (df['总市值'] <= max_cap)]
    elif min_cap is not None:
        filtered_stocks = df[df['总市值'] >= min_cap]
    elif max_cap is not None:
        filtered_stocks = df[df['总市值'] <= max_cap]
    else:
        filtered_stocks = df[(df['总市值'] >= 50e8)]

    # 提取股票代码
    filtered_stock_codes = filtered_stocks['股票代码'].tolist()

    return filtered_stock_codes


def filter_stocks_by_cv(df: Series, threshold: float = 0.2):
    std = df.std()
    cv = std / df.mean()

    df.plot(kind='bar', color='skyblue')
    plt.title('Mean of Stocks')
    plt.xlabel('Stock')
    plt.ylabel('Mean Value')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.title(f'cv:{cv}')
    plt.show()

    if 1 - threshold <= cv <= 1 + threshold:
        return True
    else:
        return False


# 使用示例
if __name__ == "__main__":
    source = SourceEF()

    # print(source.today)
    # print(source.stock_df)
    # print(source.stock_code_list)
    # print(source.data_type)
    # source.export_to_csv()

    # stock_code_set = set(filter_stocks_by_price_change(source.stock_df, min_change=3.0, max_change=5.0))
    # print(len(stock_code_set))
    # stock_code_set = stock_code_set & set(filter_stocks_by_volume_ratio(source.stock_df, min_ratio=1.0))
    # print(len(stock_code_set))
    # stock_code_set = stock_code_set & set(filter_stocks_by_turnover_rate(source.stock_df, min_rate=5.0, max_rate=10.0))
    # print(len(stock_code_set))
    # stock_code_set = stock_code_set & set(filter_stocks_by_market_cap(source.stock_df, min_cap=50e8))
    # print(len(stock_code_set))
    #
    # for stock_code in stock_code_set:
    #     print(source.get_name_by_code(stock_code=stock_code))

    # print(source.get_stock_data(stock_code='600519'))  # 以贵州茅台为例
    # print(source.get_stock_data(stock_code='600519', start_date='20250101', end_date='20250124'))  # 以贵州茅台为例
    # print(source.get_stock_data(stock_c4ode='600519', start_date='20250101', end_date='20250124', klt=1))  # 以贵州茅台为例
    # print(source.get_stock_data(stock_code=source.stock_code_list[:15],start_date=20220815, end_date=20220815, klt=1))

    # for code in stock_code_set:
    #     mt = source.get_stock_data(stock_code=code, start_date='20250101', end_date='20250124')
    #     print(filter_stocks_by_cv(mt['成交量'], threshold=20.2))

    df = source.get_stock_data(stock_code='003030', start_date='20240101', end_date='20250124')
    df.to_csv("test.csv")
