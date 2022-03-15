import numpy 
from sympy import *

m=symbols('m')
N=symbols('N')
t=symbols('t',positive=True)


print("Adjon meg egy tömeget!\n")
inputweight=input()
print("Adjon meg egy erőt")
inputForce=input()

Ft_function=10*N-(0.5*(t**2))
mt_function=Ft_function/m
mt_function=mt_function.subs({m:inputweight,N:inputForce})
Time=solve(mt_function)[0]#0-ra megoldva az M(t) függvény


print(str(Time)+" másodpercig nő a sebessége\n")#megoldás
print(str(integrate(mt_function,(t,0,Time)))+" m/s a test végsebessége\n")#integráljuk a 0-Time tartományon és megkapjuk a végsebességet
print(str(integrate(integrate(mt_function,t),(t,0,Time)))+" m-re távolodott el, mielőtt elérte a végsebességet\n")#integráljuk M(t) függvényt, majd azt integráljuk a 0-Time tartományon, hogy megkapjuk a távolságot