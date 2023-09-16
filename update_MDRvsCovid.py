# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 22:53:50 2023

@author: Hannielle
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd



# reading and filter covid data by only selecting state and death rate columns
df_covid=pd.read_csv("US_covid19_cases_and_deaths_by_state.csv") #error_bad_lines=False)
#print(df)
new_df_covid=df_covid[["State","Death Rate per 100000"]]                           # select only states and death rate from the data frame

# adding new column to define rate as high & low rate in the covid data
# these rate were gathered from the CDC website        
covid_conditions=[(new_df_covid["Death Rate per 100000"]>=77.5) & (new_df_covid["Death Rate per 100000"] <93.9),
            (new_df_covid["Death Rate per 100000"]>93.9),
            (new_df_covid["Death Rate per 100000"]<77.7)]
Cvalues=["high_rate", "very High rate", "low Rate"]
new_df_covid["rate_meaning"]=np.select(covid_conditions, Cvalues)
Covidhigh_rateState=new_df_covid[~new_df_covid["rate_meaning"].isin(["low Rate","0"])]
#print(Covidhigh_rateState)

                                                            

# read bacteria resistant data 
#1) Multidrug resistant ecoli
read_ecoli_file=pd.read_csv("Multidrug_resist_ecoli.csv")
# 2) Mdr_ pseudomonas
read_pseudomonas=pd.read_csv("Mdr_pseudomonas.csv")
#3) reading  MDR acinetobaccter file
read_acinetobacter=pd.read_csv("Mdr_acinetobacter.csv")
#4) reading MRD klebsiella file
read_klebsiella=pd.read_csv("Mdr_klebsiella.csv")
#5) reading vancomycin file
read_vancomycin=pd.read_csv("vancomycin_MRSA.csv")
#6) reading fluoroquinoe file
read_fluoroquinolone=pd.read_csv("Fluoroquinolone_MRSA.csv")

#Filter in  state and percent resistant columns for each MRD 
def multidrugRes_antibiotics(file_name):
    new_data=file_name[["State", "Percent Resistant"]]
    return new_data

# parse the multidrugRes_antibiotics function to each MDR data frame

pseudomonas_df=multidrugRes_antibiotics(read_pseudomonas)
acinetobacter_df=multidrugRes_antibiotics(read_acinetobacter)
klebsiella_df=multidrugRes_antibiotics(read_klebsiella)
vancomycin_df=multidrugRes_antibiotics(read_vancomycin)
fluoroquinolone_df=multidrugRes_antibiotics(read_fluoroquinolone)
ecoli_df=multidrugRes_antibiotics(read_ecoli_file)
print(ecoli_df)



# write a function that add a column to define  high and low resistant rate for each MDR pathogen
def defineconditions(percent_rate,rate_cutoff,highest_rate):
    conditions=[(percent_rate["Percent Resistant"]>=rate_cutoff) & (percent_rate["Percent Resistant"] <highest_rate),
            (percent_rate["Percent Resistant"]>highest_rate),
            (percent_rate["Percent Resistant"]<rate_cutoff)]
    values=["high_rate", "very High rate", "low Rate"]
    percent_rate["rate_meaning"]=np.select(conditions, values)
    high_rateState=percent_rate[~percent_rate["rate_meaning"].isin(["low Rate","0"])]
    return(high_rateState)


# parse the function for each MDR pathogen
# The cut off rate define by the CDC that is consired high and low for each pathogen

ecoli_rateCutoff=defineconditions(ecoli_df,12.9,19)                            # ecoli MDR
pseudomonas_rateCutoff=defineconditions(pseudomonas_df,24.4,37)
acinotobacter_rateCutoff=defineconditions(acinetobacter_df,61.5,75)
klebsiella_rateCutoff=defineconditions(klebsiella_df,28.8,52.5)
vancomysin_rateCutoff=defineconditions(vancomycin_df,2.9,4)
fluoroquinolone_rateCutoff=defineconditions(fluoroquinolone_df,82.6,89)



# find the state that are in ecoli dataframe with high rate  that  in the covid data frame with high rate

