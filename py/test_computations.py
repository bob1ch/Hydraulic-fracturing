#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:37:28 2021

@author: geolog
"""

import numpy as np
from scipy.optimize import fsolve
from sympy.solvers import solve
from sympy import Symbol
import math

data={'Lc':2467,'ro':2600,'d':0.076,'n':0.3,'C_p':300,'h':14.3,'ro_p':3000,\
                      'mu_g':0.285,'ro_g':950, 'Q_p': 7500, 'Pr':29.8, 'Qr':0.022,\
                      'sigma_pl':1.5};
          
          
Lc = data['Lc']#Глубина
ro =data['ro']# плотность пород
d = data['d'] #диаметр
n = data['n'] #Пуассона
C_p = data['C_p'] # Объемная концентрация проппанта кг/м3
ro_p = data['ro_p']   # плотность пропанта кг/м3
mu_g = data['mu_g']  # Па*с вяз-ть жидкости
ro_g =  data['ro_g'] # кг/м3 плотность жидкости
h = data['h'] #разбуренный интервал пласта
Qr = data['Qr'] # Подача при рабочем давлении
Pr = data['Pr'] #Рабочее давление
Q_p = data['Q_p']  # Объем пропанта в тоннах?
K = 0.8 # Кэффициент рабочего состания
N = 1 #Число резервных агентов
E=10**10 #модуль упругости, МПа
Q=0.035; #м3/сек
sigma_pl=data['sigma_pl'];


Pvg = Lc * ro * 9.81 * 10 ** (-6)  # МПа Расчет вертикальной составляющей горного давления Lc глубина r(ро) плотность пород кг/м3 = 2600
Pgg = Pvg * (n / (1 - n))  # МПа Расчет горизонтального горного давления Pvg ветикальная составляющая n коэф Пуассона = 0,2, 0,3
P_pl=(data['Lc']*1000*9.81)/10**6; #В.Г. Крец, А.В. Шадрина Основы НГД Практикум 2012 https://portal.tpu.ru/SHARED/k/KR_NAS_SH/Ycheb_metod/Tab2/Tab/МУ_ОНГПД(ИМО).docx


#P_razr = Symbol('P_razr')
#P_razr = solve((P_razr ) / (Pgg ) * ((P_razr/ Pgg) - 1) ** 3 - (5.25 * (1 / ((1 - n) ** 2)) * ((E / (Pgg )) ** 2) * ((Q * (mu_g)) / (Pgg* 10**6 ) )), P_razr)[1]
#print(P_razr)
P_razr = Pvg - P_pl + sigma_pl;  #Юрчук, Истомин Расчеты в добыче 1989


bet = C_p / ro_p / (C_p / ro_p + 1)  # Объемная концентрация проппанта 360 кг/м3 - плотность пропанта 3000 кг/м3
ro_pg = ro_g * (1 - bet) + ro_p * bet  # кг/м3 плотность жидкости с проппантом
mu_pg = mu_g * 2.7 ** (3.18 * bet)  # Па*с вяз-ть жидкости с проппантом
print(bet)
print(ro_pg)
print(mu_pg)

Re = 4 * 0.035 * ro_pg / 3.14 / d / mu_pg

if Re<2320:
    limbda = 64/Re
    print(limbda)
else:
    limbda = 0.3164/Re**0.25
    print(limbda)
    
Ptr = 8 * limbda * Lc * ro_pg * 0.0000087 ** 2 / (3.14 ** 2 * d ** 5)  # Потери на трение
print(Ptr)

Pu = P_razr - ro_pg * Lc * 9.81 * 10 ** (-6) + Ptr
# Pu = 17.47
print(Pu)

n_a = round(Pu * 0.15 / (Pr * Qr * K) + N, 1)  # Число агрегатов
print(n_a)
V_pg = 0.785 * d ** 2 * Lc  # Объем продавочной жидкости

V_g = Q_p / C_p  # Объем жидкости для осуществления ГРП

t = (V_g + V_pg) / Qr / 60  # продолжительность гидроразрыва в секундах

# h = 14.3 #Вскрытая часть пласта?

length = math.sqrt(V_g * 10 ** 4 / (5.6 * (1 - n ** 2) * h * (P_razr - Pgg)))# м
Width = (4 * (1 - n ** 2) * length * (P_razr - Pgg)) / 10 # см

output_dictionary={'n_a':n_a,'V_pg':V_pg,'V_g':V_g,'t':t,'length':length,'Width':Width} 

for key in [*output_dictionary]:
    print('%s =%s '%(key,output_dictionary[key])); 
    
"""
n_a =1.8 - Fail
V_pg =11.18577272  - Ok
V_g =25.0 - Ok
t =27.413464181818185 - Ok
length =58.28219257716556 - Ok
Width =21.4259483648956 - Fail
"""    
    