# -*- coding: utf-8 -*-
"""
JQData 数据获取模块 - 修复版
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
    
    def __init__(self):
        # 直接从配置读取
        self.account = "13606066742"
        self.password = "SXM123456asd"
        self.authenticated = False
        # 试用期数据范围
        self.data_start = '2024-12-10'
        self.data_end = '2025-12-17'
    
    def auth(self):
        """认证登录"""
        if not JQDATA_AVAILABLE:
            print("❌ JQData SDK 未安装")
            return False
        
        try:
            auth(self.account, self.password)
            self.authenticated = True
            print(f"✅ JQData 认证成功！账号：{self.account}")
            print(f"📊 数据范围：{self.data_start} 至 {self.data_end}")
            return True
        except Exception as e:
            print(f"❌ JQData 认证失败：{e}")
            return False
    
    def get_stock_price(self, code, start_date=None, end_date=None):
        """获取股票行情数据"""
        if not self.authenticated:
            if not self.auth():
                return None
        
        # 使用试用期数据范围
        if end_date is None:
            end_date = self.data_end
        if start_date is None:
            start_date = self.data_start
        
        try:
            df = get_price(code, start_date=start_date, end_date=end_date)
            print(f"✅ 获取 {code} 行情数据成功，共 {len(df)} 条")
            return df
        except Exception as e:
            print(f"❌ 获取行情失败：{e}")
            return None
    
    def get_index_stocks(self, index_code):
        """获取指数成分股"""
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
    
    def get_fundamentals(self, query_object):
        """获取财务数据"""
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
    
    def get_money_flow(self, code, date=None):
        """获取资金流向"""
        if not self.authenticated:
            if not self.auth():
                return None
        
        if date is None:
            date = self.data_end
        
        try:
            df = get_money_flow(code, end_date=date)
            print(f"✅ 获取 {code} 资金流向成功")
            return df
        except Exception as e:
            print(f"❌ 获取资金流向失败：{e}")
            return None


def test_jqdata():
    """测试 JQData 连接"""
    print("=" * 60)
    print("🧪 JQData 连接测试")
    print("=" * 60)
    
    client = JQDataClient()
    
    if not client.auth():
        print("❌ 认证失败")
        return
    
    # 测试 1: 获取股票行情（使用试用期数据范围）
    print("\n【测试 1】获取平安银行行情数据 (2025-01-01 至 2025-12-17)")
    df = client.get_stock_price('000001.XSHE', 
                                 start_date='2025-01-01', 
                                 end_date='2025-12-17')
    if df is not None:
        print("\n最近 5 个交易日:")
        print(df.tail())
    
    # 测试 2: 获取沪深 300 成分股
    print("\n【测试 2】获取沪深 300 成分股")
    hs300 = client.get_index_stocks('000300.XSHG')
    if hs300:
        print(f"\n沪深 300 共 {len(hs300)} 只成分股")
        print(f"前 10 只：{hs300[:10]}")
    
    # 测试 3: 获取财务数据
    print("\n【测试 3】获取贵州茅台财务数据")
    from jqdatasdk import query, valuation
    finance_df = client.get_fundamentals(
        query(valuation.code, valuation.pe_ratio, valuation.pb_ratio, valuation.market_cap)
        .filter(valuation.code == '600519.XSHG')
    )
    if finance_df is not None and len(finance_df) > 0:
        print(f"\n贵州茅台:")
        print(f"PE: {finance_df['pe_ratio'].iloc[0]:.2f}")
        print(f"PB: {finance_df['pb_ratio'].iloc[0]:.2f}")
        print(f"市值：{finance_df['market_cap'].iloc[0]:.2f}亿")
    else:
        print("⚠️ 财务数据为空（试用期限制）")
    
    print("\n" + "=" * 60)
    print("✅ JQData 测试完成！")
    print("=" * 60)
    print("\n⚠️ 注意：试用账号数据范围为 2024-12-10 至 2025-12-17")
    print("如需更多数据，请升级正式版本")


if __name__ == "__main__":
    test_jqdata()
