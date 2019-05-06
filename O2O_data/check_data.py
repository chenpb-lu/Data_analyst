"""
file：查看文件的数据区间
author：陈鹏波
date：
"""
# 查看数据
import pandas as pd

name1 = ["User_id",'Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']
off_train = pd.read_csv('./data/ccf_offline_stage1_train.csv',names=name1)
#查看记录数
record_count = off_train.shape[0]
received_count = off_train['Date_received'].count()
coupon_count = len(off_train["Coupon_id"].value_counts())
user_count = len(off_train['User_id'].value_counts())
merchant_count = len(off_train['Merchant_id'].value_counts())
min_received = int(off_train["Date_received"].min())
max_received = int(off_train["Date_received"].max())
max_pay = int(off_train["Date"].max())
min_pay = int(off_train["Date"].min())
print('记录数为：',record_count)
print("优惠券领取记录：",received_count)
print("优惠券数量：",coupon_count)
print("用户数量：",user_count)
print("商家数量：",merchant_count)
print("最早领券时间;",min_received)
print("最晚领券时间;",max_received)
print("最早消费时间;",min_pay)
print("最晚消费时间;",max_pay)
