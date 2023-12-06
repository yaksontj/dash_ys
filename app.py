import streamlit as st
import pymysql
import datetime
import pandas as pd

# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('branch1')


conn_yakson = pymysql.connect(host = '139.150.65.14', user = 'yaksonbon', password= 'yakson!@#bon)(*', db='yakson', charset='utf8',
                      cursorclass=pymysql.cursors.DictCursor)
cur_yakson = conn_yakson.cursor()

sql_rs = '''
SELECT *
FROM ReportSales
'''

@st.cache_data
def load_data(sql):
    cur_yakson.execute(sql)
    results = cur_yakson.fetchall()
    df = pd.DataFrame(results)
    return df

df_rs = load_data(sql_rs)
df_rs['ym'] = df_rs['sr_date'].dt.strftime('%Y-%m')

sql_b='''
SELECT *
FROM Branch
'''
df_branch = load_data(sql_b)
df_branch = df_branch[df_branch['b_status']=='Y'][['b_name','b_idx']]


month_dict = {}
now = datetime.date.today()
for i in range(0, 12):
    a = now.month

    if a + i > 12:
        if a+i-12 >= 10:
            month_dict[str(a + i - 12)+'월']= str(a + i - 12)
        else:
            month_dict[str(a + i - 12)+'월']= '0' + str(a + i - 12)
    else:
        if a+i >= 10:
            month_dict[str(a + i)+'월']= str(a + i)
        else:
            month_dict[str(a + i)+'월']= '0' + str(a + i)

select_year = st.sidebar.selectbox(
    '확인하고 싶은 년도를 선택하세요', ['2023']
)

select_month = st.sidebar.selectbox(
    '확인하고 싶은 월을 선택하세요', list(month_dict.keys())
)

branch_dict = df_branch['b_name'].to_dict()

# select_species 변수에 사용자가 선택한 값이 지정됩니다
select_branch = st.sidebar.selectbox(
    '확인하고 싶은 매장명을 선택하세요', ['전체']+list(branch_dict.values())
)


df_rs_month = df_rs[df_rs['ym'].between(str(select_year)+'-'+str(month_dict[select_month]), str(select_year)+'-'+str(month_dict[select_month]))]


df_rs_month.loc[df_rs_month[df_rs_month['use_flat'] > 0].index, 'payment_price'] = 0
df_static = df_rs_month[['b_idx','payment_price']].groupby('b_idx').sum()
df_static['payment_price'] = df_static['payment_price'].astype('int')

df_static = pd.merge(df_branch, df_static, how = 'left', on ='b_idx')


# 원래 dataframe으로 부터 꽃의 종류가 선택한 종류들만 필터링 되어서 나오게 일시적인 dataframe을 생성합니다
if select_branch == '전체':
    tmp_df = df_static[df_static['payment_price']>0][['b_name','payment_price']].sort_values('payment_price',ascending=False)
    st.table(tmp_df)
else:
    tmp_df = df_static[df_static['b_name']== select_branch][['b_name','payment_price']].sort_values('payment_price',ascending=False)
    # 선택한 종의 맨 처음 5행을 보여줍니다
    st.table(tmp_df)