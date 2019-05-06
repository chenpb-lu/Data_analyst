"""
file：
author：
date：
"""
import pandas as pd
name1 = ["User_id",'Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']
name2 = ["User_id",'Merchant_id','Action','Coupon_id','Discount_rate','Date_received','Date']
name3 = ["User_id",'Merchant_id','Coupon_id','Discount_rate','Distance','Date_received']
dfoff = pd.read_csv('data/ccf_offline_stage1_train.csv',keep_default_na=False,names=name1)
dfon = pd.read_csv('data/ccf_online_stage1_train.csv',keep_default_na=False,names=name2)
dftest = pd.read_csv('data/ccf_offline_stage1_test_revised.csv',keep_default_na=False,names=name3)


a = dfoff.head(5)

print('有优惠卷，购买商品：%d' % dfoff[(dfoff['Date_received'] != 'null') & (dfoff['Date'] != 'null')].shape[0])
print('有优惠卷，未购商品：%d' % dfoff[(dfoff['Date_received'] != 'null') & (dfoff['Date'] == 'null')].shape[0])
print('无优惠卷，购买商品：%d' % dfoff[(dfoff['Date_received'] == 'null') & (dfoff['Date'] != 'null')].shape[0])
print('无优惠卷，未购商品：%d' % dfoff[(dfoff['Date_received'] == 'null') & (dfoff['Date'] == 'null')].shape[0])

print('Discount_rate 类型：\n',dfoff['Discount_rate'].unique())