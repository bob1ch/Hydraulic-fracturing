# -*- coding: utf-8 -*-
import math as m
import pandas as pd
import os
import numpy
from sympy.solvers import solve
from sympy import Symbol

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
        self.data = my_data
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

        Pvg = Lc * ro * 9.81 * 10 ** (
            -6)  # МПа Расчет вертикальной составляющей горного давления Lc глубина r(ро) плотность пород кг/м3 = 2600
        Pgg = Pvg * (n / (
                    1 - n))  # МПа Расчет горизонтального горного давления Pvg ветикальная составляющая n коэф Пуассона = 0,2, 0,3

        import numpy as np
        from scipy.optimize import fsolve

        P_razr = Symbol('P_razr')
        P_razr = solve(P_razr / Pgg * (P_razr / Pgg - 1) ** 3 - (
                    5.25 * 1 / (1 - n) ** 2 * (10 ** 4 / Pgg) ** 2 * 0.0035 * mu_g / Pgg / 10 ** 6), P_razr)[1]
        print(P_razr)

        bet = C_p / ro_p / (C_p / ro_p + 1)  # Объемная концентрация проппанта 360 кг/м3 - плотность пропанта 3000 кг/м3
        ro_pg = ro_g * (1 - bet) + ro_p * bet  # кг/м3 плотность жидкости с проппантом
        mu_pg = mu_g * 2.7 ** (3.18 * bet)  # Па*с вяз-ть жидкости с проппантом
        print(bet)
        print(ro_pg)
        print(mu_pg)

        Re = 4 * 0.035 * ro_pg / 3.14 / d / mu_pg

        limbda = 0.039
        print(limbda)

        Ptr = 8 * limbda * Lc * ro_pg * 0.0000087 ** 2 / (3.14 ** 2 * d ** 5)  # Потери на трение
        print(Ptr)

        Pu = P_razr - ro_pg * Lc * 9.81 * 10 ** (-6) + Ptr
        # Pu = 17.47
        print(Pu)

        n_a = Pu * 0.15 / (Pr * Qr * K) + N  # Число агрегатов
        print(n_a)
        V_pg = 0.785 * d ** 2 * Lc  # Объем продавочной жидкости

        V_g = Q_p / C_p  # Объем жидкости для осуществления ГРП

        t = (V_g + V_pg) / Qr / 60  # продолжительность гидроразрыва в секундах

        # h = 14.3 #Вскрытая часть пласта?

        length = m.sqrt(V_g * 10 ** 4 / (5.6 * (1 - n ** 2) * h * (P_razr - Pgg)))# м
        Width = (4 * (1 - n ** 2) * length * (P_razr - Pgg)) / 10 # см

        output_dictionary={'n_a':n_a,'V_pg':V_pg,'V_g':V_g,'t':t,'length':length,'Width':Width}
        
        return output_dictionary;

