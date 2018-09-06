import pandas as pd
import ast
import matplotlib.pyplot as plt


#dic 형태로 저장된. txt 파일을 읽어옴.
r = open("BLEdict.txt", mode='r')

df_result = pd.DataFrame()#결과를 담을 DataFrame 생성
time_list = [] #시간 정보를 담을 리스트 생성(미사용)

# 파일 읽기
for i, line in enumerate(r):
    try:
        dic_line = ast.literal_eval(line.strip('\n'))#문자열을 dic로 변환
        df_line = pd.DataFrame([dic_line],[i-1])#DataFrame 형식으로 변경
        df_result = pd.concat([df_result,df_line],axis=0)#axis = 0, 한 행씩 추가.
    except:#시간 추출. 오류로 간주. (미사용)
        time_stamp = line.rstrip("\n").rstrip("-")
        time_list.append(time_stamp)
        continue

#파일 닫기
r.close()

#colum RSSI 값을 숫자로 변환
#미실행시 plot 실행시 문자로 인식함.
df_result['RSSI'] = df_result['RSSI'].convert_objects(convert_numeric=True)

#각 MAC 주소별로 RSSI 값을 분석할 예정
#중복되는 맥주소 제거.
MAC_only = df_result.MAC.drop_duplicates(keep = 'first')

#MAC_only에서 기존 index를 reset 시킴.
MAC_only = MAC_only.reset_index().drop("index",axis = 1)

#df_result에서 내가 정한 MAC 행을 추출
MAC_row_1 = df_result.loc[df_result["MAC"] == MAC_only.MAC[0]]
MAC_row_2 = df_result.loc[df_result["MAC"] == MAC_only.MAC[1]]

#100개의 RSSI 열 데이터만 추출
row1 = MAC_row_1.get("RSSI")[0:100]
row2 = MAC_row_2.get("RSSI")[0:100]

#추출된 RSSI 열 index를 초기화 및 기존의 index 열 삭제
new_row1 = row1.reset_index().drop("index",axis = 1)
new_row2 = row2.reset_index().drop("index",axis = 1)


#subplots 를 생성
fig, ax = plt.subplots()

# X값: 추출한 RSSI 의 개수(100개) / Y값: RSSI 실제 측정 값
ax.plot(range(len(new_row1.RSSI)),new_row1.RSSI,'r'
        ,range(len(new_row2.RSSI)),new_row2.RSSI,'k')

#크기 정하기. 파일 저장.
fig.set_size_inches(40,10)
fig.savefig('RSSI_rows.png')
plt.close(fig)

#데이터 합치기
result_row = pd.DataFrame()
result_row = pd.concat([result_row,new_row1],axis=1)
result_row = pd.concat([result_row,new_row2],axis=1)

#컬럼 이름 변경하기
result_row.columns.values[0] = 'RSSI_1'
result_row.columns.values[1] = 'RSSI_2'

#csv 파일로 저장.
result_row.to_csv("RSSI_rows.csv", mode='w')

#각 row 별로 개수를 센다음. index 를 정렬하고 바 형태로 만들 수도 있음.
#분포를 보기 위해서.
a = result_row['RSSI_1'].value_counts().sort_index().plot.bar()
result_row['RSSI_2'].value_counts().sort_index().plot.bar()

#데이터 간단히 분석해주는 메소드
result_row.describe()
