import requests

from Order import Order
from Position import Position


class ThsDT:
    def __init__(self):
        self.buy_url = 'https://mncg.10jqka.com.cn/cgiwt/delegate/tradestock/'
        self.sell_url = 'https://mncg.10jqka.com.cn/cgiwt/delegate/tradestock/'
        self.cancel_url = 'https://mncg.10jqka.com.cn/cgiwt/delegate/cancelDelegated/'
        self.get_order_url = 'https://mncg.10jqka.com.cn/cgiwt/delegate/updateclass/'
        self.get_chicang_url = 'https://mncg.10jqka.com.cn/cgiwt/delegate/updateclass'
        self.qry_stock_url = 'https://mncg.10jqka.com.cn/cgiwt/delegate/qrystock/'

        self.headers = {
            'host': 'mncg.10jqka.com.cn',
            'origin': 'https://mncg.10jqka.com.cn',
            'referer': 'https://mncg.10jqka.com.cn/cgiwt/index/index',
            'cookie': 'u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=yiOhwrKwFU6atVfWUpvzI2UihB7NKsoGIFTGD1hI67346G8Uat7rsYN3YNroKXaxHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=B3C5C784163548F59362718A68218961; u_ttype=WEB; ttype=WEB; user=MDptb180NTY1MDIzNDQ6Ok5vbmU6NTAwOjQ2NjUwMjM0NDo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNDo6OjQ1NjUwMjM0NDoxNzM3NDYwODM5Ojo6MTUzMTU0MzUwMDo2MDQ4MDA6MDoxOTQxMmNjMzU1MTEwNTBkNTMzMWU1Y2YxMzhkNWJmMWY6ZGVmYXVsdF80OjE%3D; userid=456502344; u_name=mo_456502344; escapename=mo_456502344; ticket=836eef78afe2371826539033a379cda5; user_status=0; utk=26bd93f088b41338c459ff7071751627; spversion=20130314; isSaveAccount=0; historystock=601988%7C*%7C300044; log=; Hm_lvt_722143063e4892925903024537075d0d=1737460803,1737529519; Hm_lpvt_722143063e4892925903024537075d0d=1737529519; HMACCOUNT=663F7C2F7358C2B0; Hm_lvt_929f8b362150b1f77b477230541dbbc2=1737460804,1737529519; Hm_lpvt_929f8b362150b1f77b477230541dbbc2=1737529519; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1737460804,1737529519; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1737529553; PHPSESSID=5e6d72428b2c4d15a4c0e3d94f599522; v=A0XIyTmIjlQoVqqILHRKsAraVIp6AvunQ7Td3kegARKLT2v0D1IJZNMG7bzU',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        }
        self.gdzh = 'A478135763'

        self.ky_fund = 0
        self.init_info()

    def init_info(self):
        print("->当前持仓:")
        for chicang in self.get_chicang():
            print(chicang)
        print()
        print("->当前可用资金:", self.get_fund())
        print()
        print("->当前委托:")
        for order in self.get_order():
            print(order)
        print()


    def buy(self, stock_code:str, amount:int, price=None):
        '''
        买入，price=none，则按最新价
        :param stock_code:代码
        :param price: 价格
        :param amount: 数量
        :return:
        '''
        amount = int(amount / 100) * 100
        stock_info = self.qry_stock(stock_code=stock_code,cmd='cmd_wt_mairu')
        if price is None:
            price = stock_info['cur_price']
        # if amount > stock_info['can_buy']:# 如果买入数量大于可买数量，则按可买数量买入
        #     amount = stock_info['can_buy']
        mkcode = stock_info['mkcode']
        data = {
            'type': 'cmd_wt_mairu',
            'mkcode': mkcode,
            'gdzh': self.gdzh,
            'stockcode': stock_code,
            'price': price,
            'amount': amount,
        }
        print(f'【买入】{stock_code} {price} {amount}')
        resp = requests.post(self.buy_url, headers=self.headers, data=data)
        ret_code = resp.json()['errorcode']
        err_msg = resp.json()['errormsg']
        print('【提示】', ret_code, err_msg)
        return ret_code

    def sell(self, position: Position, amount:int, price=None):
        '''
        卖出，price=none 则按最新价
        :param position:
        :param price:
        :param amount:
        :return:
        '''
        amount = int(amount / 100) * 100
        stock_info = self.qry_stock(position.stockcode,cmd='cmd_wt_maichu')
        if price is None:
            price = stock_info['cur_price']
        if amount > stock_info['can_buy']:# 如果买入数量大于可买数量，则按可买数量买入
            amount = stock_info['can_buy']
        data = {
            'type': 'cmd_wt_maichu',
            'mkcode': stock_info['mkcode'],
            'gdzh': position.gdzh,
            'stockcode': position.stockcode,
            'price': price,
            'amount': amount,
        }
        print(f'【卖出】{position.stockcode} {position.stockname} {price} {amount}')
        resp = requests.post(self.sell_url, headers=self.headers, data=data)
        ret_code = resp.json()['errorcode']
        err_msg = resp.json()['errormsg']
        print('【提示】', ret_code, err_msg)
        return ret_code

    def cancel(self, order: Order):
        '''
        撤单
        :param order:
        :return:
        '''
        htbh = order.htbh
        wtrq = order.wtrq
        data = {
            'htbh': htbh,
            'wtrq': wtrq,
        }
        print(f'【撤单】{order}')
        resp = requests.post(self.cancel_url, headers=self.headers, data=data)
        ret_code = resp.json()['errorcode']
        err_msg = resp.json()['errormsg']
        print('【提示】', ret_code, err_msg)
        return ret_code

    def get_order(self) -> list[Order]:
        '''
        查询委托订单
        :return:委托订单列表
        '''
        data = {
            'type': 'cmd_qu_chedan',
            'updateClass': 'qryzijin|qryChedan|',
        }
        resp = requests.post(self.get_order_url, headers=self.headers, data=data)
        info = resp.json()['result']['qryChedan']['result']['list']
        self.ky_fund = resp.json()['result']['qryzijin']['result']['data']['kyje']
        ret_list = []
        for d in info:
            ret_list.append(Order(
                {
                    'time': d['d_2140'],
                    'htbh': d['d_2135'],
                    'wtrq': d['d_2139'],
                    'stockcode': d['d_2102'],
                    'stockname': d['d_2103'],
                    'price': d['d_2127'],
                    'amount': d['d_2126'],
                    'type': d['d_2109'],
                    'status': d['d_2105'],
                    'mktype': d['d_2108'],
                }
            ))
        return ret_list

    def get_chicang(self) -> list[Position]:
        '''
        查询持仓信息，更新可用资金
        :return:持仓信息
        '''
        data = {
            'type': 'cmd_wt_mairu',
            'updateClass': 'qryzijin|qryChicang|',
        }
        resp = requests.post(self.get_chicang_url, headers=self.headers, data=data)
        info = resp.json()['result']['qryChicang']['result']['list']
        self.ky_fund = resp.json()['result']['qryzijin']['result']['data']['kyje']
        ret_list = []
        for p in info:
            ret_list.append(Position(
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
            ))
        return ret_list
    def get_fund(self):
        '''
        查询可用资金
        :return:
        '''
        data = {
            'type': 'cmd_wt_mairu',
            'updateClass': 'qryzijin|',
        }
        resp = requests.post(self.get_chicang_url, headers=self.headers, data=data)
        self.ky_fund = resp.json()['result']['qryzijin']['result']['data']['kyje']
        return self.ky_fund

    def qry_stock(self, stock_code: str,cmd:str):
        '''
        查询当前股票信息
        :param stock_code:
        :return: 当前价格、可买数量、市场代码、五档信息
        '''
        data = {
            'type': cmd,
            'stockcode': stock_code,
        }
        resp = requests.post(self.qry_stock_url, headers=self.headers, data=data)
        info = resp.json()['result']['data']
        ret_data = {
            'cur_price': float(info['st_price']),
            'can_buy': int(info['canbuy']),
            'mkcode': info['mkcode'],
            'wudang': {
                "buy_price": [info['mrjw1'], info['mrjw2'], info['mrjw3'], info['mrjw4'], info['mrjw5']],
                "buy_amount": [info['mrsl1'], info['mrsl2'], info['mrsl3'], info['mrsl4'], info['mrsl5']],
                "sell_price": [info['mcjw1'], info['mcjw2'], info['mcjw3'], info['mcjw4'], info['mcjw5']],
                "sell_amount": [info['mcsl1'], info['mcsl2'], info['mcsl3'], info['mcsl4'], info['mcsl5']],
            }
        }
        return ret_data

def cancel_all(ths):
    for order in ths.get_order():
        ths.cancel(order)
def main():
    ths = ThsDT()
    cancel_all(ths)
    # ths.buy(stock_code='601988', price=5.41, amount=100)
    # ths.buy(stock_code='601988', amount=2600)
    # ths.sell(ths.get_chicang()[0], price=8.14, amount=200)
    # ths.sell(ths.get_chicang()[0], amount=200)
    # ths.cancel(ths.get_order()[0])
    # print(ths.get_fund())
    # print(ths.get_chicang())
    # print(ths.get_order())



if __name__ == '__main__':
    main()
