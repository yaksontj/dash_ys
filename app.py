import streamlit as st
import pymysql
import datetime
import time
import os
import numpy as np
import math

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
branch_list = df_branch['b_name'].tolist()

st.text('약손명가 대시보드')


# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('매장명')

# select_species 변수에 사용자가 선택한 값이 지정됩니다
select_species = st.sidebar.selectbox(
    '확인하고 싶은 매장을 선택하세요',
    branch_list
)
# 원래 dataframe으로 부터 꽃의 종류가 선택한 종류들만 필터링 되어서 나오게 일시적인 dataframe을 생성합니다
tmp_df = df[df['species']== select_species]
# 선택한 종의 맨 처음 5행을 보여줍니다
st.table(tmp_df.head())



df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

st.write(df)