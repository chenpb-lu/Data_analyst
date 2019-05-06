"""
file：提取特征
author：陈鹏波
date：
"""
import pandas as pd
import  math
def get_feature(dfoff):
    # 优惠券类型转换，会把null也转换
    dfoff['Coupon_id'] = dfoff['Coupon_id'].map(lambda x: 0 if math.isnan(x) else int(x))
    dfoff['Date_received'] = dfoff['Date_received'].map(lambda x: 0 if math.isnan(x) else int(x))
    dfoff['cnt'] = 1  # 便于提取特征
    feature = dfoff.copy()
    # 用户领券数
    keys = ["User_id"]
    prefixs = 'simple_' + '_'.join(keys) + '_'
    pivot = pd.pivot_table(dfoff, index=keys, values='cnt', aggfunc=len)
    pivot = pd.DataFrame(pivot).rename(columns={'cnt': prefixs + 'received_cnt'}).reset_index()
    feature = pd.merge(feature, pivot, on=keys, how='left')

    # 用户领取某个优惠券
    keys = ["User_id", 'Coupon_id']
    prefixs = 'simple_' + '_'.join(keys) + '_'
    pivot = pd.pivot_table(dfoff, index=keys, values='cnt', aggfunc=len)
    pivot = pd.DataFrame(pivot).rename(columns={'cnt': prefixs + 'received_cnt'}).reset_index()
    feature = pd.merge(feature, pivot, on=keys, how='left')

    # 用户当天的领券数
    keys = ["User_id", 'Date_received']
    prefixs = 'simple_' + '_'.join(keys) + '_'
    pivot = pd.pivot_table(dfoff, index=keys, values='cnt', aggfunc=len)
    pivot = pd.DataFrame(pivot).rename(columns={'cnt': prefixs + 'received_cnt'}).reset_index()
    feature = pd.merge(feature, pivot, on=keys, how='left')

    # 用户当天领取某个特定的优惠券
    keys = ["User_id", "Coupon_id", 'Date_received']
    prefixs = 'simple_' + '_'.join(keys) + '_'
    pivot = pd.pivot_table(dfoff, index=keys, values='cnt', aggfunc=len)
    pivot = pd.DataFrame(pivot).rename(columns={'cnt': prefixs + 'received_cnt'}).reset_index()
    feature = pd.merge(feature, pivot, on=keys, how='left')

    # 用户是否当天多次领取某个特定的优惠券
    keys = ["User_id", "Coupon_id", 'Date_received']
    prefixs = 'simple_' + '_'.join(keys) + '_'
    pivot = pd.pivot_table(dfoff, index=keys, values='cnt', aggfunc=lambda x: 1 if len(x) > 1 else 0)
    pivot = pd.DataFrame(pivot).rename(columns={'cnt': prefixs + 'repeat_received'}).reset_index()
    feature = pd.merge(feature, pivot, on=keys, how='left')

    feature.drop(['cnt'], axis=1, inplace=True)
    return feature