commonState=Covidhigh_rateState["State"].isin(ecoli_rateCutoff["State"])==True 
#print(commonState=="True")

high_covid=Covidhigh_rateState[commonState]       # this give the states and the data of high death rate
common_states=ecoli_rateCutoff["State"].isin(Covidhigh_rateState["State"])==True


highecoli=ecoli_rateCutoff[common_states]                         # this give state with high MDR ecoli percent rate

# write a function that select state with high MDR and high covid death rate

def final_ouput(covid_cutoff, mdrcutoff):
    high_covid=covid_cutoff["State"].isin(mdrcutoff["State"])==True 
    high_result=covid_cutoff[high_covid]
    B=mdrcutoff["State"].isin(covid_cutoff["State"])==True
    B_result=mdrcutoff[B]
    if len(high_result)>0: #

        print("This multi drug resistant might have an effect on Covid-19 death rate in these state:", "Covid-19 Death Rate")
        print( high_result, "\n")
        print(" Multi Drug Resistant Rate")
        print(B_result,"\n")
    if len(high_result)<1:
        print(" there is no state with  high death rate in this multidrug resistant \n")
    


  
print(" Comparing covid-19 death rate with multi drug resistant ecoli percent resistant rate by state")
print(final_ouput(Covidhigh_rateState, ecoli_rateCutoff))


print(" Comparing covid-19 death rate with multi drug resistant pseudomonas percent resistant rate by state" )
print(final_ouput(Covidhigh_rateState, pseudomonas_rateCutoff))


print(" Comparing covid-19 death rate with multi drug resistant acinotobacter percent resistant rate by state")
print(final_ouput(Covidhigh_rateState, acinotobacter_rateCutoff))


print(" Comparing covid-19 death rate with multi drug resistant klebsiella percent resistant rate by state")
print(final_ouput(Covidhigh_rateState, klebsiella_rateCutoff))


print(" Comparing covid-19 death rate with multi drug resistant vancomysin percent resistant rate by state")
print(final_ouput(Covidhigh_rateState, vancomysin_rateCutoff))


print(" Comparing covid-19 death rate with multi drug resistant fluoroquinolone percent resistant rate by state")
    
print(final_ouput(Covidhigh_rateState, fluoroquinolone_rateCutoff))



## creating a map plot for covid data and MDR
# read bacteria resistant data 
#1) Multidrug resistant ecoli
#read_ecoli_file=pd.read_csv("Multidrug_resist_ecoli.csv")                              # reading the file
#print(read_ecoli_file)
## Reading file that containg Us Map
shape_path ="/Users/hanni/Downloads/data analytics-20230820T214729Z-001/data analytics/cb_2018_us_state_500k/cb_2018_us_state_500k.shp"
shape = gpd.read_file(shape_path)
#print (shape['NAME'])
shape = pd.merge(
    left=shape,
    right=df_covid,
    left_on='NAME',
    right_on='State',
    how='left'
    )   # this create a left join

ax = shape.boundary.plot()
shape.plot(ax=ax, column='Death Rate per 100000')
#plt.show()
ax = shape.boundary.plot()
shape.plot(ax=ax, column='Death Rate per 100000')
#plt.show()
ax = shape.boundary.plot(edgecolor='black',linewidth=0.2, figsize=(10, 5))  ### edgewith=boder aroun the state, linewidth= how big is the Border
shape.plot(ax=ax, column='Death Rate per 100000',legend=True,cmap='OrRd')
# remove the border
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
for edge in ['right','bottom','top', 'left']:
    ax.spines[edge].set_visible(False)
    
#add title
ax.set_title('Covid-19 death Rate per 100000 from January 2020 to November 2020', size=12, weight='bold')
ax 
plt.xlim(-150, -50)
plt.ylim(25, 50)
plt.show()

# Ploting ecoli resistant rate
read_ecoli_file=pd.read_csv("Multidrug_resist_ecoli.csv")                              # reading the file
#print(read_ecoli_file)
ecoli_df=read_ecoli_file[["State", "Percent Resistant"]]                           #select state and percent resistant rate column
#print(percent_rate)
shape = pd.merge(
    left=shape,
    right=ecoli_df,
    left_on='NAME',
    right_on='State',
    how='left'
    )   # this create a left join

