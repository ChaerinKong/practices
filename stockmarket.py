import pandas as pd
from datetime import date
import sys

import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')

sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')  #Unicode Encoding

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드', '지역']]
# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code', '지역': 'region'})
# print(code_df.head())

def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    # print("요청 URL = {}".format(url))
    return url
    # 신라젠의 일자데이터 url 가져오기

item_names = ['SK텔레콤', 'LG디스플레이', '네오위즈', '넥센타이어']
df = pd.DataFrame()
for item_name in item_names:
    for page in range(1, 6):
        url = get_url(item_name, code_df) # 일자 데이터를 담을 df라는 DataFrame 정의
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

# 1페이지에서 20페이지의 데이터만 가져오기
names = [item_names[0]]*50 + [item_names[1]]*50 + [item_names[2]]*50 + [item_names[3]]*50
# df.dropna()를 이용해 결측값 있는 행 제거

df = df.dropna().reset_index(drop=True)
# print(df.head())
df['회사명'] = names
df['전일비'] = df['종가'] - df.shift(-1)['종가']
temp = list()
for ind, val in df.iterrows():
    if (ind+1) % 50 == 0:
        temp.append('-')
    else:
        temp.append(val['전일비'])
df['전일비'] = temp
df.to_csv('../{date}.csv'.format(date=date.today().strftime('%Y_%m_%d')), encoding='euc-kr', index=False)
# print(df.iloc[48:52])
# 출처: https://excelsior-cjh.tistory.com/109 [EXCELSIOR]
df = df.rename(columns={'회사명': 'name', '종가': 'end_price'})
print('-'*70)
print("{date}의 일간 주식 리포트".format(date=date.today()))
print('-'*70)
print()
for i in range(len(item_names)):
    print("{num}. {item}".format(num=i+1, item=item_names[i]))
    print()
    print("{item}의 오늘 등락율은 {rate:.3f}%({amount}원)".format(
                            item=item_names[i],
                            rate=(100*(df[df['name']==item_names[i]].iloc[0]['end_price']-df[df['name']==item_names[i]].iloc[1]['end_price'])/df[df['name']==item_names[i]].iloc[1]['end_price']),
                            amount=(df[df['name']==item_names[i]].iloc[0]['end_price']-df[df['name']==item_names[i]].iloc[1]['end_price'])))
    print("{item}의 1주일 등락율은 {rate:.3f}%({amount}원)".format(
                            item=item_names[i],
                            rate=(100*(df[df['name']==item_names[i]].iloc[0]['end_price']-df[df['name']==item_names[i]].iloc[6]['end_price'])/df[df['name']==item_names[i]].iloc[6]['end_price']),
                            amount=(df[df['name']==item_names[i]].iloc[0]['end_price']-df[df['name']==item_names[i]].iloc[6]['end_price'])))
    print()
    if (100*(df[df['name']==item_names[i]].iloc[0]['end_price']-df[df['name']==item_names[i]].iloc[6]['end_price'])/df[df['name']==item_names[i]].iloc[6]['end_price']) > 1:
        print("상승세가 눈에 띄네요~!")
    elif (100*(df[df['name']==item_names[i]].iloc[0]['end_price']-df[df['name']==item_names[i]].iloc[6]['end_price'])/df[df['name']==item_names[i]].iloc[6]['end_price']) < -3:
        print("걱정스러운 하락세입니다..ㅠㅠ")
    else:
        print("평탄한 한 주였어요.")
    print()
