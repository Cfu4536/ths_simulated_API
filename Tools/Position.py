class Position:
    '''
    {
        'stockcode': p['d_2102'],
        'stockname': p['d_2103'],
        'balance': p['d_2117'],
        'available': p['d_2121'],
        'amount': p['d_2164'],
        'price': p['d_2122'],
        'Profit/Loss': p['d_2147'],
        'Profit/Loss_ratio': p['d_3616'],
        'mktype': p['d_2108'],
        'gdzh': p['d_2106'],
        'mkcode': p['d_2167'],
    }
    '''
    def __init__(self, data:dict):
        self.stockcode = data.get('stockcode',None)
        self.stockname = data.get('stockname',None)
        self.balance = data.get('balance',None)
        self.available = data.get('available',None)
        self.amount = data.get('amount',None)
        self.price = data.get('price',None)
        self.Profit_Loss = data.get('Profit/Loss',None)
        self.Profit_Loss_ratio = data.get('Profit/Loss_ratio',None)
        self.mktype = data.get('mktype',None)
        self.gdzh = data.get('gdzh',None)
        self.mkcode = data.get('mkcode',None)

    def __str__(self):
        # return f'stockcode:{self.stockcode}, stockname:{self.stockname}, balance:{self.balance}, available:{self.available}, amount:{self.amount}, price:{self.price}, Profit_Loss:{self.Profit_Loss}, Profit_Loss_ratio:{self.Profit_Loss_ratio}, mktype:{self.mktype}, gdzh:{self.gdzh}, mkcode:{self.mkcode}'
        return f'股票代码: {self.stockcode}, 股票名称: {self.stockname}, 剩余数量: {self.balance}, 可用数量: {self.available}, 实际数量: {self.amount}, 价格: {self.price}, 盈亏: {self.Profit_Loss}, 盈亏比: {self.Profit_Loss_ratio}, 市场类型: {self.mktype}, 股东账户: {self.gdzh}, 市场代码: {self.mkcode}'
