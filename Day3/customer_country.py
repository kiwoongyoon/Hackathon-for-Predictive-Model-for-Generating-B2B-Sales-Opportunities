import re
import pycountry # !pip install pycountry


# '고객_유형' 컬럼의 모든 값을 소문자로 변환하고, 기호와 띄어쓰기 제거 ## 숫자도
def preprocess_text_column(df, column_name):
    df[column_name] = df[column_name].str.lower().str.replace(r'[^a-zA-Z]+', '', regex=True)
    

# 국가 이름을 표준화하는 함수
def standardize_country_name(name):
    try:
        # pycountry를 사용하여 국가 객체 찾기
        country = pycountry.countries.lookup(name)
        # 공식 국가명 반환
        return country.name
    except LookupError:
        # 국가를 찾지 못한 경우 입력값 그대로 반환
        return name

##########################################################################################
    

def eda_customer_country(df):
    ## '/'를 기준으로 컬럼을 나누어 'customer_city'와 'customer_country' 컬럼 생성
    df[['customer_city', 'customer_nation']] = df['customer_country'].str.split('/', expand=True).iloc[:, 1:3]

    ## 영어로 번역
    df['customer_city'] = df['customer_city'].apply(standardize_country_name)
    df['customer_nation'] = df['customer_nation'].apply(standardize_country_name)

    ## 띄어쓰기, 기호, 소문자 + 숫자 제거
    preprocess_text_column(df, 'customer_city')
    preprocess_text_column(df, 'customer_nation')

    ## 커스텀 : 터키, us
    df['customer_nation'] = df['customer_nation'].replace({'trkiye': 'turkey'}, regex=True)
    df['customer_nation'] = df['customer_nation'].replace({'.*unitedstates.*': 'unitedstates'}, regex=True)

    ## 기존 customer_country 제거
    df.drop(['customer_country'], axis=1, inplace=True)

    return df