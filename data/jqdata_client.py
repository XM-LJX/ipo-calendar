# -*- coding: utf-8 -*-
"""
JQData 数据获取模块
聚宽金融数据 SDK
"""

import os
from datetime import datetime, timedelta

try:
    from jqdatasdk import *
    JQDATA_AVAILABLE = True
except ImportError:
    JQDATA_AVAILABLE = False
    print("⚠️ 未安装 jqdatasdk，运行：pip install jqdatasdk")


class JQDataClient:
    """JQData 数据客户端"""
    
    def __init__(self, account=None, password=None):
        self.account = account or os.getenv("JQDATA_ACCOUNT")
        self.password = password or os.getenv("JQDATA_PASSWORD")
        self.authenticated = False
    
    def auth(self):
        """认证登录"""
        if not JQDATA_AVAILABLE:
            print("❌ JQData SDK 未安装")
            return False
        
        try:
            auth(self.account, self.password)
            self.authenticated = True
            print(f"✅ JQData 认证成功！账号：{self.account}")
            
            # 获取账号信息
            info = get_account_info()
            print(f"📊 账号有效期：{info.get('expire_date', '未知')}")
            print(f"📊 每日流量：{info.get('daily_flow', '未知')}")
            
            return True
        except Exception as e:
            print(f"❌ JQData 认证失败：{e}")
            return False
    
    def get_stock_price(self, code, start_date=None, end_date=None, frequency='daily'):
        """
        获取股票行情数据
        
        Args:
            code: 股票代码（如：000001.XSHE）
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
            frequency: 频率（daily/weekly/monthly/minute）
        
        Returns:
            DataFrame: 行情数据
        """
        if not self.authenticated:
            if not self.auth():
                return None
        
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        try:
            df = get_price(code, start_date=start_date, end_date=end_date, frequency=frequency)
            print(f"✅ 获取 {code} 行情数据成功，共 {len(df)} 条")
            return df
        except Exception as e:
            print(f"❌ 获取行情失败：{e}")
            return None
    
    def get_fundamentals(self, query_object):
        """
        获取财务数据
        
        Args:
            query_object: 聚宽 query 对象
        
        Returns:
            DataFrame: 财务数据
        """
        if not self.authenticated:
            if not self.auth():
                return None
        
        try:
            df = get_fundamentals(query_object)
            print(f"✅ 获取财务数据成功，共 {len(df)} 条")
            return df
        except Exception as e:
            print(f"❌ 获取财务数据失败：{e}")
            return None
    
    def get_new_stocks(self, start_month=None, end_month=None):
        """
        获取 IPO 新股数据
        
        Args:
            start_month: 开始月份（YYYY-MM）
            end_month: 结束月份（YYYY-MM）
        
        Returns:
            DataFrame: IPO 数据
        """
        if not self.authenticated:
            if not self.auth():
                return None
        
        if end_month is None:
            end_month = datetime.now().strftime('%Y-%m')
        if start_month is None:
            start_month = (datetime.now() - timedelta(days=90)).strftime('%Y-%m')
        
        try:
            df = get_new_stocks(start_month, end_month)
            print(f"✅ 获取 IPO 数据成功，共 {len(df)} 只")
            return df
        except Exception as e:
            print(f"❌ 获取 IPO 数据失败：{e}")
            return None
    
    def get_index_stocks(self, index_code):
        """
        获取指数成分股
        
        Args:
            index_code: 指数代码（如：000300.XSHG）
        
        Returns:
            list: 成分股列表
        """
        if not self.authenticated:
            if not self.auth():
                return []
        
        try:
            stocks = get_index_stocks(index_code)
            print(f"✅ 获取 {index_code} 成分股成功，共 {len(stocks)} 只")
            return stocks
        except Exception as e:
            print(f"❌ 获取成分股失败：{e}")
            return []
    
    def get_money_flow(self, code, date=None):
        """
        获取资金流向
        
        Args:
            code: 股票代码
            date: 日期（YYYY-MM-DD）
        
        Returns:
            DataFrame: 资金流向数据
        """
        if not self.authenticated:
            if not self.auth():
                return None
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            df = get_money_flow(code, end_date=date)
            print(f"✅ 获取 {code} 资金流向成功")
            return df
        except Exception as e:
            print(f"❌ 获取资金流向失败：{e}")
            return None


# 测试函数
def test_jqdata():
    """测试 JQData 连接"""
    print("=" * 60)
    print("🧪 JQData 连接测试")
    print("=" * 60)
    
    client = JQDataClient()
    
    if not client.auth():
        print("❌ 认证失败")
        return
    
    # 测试 1: 获取股票行情
    print("\n【测试 1】获取平安银行行情数据")
    df = client.get_stock_price('000001.XSHE', 
                                 start_date='2026-03-01', 
                                 end_date='2026-03-19')
    if df is not None:
        print(df.tail())
    
    # 测试 2: 获取 IPO 数据
    print("\n【测试 2】获取 2026 年 IPO 数据")
    ipo_df = client.get_new_stocks('2026-01', '2026-03')
    if ipo_df is not None:
        print(f"2026 年 Q1 共 {len(ipo_df)} 只 IPO")
        print(ipo_df.head())
    
    # 测试 3: 获取沪深 300 成分股
    print("\n【测试 3】获取沪深 300 成分股")
    hs300 = client.get_index_stocks('000300.XSHG')
    if hs300:
        print(f"沪深 300 共 {len(hs300)} 只成分股")
        print(f"前 10 只：{hs300[:10]}")
    
    print("\n" + "=" * 60)
    print("✅ JQData 测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_jqdata()
