import matplotlib.pyplot as plt
import pandas as pd

#스칼라 일 때만 적용되는 칼만 필터.
class KF_SCALAR:
    def __init__(self, P = 2, Q = 0.01 , R = 4, X = 80):
        self.p_last = P # 추정값의 정확도에 대한 척도를 나타냄
        self.Q = Q #시스템의 잡음.클수록 변화가 완만함. 과정 노이즈 공분산
        self.R = R #클수록 측정값 영향을 많이 받음. 영향이 큼. 측정 노이즈 공분산
        self.flag = True #처음 값이 들어왔는지 판별하는 변수

    def update(self, data):

        #처음 값이 들어왔을 경우 그 값을 예측 값으로 함.
        if self.flag == True:
            self.x_last = data
            self.flag = False
        x_pred = self.x_last

        # 오차 공분산 예측
        p_pred = self.p_last + self.Q

        #칼만 이득 계산
        k_gain = p_pred / (p_pred + self.R)

        #추정값 계산
        self.x_last = x_pred + k_gain * (data - x_pred)

        #오차 공분산 계산
        self.p_last = (1 - k_gain) * p_pred

        return self.x_last

#ble_data_analysis.py 에서 저장한 파일을 읽음.
result_row = pd.read_csv('RSSI_rows.csv')

#클래스 생성. 초기값은 default로 자동적용.
kf_filter = KF_SCALAR()
x = []

#RSSI_1 값을 하나씩 kf_filter를 적용.
for i in range(len(result_row['RSSI_1'])):
    x.append(kf_filter.update(result_row['RSSI_1'][i]))

#위와 같음. RSSI_2값을 넣음.
kf_filter2 = KF_SCALAR()
y = []
for i in range(len(result_row['RSSI_2'])):
    y.append(kf_filter2.update(result_row['RSSI_2'][i]))

fig, ax = plt.subplots()

#RSSI_1 과 칼만필터를 적용한 RSSI_1를 비교
ax.plot(result_row['RSSI_1'],'r',x,'b')
fig.set_size_inches(40,10)
fig.savefig('RSSI_1.png')
plt.close(fig)

#RSSI_2 과 칼만필터를 적용한 RSSI_2를 비교
fig, ax = plt.subplots()
ax.plot(result_row['RSSI_2'],'r',y,'b') 
fig.set_size_inches(40,10)
fig.savefig('RSSI_2.png')
plt.close(fig)
