import streamlit as st
import pymysql
import datetime
import time
import os
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt


conn_yakson = pymysql.connect(host = '139.150.65.14', user = 'yaksonbon', password= 'yakson!@#bon)(*', db='yakson', charset='utf8',
                      cursorclass=pymysql.cursors.DictCursor)
cur_yakson = conn_yakson.cursor()


sql_rs = '''
SELECT *
FROM ReportSales
'''
cur_yakson.execute(sql_rs)
results = cur_yakson.fetchall()
df_rs = pd.DataFrame(results)

sql_b='''
SELECT *
FROM Branch
'''
cur_yakson.execute(sql_b)
results = cur_yakson.fetchall()
df_branch = pd.DataFrame(results)

df_branch = df_branch[df_branch['b_status']=='Y'][['b_name','b_idx']]
branch_dict = df_branch['b_name'].to_dict()

df_rs.loc[df_rs[df_rs['use_flat'] > 0].index, 'payment_price'] = 0
df_static = df_rs[['b_idx','payment_price']].groupby('b_idx').sum()

df_static = pd.merge(df_branch, df_static, how = 'left', on ='b_idx')

# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('branch')

# select_species 변수에 사용자가 선택한 값이 지정됩니다
select_branch = st.sidebar.selectbox(
    '확인하고 싶은 매장명을 선택하세요', branch_list
)

# 원래 dataframe으로 부터 꽃의 종류가 선택한 종류들만 필터링 되어서 나오게 일시적인 dataframe을 생성합니다
if select_branch == '전체':
    tmp_df = df_static[df_static['payment_price']>0]
    st.table(tmp_df.head())
else:
    tmp_df = df_static[df_static['b_name']== select_branch]
    # 선택한 종의 맨 처음 5행을 보여줍니다
    st.table(tmp_df.head())