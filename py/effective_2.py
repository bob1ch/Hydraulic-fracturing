import math as m
import pandas as pd
import os
'''
data = {}
datafilenate=os.path.join('data.xlsx')
datas=pd.read_excel(datafilenate)
for line in datas:
    key = line
    for row in datas[line]:
        value = row
        data[key] = row
print(data['Lc',0])
'''        
def Pv(Lc,pn):
    return Lc*pn*9.81*10^(-6) #вертикальное давление горной породы

def Pg(Pvg, n):
    return Pvg*n/(1-n) #Горизонатлное давление горной породы

    
#Описание переменных(Сделать нормальны ввод данных)
Lc = data['Lc'][0]
h = data['h'][0]
d = data['d'][0]
r = data['r'][0] #плотность
n =data['n'][0]#Коэф Пуассона горных пород (0.2-0.3)
M = data['M'][0] # вязкость
Qs = data['Qs'][0] #кол-во песка
Q = data['Q'][0] #темп закачки
rp = data['rp'][0]#плотность породы
Ppl = data['Ppl'][0]#Давление пласта
sg = data['sg'][0]#МПа предел прочности(сигма)
C=data['C'][0] #Концентрация песка в 1м3(должно расчитываться)
K = data['K'][0]#Взял среднее, надо разобраться что это такое
Qp = data['Qp'][0] #секундный расход закачиваемой жидкости для конкретного агрегата
E = data['E'][0]
Kp = data['Kp'][0]
Rk = data['Rk'][0]
rc = data['rc'][0]

Pvg = Lc*r*9.81*10**(-6) #МПа
Pgg = Pvg*n/(1-n)
P_razr = Pvg + Ppl + sg
V_liq = Qs/C
V_pr = K*m.pi*d**2 *Lc/4 #Объем продавочной жидкости
t = (V_liq+V_pr)/Qp # продолжительность гидроразрыва в секундах
length= m.sqrt(V_liq*E/(5.6*(1-n**2)*Lc*(P_razr-Pgg)))
Width = (4*(1-n**2)*length*(P_razr-Pgg))/E
K1 = Width**2/(12*12**4)
Kpriz = (Kp*Lc+K1*Width)/(Width+Lc)
Rt = (0.0134-1.6*0.000001*Lc)*(10**3*Q*m.sqrt(M*t/Kpriz))**(1/2)
for i in range(len(data['Q'])):
    Q=data['Q'][i]
    Rt_temp = (0.0134-1.6*0.000001*Lc)*(10**3*Q*m.sqrt(M*t/Kpriz))**(1/2)
    if Rt_temp > Rt:
        Rt=Rt_temp
n_ef = m.log10(Rk/rc)/m.log10(Rk/Rt) #расчёт эффективности

print('ok')

df = pd.DataFrame({'effective': [n_ef]})
writer = pd.ExcelWriter('result.xlsx')
df.to_excel(writer,'result', index=False)
writer.save()
os.startfile('result.xlsx')
