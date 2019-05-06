"""
file：将数据集进行预处理储存，方便下一步执行
author：
date：
"""
import pandas as pd
# name1 = ["User_id",'Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']
# dfoff = pd.read_csv('data/ccf_offline_stage1_train.csv',names=name1)
# #判断是否为满减折扣
# dfoff['is_manjian'] = dfoff['Discount_rate'].map(lambda x : 1 if ':' in str(x) else 0)
# #找出优惠的最低消费
# dfoff['min_pay_of_manjian'] = dfoff['Discount_rate'].map(lambda x : -1 if ":" not in str(x) else int(str(x).split(':')[0]))
# #将满减的优惠也转换成折扣率
# dfoff['discount_rate'] = dfoff['Discount_rate'].map(lambda x : float(x) if ':' not in str(x) else (float(str(x).split(':')[0]) - float(str(x).split(':')[1]))/float(str(x).split(':')[0]))
#
# #设置一列为datel类型发日期数据领取优惠券日期数据
# dfoff['date_received'] = pd.to_datetime(dfoff['Date_received'],format='%Y%m%d')
# #设置一列为datel类型发日期数据的消费日期数据
# dfoff['date'] = pd.to_datetime(dfoff['Date'],format='%Y%m%d')
#
# # 查看缺省值
# # print(dfoff.isnull().any())
# # 统计缺省值的比例
# # print(dfoff.isnull().sum() / len(dfoff))
#
# # 将距离为空的数据进行处理
# dfoff['Distance'].fillna(-1,inplace= True)
# # 标记距离是否为空
# dfoff['null_Distance'] = dfoff['Distance'].map(lambda x : 1 if x == -1 else 0)
#
# # 将日期转换成周几，便于分析
# dfoff['weekday_Receive'] = dfoff['date_received'].apply(lambda  x : x.isoweekday())
#
# # 保存处理后的训练集
# # dfoff.to_csv('./data2/offline_data.csv',index=False,header=True)
#
# dfoff['label'] = list(map(lambda x ,y : 1 if (x - y).total_seconds()/60*60*24 <= 15 else 0 ,dfoff['date'],dfoff['date_received']))
#
# # drill_section = dfoff[dfoff['date_received'].isin(pd.date_range('2016/3/2', periods= 60))]
# #
# # verify_section = dfoff[dfoff['date_received'].isin(pd.date_range('2016/1/16', periods= 60))]
def pre(dfoff):
    dfoff['is_manjian'] = dfoff['Discount_rate'].map(lambda x: 1 if ':' in str(x) else 0)
    dfoff['min_pay_of_manjian'] = dfoff['Discount_rate'].map(
        lambda x: -1 if ":" not in str(x) else int(str(x).split(':')[0]))
    dfoff['discount_rate'] = dfoff['Discount_rate'].map(lambda x: float(x) if ':' not in str(x) else (float(
        str(x).split(':')[0]) - float(str(x).split(':')[1])) / float(str(x).split(':')[0]))
    dfoff['date_received'] = pd.to_datetime(dfoff['Date_received'], format='%Y%m%d')
    dfoff['Distance'].fillna(-1, inplace=True)
    dfoff['null_Distance'] = dfoff['Distance'].map(lambda x: 1 if x == -1 else 0)
    dfoff['weekday_Receive'] = dfoff['date_received'].apply(lambda x: x.isoweekday())
    return dfoff



