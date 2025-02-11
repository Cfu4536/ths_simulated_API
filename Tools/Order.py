class Order:
    '''
    { "time": "20:13:48",
    "htbh": "4711504428",
    "wtrq": "20250121",
    "stockcode": "601988",
    "stockname": "中国银行",
    "price": "5.410",
    "amount": "2600",
    "type": "买入",
    "status": "未成交",
    "mktype": "上海Ａ股"
  }
    '''
    def __init__(self, data:dict):
        self.time = data.get('time')  # 获取时间
        self.htbh = data.get('htbh')  # 获取合同编号
        self.wtrq = data.get('wtrq')  # 获取委托日期
        self.stockcode = data.get('stockcode')  # 获取股票代码
        self.stockname = data.get('stockname')  # 获取股票名称
        self.price = data.get('price')  # 获取委托价格
        self.amount = data.get('amount')  # 获取委托数量
        self.type = data.get('type')  # 获取委托类型
        self.status = data.get('status')  # 获取状态
        self.mktype = data.get('mktype')  # 获取市场类型

    def __str__(self):
        return f'时间: {self.time}, 合同编号: {self.htbh}, 委托日期: {self.wtrq}, 股票代码: {self.stockcode}, 股票名称: {self.stockname}, 委托价格: {self.price}, 委托数量: {self.amount}, 委托类型: {self.type}, 状态: {self.status}, 市场类型: {self.mktype}'