#print(shape.columns)
ax = shape.boundary.plot()
shape.plot(ax=ax, column='Percent Resistant')
#plt.show()
# to zoom in the map
#shape = shape[~shape['NAME'].isin(['Alaska',' Hawaii', 'Puerto Rico'])]
ax = shape.boundary.plot()
shape.plot(ax=ax, column='Percent Resistant')
#plt.show()
ax = shape.boundary.plot(edgecolor='black',linewidth=0.2, figsize=(10, 5))  ### edgewith=boder aroun the state, linewidth= how big is the Border
shape.plot(ax=ax, column='Percent Resistant',legend=True,cmap='PuRd')
# remove the border

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
for edge in ['right','bottom','top', 'left']:
    ax.spines[edge].set_visible(False)
    
#add title
ax.set_title('2018 e.coli Percent Resistant Rate', size=14, weight='bold')
ax 
plt.xlim(-150, -50)
plt.ylim(25, 50)
plt.show()


# acinobactor resistant rate
# Ploting ecoli resistant rate
#read_acinetobacter=pd.read_csv("Mdr_acinetobacter.csv")                            # reading the file
#print(read_ecoli_file)

read_acinetobacter=pd.read_csv("Mdr_acinetobacter.csv")                            # reading the file
#print(read_ecoli_file)
 
#acinetobacter_df=read_acinetobacter[["State", "aPercent Resistant"]]                        #select state and percent resistant rate column
#print(acinetobacter_df)
acinetobacter_df=read_acinetobacter[["State", "Percent Resistant"]]                        #select state and percent resistant rate column
#print(percent_rate)
shape = pd.merge(
    left=shape,
    right= acinetobacter_df,
    left_on='NAME',
    right_on='State',
    how='left'
    )   # this create a left join

ax = shape.boundary.plot()
shape.plot(ax=ax, column='Percent Resistant')
#plt.show()

ax = shape.boundary.plot()
shape.plot(ax=ax, column='Percent Resistant')
#plt.show()
ax = shape.boundary.plot(edgecolor='black',linewidth=0.2, figsize=(10, 5))  ### edgewith=boder aroun the state, linewidth= how big is the Border
shape.plot(ax=ax, column='Percent Resistant',legend=True,cmap='YlOrBr')
# remove the border
ax.set_title('2018 Acinetobacter Percent Resistant Rate', size=14, weight='bold')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
for edge in ['right','bottom','top', 'left']:
    ax.spines[edge].set_visible(False)
    
plt.xlim(-150, -50)
plt.ylim(25, 50)
plt.show()
'''

#flouroquinolone percent resistant rate
read_fluoroquinolone=pd.read_csv("Fluoroquinolone_MRSA.csv")                          # reading the file
#print(read_ecoli_file)
 
#acinetobacter_df=read_acinetobacter[["State", "aPercent Resistant"]]                        #select state and percent resistant rate column
#print(acinetobacter_df)
fluoroquinolone_df=read_fluoroquinolone[["State", "fPercent Resistant"]]                        #select state and percent resistant rate column
#print(percent_rate)
shape = pd.merge(
    left=shape,
    right= fluoroquinolone_df,
    left_on='NAME',
    right_on='State',
    how='left'
    )   # this create a left join

ax = shape.boundary.plot()
shape.plot(ax=ax, column='fPercent Resistant')
#plt.show()

ax = shape.boundary.plot()
shape.plot(ax=ax, column='fPercent Resistant')
#plt.show()
ax = shape.boundary.plot(edgecolor='black',linewidth=0.2, figsize=(10, 5))  ### edgewith=boder aroun the state, linewidth= how big is the Border
shape.plot(ax=ax, column='Percent Resistant',legend=True,cmap='BuPu')
# remove the border
ax.set_title('2018 Fluoroquinolone percent Resistant Rate', size=14, weight='bold')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
for edge in ['right','bottom','top', 'left']:
    ax.spines[edge].set_visible(False)
    
plt.xlim(-150, -50)
plt.ylim(25, 50)
plt.show()



'''



















