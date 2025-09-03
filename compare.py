import pandas as pd

def compare_data():
    df = pd.read_csv("./resData/2022_환경_통합.csv", encoding='cp949')
    df_filtered = df[['품목', '온도_내부', '상대습도_내부', '일사량_외부']]
    df_filtered_5up = df_filtered[df_filtered['일사량_외부'] >= 5]
    average_temp = df_filtered.groupby('품목')[['온도_내부', '상대습도_내부', '일사량_외부']].mean().reset_index()
    out_data = ['가지', '국화']
    average_temp = average_temp[~average_temp['품목'].isin(out_data)]

    labels = average_temp['품목'].tolist()
    temp = average_temp['온도_내부'].tolist()
    humid = average_temp['상대습도_내부'].tolist()
    solar = average_temp['일사량_외부'].tolist()

    compare_data = {
        "labels" : labels,
        "temp" : temp,
        "humid" : humid,
        "solar" : solar
    }


    return compare_data