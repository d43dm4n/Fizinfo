from datetime import datetime
import numpy 
import pandas 

import matplotlib.pyplot

inputFile="./vezetes-1.txt"
inputFile2="./vezetes-2.txt"

dataStream=pandas.read_csv(inputFile,sep=",")
dataStream2=pandas.read_csv(inputFile2,sep=",")

dataStream["Time"]=pandas.to_datetime(dataStream["date time"],format="%Y-%m-%d %H:%M:%S")
dataStream["speed"]=dataStream["speed(m/s)"]
dataStream2["Time"]=pandas.to_datetime(dataStream2["date time"],format="%Y-%m-%d %H:%M:%S")
dataStream2["speed"]=dataStream2["speed(m/s)"]

TimeArray=dataStream.Time.to_numpy()
TimeArray2=dataStream2.Time.to_numpy()
ProcessedTimeArray=(TimeArray-TimeArray[0])/numpy.timedelta64(1,"s")
ProcessedTimeArray2=(TimeArray2-TimeArray2[0])/numpy.timedelta64(1,"s")

timeOfLawBreaking=0
timeOfLawBreaking2=0
timeOfLawBreaking3=0
timeOfLawBreaking4=0
v_max=13.8888889
delta_t=ProcessedTimeArray[-1]-ProcessedTimeArray[0]
delta_t2=ProcessedTimeArray2[-1]-ProcessedTimeArray2[0]

R_F=6378000.0 # a Föld sugara m-ben

long_arr=numpy.radians(dataStream.longitude).to_numpy()  
lat_arr=numpy.radians(dataStream.latitude).to_numpy()    
long_arr2=numpy.radians(dataStream2.longitude).to_numpy()  
lat_arr2=numpy.radians(dataStream2.latitude).to_numpy() 

x_arr=(long_arr-long_arr[0])*numpy.cos(lat_arr[0])*R_F
y_arr=(lat_arr-lat_arr[0])*R_F
x_arr2=(long_arr2-long_arr2[0])*numpy.cos(lat_arr[0])*R_F
y_arr2=(lat_arr2-lat_arr2[0])*R_F



def deriv(xx_tab, ff_tab): 
    dff_dxx=numpy.zeros(xx_tab.shape, numpy.float64)
    dff_dxx[0]=(ff_tab[1]-ff_tab[0])/(xx_tab[1]-xx_tab[0]) 
    dff_dxx[-1]=(ff_tab[-1]-ff_tab[-2])/(xx_tab[-1]-xx_tab[-2]) 
    dff_dxx[1:-1]=(ff_tab[2:]-ff_tab[0:-2])/(xx_tab[2:]-xx_tab[0:-2]) 
    return(dff_dxx)


vx_arr=deriv(ProcessedTimeArray, x_arr)
vy_arr=deriv(ProcessedTimeArray, y_arr)
vx_arr2=deriv(ProcessedTimeArray2, x_arr2)
vy_arr2=deriv(ProcessedTimeArray2, y_arr2)

vabs_arr=(vx_arr2**2+vy_arr2**2)**0.5#egyik file
vabs_arr2=(vx_arr2**2+vy_arr2**2)**0.5#másik file

delta_t_with_speed_limited=delta_t
delta_t_with_speed_limited2=delta_t2
delta_t_with_speed_limited3=delta_t
delta_t_with_speed_limited4=delta_t2

for Time in range(len(ProcessedTimeArray)) :
    if dataStream.speed[Time]>v_max:
        timeOfLawBreaking+=1
        delta_t_with_speed_limited+=(1*(dataStream.speed[Time]/v_max))-1


for Time in range(len(ProcessedTimeArray)) :
    if vabs_arr[Time]>v_max:
        timeOfLawBreaking3+=1
        delta_t_with_speed_limited3+=(1*(vabs_arr[Time]/v_max))-1


for Time in range(len(ProcessedTimeArray2)) :
    if dataStream2.speed[Time]>v_max:
        timeOfLawBreaking2+=1
        delta_t_with_speed_limited3+=(1*(dataStream2.speed[Time]/v_max))-1

for Time in range(len(ProcessedTimeArray2)) :
    if vabs_arr2[Time]>v_max:
        timeOfLawBreaking4+=1
        delta_t_with_speed_limited4+=(1*(vabs_arr2[Time]/v_max))-1


print(str(delta_t)+" s vezetésből "+str(timeOfLawBreaking)+" s-ig történt gyorshajtás a "+str(inputFile)+" log alapján")
print(str(delta_t)+" s vezetésből "+str(timeOfLawBreaking3)+" s-ig történt gyorshajtás a "+str(inputFile)+" log alapján(számolt értékkel)\n")

print(str(delta_t2)+" s vezetésből "+str(timeOfLawBreaking2)+" s-ig történt gyorshajtás a "+str(inputFile2)+" log alapján")
print(str(delta_t)+" s vezetésből "+str(timeOfLawBreaking4)+" s-ig történt gyorshajtás a "+str(inputFile2)+" log alapján(számolt értékkel)\n")

print(str(delta_t_with_speed_limited)+" s ideig tartana az út, ha a sebességhatárt betartanánk a "+str(inputFile)+" log esetén")
print(str(delta_t_with_speed_limited3)+" s ideig tartana az út, ha a sebességhatárt betartanánk a "+str(inputFile)+" log esetén(számolt értékkel)\n")

print(str(delta_t_with_speed_limited2)+" s ideig tartana az út, ha a sebességhatárt betartanánk  "+str(inputFile2)+" log esetén")
print(str(delta_t_with_speed_limited4)+" s ideig tartana az út, ha a sebességhatárt betartanánk a "+str(inputFile2)+" log esetén(számolt értékkel)")
