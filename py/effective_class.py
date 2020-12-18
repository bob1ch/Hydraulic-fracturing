import math as m
import pandas as pd
import os
import numpy


data = {}
datafilenate=os.path.join('data.xlsx')
datas=pd.read_excel(datafilenate)

for line in datas:
    if line != str('Q'):
        data[line]=float(datas[line][0])
    else:
        for row in datas[line]:
            data[line] = datas[line]

def Pv(Lc,pn):
    return Lc*pn*9.81*10^(-6) #вертикальное давление горной породы

def Pg(Pvg, n):
    return Pvg*n/(1-n) #Горизонатлное давление горной породы

class Solver():
    def __init__(self, data):
        self.ef = 0
        self.data = data
        self.solv(data)
    def solv(self,data):
        self.data = data
        self.Pvg = self.data['Lc'] * self.data['r'] * 9.81 * 10 ** (-6)  # МПа
        self.Pgg = self.Pvg * (self.data['n'] / (1 - self.data['n']))
        self.P_razr = self.Pvg - self.data['Ppl'] + self.data['sg']
        self.V_liq = self.data['Qs'] / self.data['C']
        self.V_pr = self.data['K'] * m.pi * self.data['d'] ** 2 * self.data['Lc'] / 4  # Объем продавочной жидкости
        self.t = (self.V_liq + self.V_pr) / self.data['Qp']  # продолжительность гидроразрыва в секундах
        self.length = m.sqrt(self.V_liq * self.data['E'] / (5.6 * (1 - self.data['n'] ** 2) * self.data['Lc'] * (self.P_razr - self.Pgg)))
        self.Width = (4 * (1 - self.data['n'] ** 2) * self.length * (self.P_razr - self.Pgg)) / self.data['E']
        self.K1 = self.Width ** 2 / (12 * 12 ** 4)
        self.Kpriz = (self.data['Kp'] * self.data['Lc'] + self.K1 * self.Width) / (self.Width + self.data['Lc'])
        self.Rt = (0.0134 - 1.6 * 0.000001 * self.data['Lc']) * (10 ** 3 * self.data['Q'][0] * m.sqrt(self.data['M'] * self.t / self.Kpriz)) ** (
                    1 / 2)
        self.n_ef = numpy.log10(self.data['Rk'] / self.data['rc']) / numpy.log10(data['Rk'] / self.Rt)
        for i in data['Q']:
            Q = i
            self.Rt_temp = (0.0134 - 1.6 * 0.000001 * data['Lc']) * (10 ** 3 * Q * m.sqrt(data['M'] * self.t / self.Kpriz)) ** (1 / 2)
            self.n_ef_temp = numpy.log10(data['Rk'] / data['rc']) / numpy.log10(data['Rk'] / self.Rt_temp)
            if self.n_ef_temp > self.n_ef:
                self.n_ef = self.n_ef_temp
                self.ef = self.n_ef


f = Solver(data)
r = f.ef
print(r)


