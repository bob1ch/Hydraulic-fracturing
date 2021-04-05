# -*- coding: utf-8 -*-
import math as m
import pandas as pd
import os
import numpy
from sympy.solvers import solve
from sympy import Symbol
import copy
import math

class Engine():
    def __init__(self):
        print('the Engine has been initialized');
        self.data = {}
    def compute2(self,params):
        print('Engine has been activated')
        print(params);
        
        for key in [*params]: #параметр "глубина" (Depth), не зная точное имя поля
            if 'depth' in key.lower():
                print('Значение глубины хранится в параметре с ключом: '+key);
        
        
    def compute(self, my_data):
        self.data = copy.copy(my_data);
        Lc = self.data['Lc']#Глубина
        ro =self.data['ro']# плотность пород
        d = self.data['d'] #диаметр
        n = self.data['n'] #Пуассона
        C_p = self.data['C_p'] # Объемная концентрация проппанта кг/м3
        ro_p = self.data['ro_p']   # плотность пропанта кг/м3
        mu_g = self.data['mu_g']  # Па*с вяз-ть жидкости
        ro_g =  self.data['ro_g'] # кг/м3 плотность жидкости
        h = self.data['h'] #разбуренный интервал пласта
        Qr = self.data['Qr'] # Подача при рабочем давлении
        Pr = self.data['Pr'] #Рабочее давление
        Q_p = self.data['Q_p']  # Объем пропанта в тоннах?
        K = 0.8 # Кэффициент рабочего состания
        N = 1 #Число резервных агентов
        E=10**4#модуль упругости, МПа
        #Q=0.035; #м3/сек
        sigma_pl=self.data['sigma_pl'];
        
        
        Pvg = Lc * ro * 9.81 * 10 ** (-6)  # МПа Расчет вертикальной составляющей горного давления Lc глубина r(ро) плотность пород кг/м3 = 2600
        Pgg = Pvg * (n / (1 - n))  # МПа Расчет горизонтального горного давления Pvg ветикальная составляющая n коэф Пуассона = 0,2, 0,3
        P_pl=(self.data['Lc']*1000*9.81)/10**6; #В.Г. Крец, А.В. Шадрина Основы НГД Практикум 2012 https://portal.tpu.ru/SHARED/k/KR_NAS_SH/Ycheb_metod/Tab2/Tab/МУ_ОНГПД(ИМО).docx
        
        
        #P_razr = Symbol('P_razr')
        #P_razr = solve((P_razr ) / (Pgg ) * ((P_razr/ Pgg) - 1) ** 3 - (5.25 * (1 / ((1 - n) ** 2)) * ((E / (Pgg )) ** 2) * ((Q * (mu_g)) / (Pgg* 10**6 ) )), P_razr)[1]
        #print(P_razr)
        P_razr = Pvg - P_pl + sigma_pl;  #Юрчук, Истомин Расчеты в добыче 1989
        
        
        bet = C_p / ro_p / (C_p / ro_p + 1)  # Объемная концентрация проппанта 360 кг/м3 - плотность пропанта 3000 кг/м3
        ro_pg = ro_g * (1 - bet) + ro_p * bet  # кг/м3 плотность жидкости с проппантом
        mu_pg = mu_g * 2.7 ** (3.18 * bet)  # Па*с вяз-ть жидкости с проппантом
        
        
        Re = 4 * 0.035 * ro_pg / 3.14 / d / mu_pg
        
        if Re<2320:
            limbda = 64/Re
        #    print(limbda)
        else:
            limbda = 0.3164/Re**0.25
        #    print(limbda)
            
        Ptr = 8 * limbda * Lc * ro_pg * 0.0000087 ** 2 / (3.14 ** 2 * d ** 5)  # Потери на трение
        #print(Ptr)
        
        Pu = P_razr - ro_pg * Lc * 9.81 * 10 ** (-6) + Ptr
        # Pu = 17.47
        #print(Pu)
        
        n_a = m.ceil(Pu * 0.15 / (Pr * Qr * K) + N)  # Число агрегатов
        #print(n_a)
        V_pg = round(0.785 * d ** 2 * Lc,2)  # Объем продавочной жидкости
        
        V_g = round(Q_p / C_p,2)  # Объем жидкости для осуществления ГРП
        
        t = round((V_g + V_pg) / Qr / 60,2)  # продолжительность гидроразрыва в секундах
        
        # h = 14.3 #Вскрытая часть пласта?
        
        length = round(math.sqrt(V_g * E / (5.6 * (1 - n ** 2) * h * (P_razr - Pgg))), 2)# м
        
        #уточнить формулу расчета ширины трещины и ее размерность
        Width = round((4 * (1 - n ** 2) * length * (P_razr - Pgg))/ E * 100, 2)  # см
        #
        
        output_dictionary={'n_a':n_a,'V_pg':V_pg,'V_g':V_g,'t':t,'length':length,'Width':Width} 

        return output_dictionary;

