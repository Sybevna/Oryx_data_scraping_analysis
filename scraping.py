# Import modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
#%% Open browser and navigate to page to retrieve data from
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html")
#%% Retrieve content from HTML page
# Y= []
content = driver.page_source
soup = BeautifulSoup(content)
# Tags = soup.find_all(id= 'Pistols') # Find all objects with ID "Pistols" - i.e all vehicles categories
# for i in range(len(Tags)):
#     print(Tags[i].contents[0])
#     if len(str(Tags[i].contents[0])) > 1: # Get rid of the empty lines
#         Y.append(str(Tags[i].contents[0]))

Data = []
#Names = []
df = pd.DataFrame()
Tags2 = soup.find_all("h3") # Retrive all content of h3 tags- where data of interest is stored
for j in range(len(Tags2)):
    #print(str(Tags2[j].contents))
    if len(str(Tags2[j].contents[0])) > 1 :
        Data.append(str(Tags2[j].contents)) # Dump everything into Data array
        #Names.append(str(Tags2[j].contents[0]))
    
#%% Cleanup data - to be put in separate file
def cleanup(X):
    for i in range(len(X)):
        if chr(34) in X[i]:
            X[i]=X[i].replace('"','')
        if "'" in X[i]:
                X[i]=X[i].replace("'",'')    
        if "class=mw-headline id=Pistols>" in X[i]:
            X[i]=X[i].replace('class=mw-headline id=Pistols>','')
        if "</span>," in X[i]:
            X[i]=X[i].replace('</span>,','')
        if "style=color: red;>" in X[i]:   
            X[i]=X[i].replace('style=color: red;>','')
        if "<br/></span>" in X[i]:
            X[i]=X[i].replace('<br/></span>','')    
        if "-" in X[i]:
            X[i]=X[i].replace('-','')    
        if ":" in X[i]:
            X[i]=X[i].replace(':','')
        if "," in X[i]:
            X[i]=X[i].replace(',','')
        if "of which" in X[i]:
            X[i]=X[i].replace('of which','')
        if "(" in X[i]:
            X[i]=X[i].replace('(','')
        if ")" in X[i]:
            X[i]=X[i].replace(')','')
        if "<br/>" in X[i]:
            X[i]=X[i].replace('<br/>','')     
        if "[" in X[i]:
            X[i]=X[i].replace('[','')
        if "]" in X[i]:
            X[i]=X[i].replace(']','')  
        if "<span" in X[i]:
            X[i]=X[i].replace('<span','') 
        if "</span>" in X[i]:
            X[i]=X[i].replace('</span>','')
    return X
#%% Remove all the HTML characters and things we don't need
cleanup(Data)
#%% Split all elements into different str
for i in range(len(Data)):
    Data[i] = Data[i].split()
#%% Put all rows in same format
# This handles cases where all the categories are not all present, or 2 are present, or 3 etc...
# The idea is to standardise the format of the data to put everything in DF after

for i in range(len(Data)):
        if "captured" in Data[i] and "destroyed" not in Data[i] and "damaged" not in Data[i] and "abandoned" not in Data[i]:
            j = Data[i].index("captured")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1+ ["destroyed"] + [" 0 "] + ["damaged "] + ["0 "] +  ["abandoned "] + ["0 "]+ temp2
            continue
            
        if "abandoned" in Data[i] and "destroyed" not in Data[i] and "damaged" not in Data[i] and "captured" not in Data[i]:
            j = Data[i].index("abandoned")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1+ ["destroyed"] + [" 0 "] + ["damaged "] + ["0 "]  + temp2 +  ["captured "] + ["0 "]
            continue
            
        if "damaged" in Data[i] and "destroyed" not in Data[i] and "abandoned" not in Data[i] and "captured" not in Data[i]:
            j = Data[i].index("damaged")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1+ ["destroyed"] + [" 0 "] + temp2 + ["abandoned "] + ["0 "]   +  ["captured "] + ["0 "]
            continue
            
        if "destroyed" in Data[i] and "damaged" not in Data[i] and "abandoned" not in Data[i] and "captured" not in Data[i]:
            j = Data[i].index("destroyed")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1+  temp2 +["damaged "] + ["0 "] +  ["abandoned "] + ["0 "]  +  ["captured "] + ["0 "]
            continue
            ## 2 out of 4
        if "destroyed" not in Data[i] and "damaged" not in Data[i] and "abandoned"  in Data[i] and "captured"  in Data[i]: 
            j = Data[i].index("abandoned")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1+ ["destroyed"] + [" 0 "] +  ["damaged "] + ["0 "] + temp2
            continue
            
        if "destroyed" not in Data[i] and "damaged" in Data[i] and "abandoned"  in Data[i] and "captured" not in Data[i]: 
            j = Data[i].index("damaged")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1+ ["destroyed"] + ["0 "] + temp2 +  ["captured "] + ["0 "] 
            continue
            
        if "destroyed" in Data[i] and "damaged" in Data[i] and "abandoned" not in Data[i] and "captured" not in Data[i]: 
            Data[i] = Data[i]+  ["abandoned "] + ["0 "] +  ["captured "] + ["0 "]  
            continue
            
        if "destroyed" in Data[i] and "damaged" not in Data[i] and "abandoned" in Data[i] and "captured" not in Data[i]: 
            j = Data[i].index("abandoned")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1 +["damaged "] + ["0 "] + temp2 +   ["captured "] + ["0 "]
            continue
            
        if "destroyed" in Data[i] and "damaged" not in Data[i] and "abandoned" not in Data[i] and "captured"  in Data[i]: 
            j = Data[i].index("captured")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1 + ["damaged "] + ["0 "] + ["abandoned "] + ["0 "]   + temp2   
            continue

        if "destroyed" not in Data[i] and "damaged" in Data[i] and "abandoned" not in Data[i] and "captured" in Data[i]: 
            j = Data[i].index("damaged")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:j+2]
            temp3 = Data[i][j+2:]
            Data[i] = temp1 + ["destroyed"] + [" 0 "] + temp2+  ["abandoned "] + ["0 "]   + temp3   
            continue

        if "destroyed" not in Data[i] and "damaged" in Data[i] and "abandoned"  in Data[i] and "captured" in Data[i]: 
            j = Data[i].index("damaged")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1 + ["destroyed"] + temp2   
            continue
            
        if "destroyed"  in Data[i] and "damaged" in Data[i] and "abandoned"  in Data[i] and "captured" not in Data[i]: 
            j = Data[i].index("damaged")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = Data[i] +  ["captured "] + ["0 "]
            continue

        if "destroyed"  in Data[i] and "damaged" in Data[i] and "abandoned" not in Data[i] and "captured" in Data[i]: 
            j = Data[i].index("captured")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1 +  ["abandoned "] + ["0 "] + temp2
            continue
            
        if "destroyed"  in Data[i] and "damaged" not in Data[i] and "abandoned"  in Data[i] and "captured" in Data[i]: 
            j = Data[i].index("abandoned")
            temp1 = Data[i][0:j]
            temp2 = Data[i][j:]
            Data[i] = temp1 +  ["damaged "] + ["0 "] + temp2    
            continue
  
#%% Collapse names in 1 str for long vehicle names
for i in range(len(Data)):   
    j = Data[i].index("destroyed")
    Data[i] = [' '.join(Data[i][:j-1])] + Data[i][j-1:] # Use j-1 to point grab everything BEFORE the total number for each category
    if "Ukraine" in Data[i]:
        k = i
#%% Get everything into Pandas Dataframe - split into 2 dataframes for each country
df_ru = pd.DataFrame(Data[:k], columns = ['Vehicle Type', 'Total', 'des','Destroyed','dam','Damaged','aba','Abandoned','capt','Captured'])  
df_ua = pd.DataFrame(Data[k:], columns = ['Vehicle Type', 'Total', 'des','Destroyed','dam','Damaged','aba','Abandoned','capt','Captured']) 
#%% Convert columns to numeric
df_ru.Total=pd.to_numeric(df_ru.Total)
df_ru.Destroyed=pd.to_numeric(df_ru.Destroyed)
df_ru.Damaged=pd.to_numeric(df_ru.Damaged)
df_ru.Abandoned=pd.to_numeric(df_ru.Abandoned)
df_ru.Captured=pd.to_numeric(df_ru.Captured)

df_ua.Total=pd.to_numeric(df_ua.Total)
df_ua.Destroyed=pd.to_numeric(df_ua.Destroyed)
df_ua.Damaged=pd.to_numeric(df_ua.Damaged)
df_ua.Abandoned=pd.to_numeric(df_ua.Abandoned)
df_ua.Captured=pd.to_numeric(df_ua.Captured)

#%% Get rid of columns with same words - tidy up
df_ru =df_ru.drop(labels = ["des", "dam","aba","capt"],axis = 1)       
df_ua =df_ua.drop(labels = ["des", "dam","aba","capt"],axis = 1)
#%% Plotting section
ax = df_ru.iloc[1:].plot.bar(x = 'Vehicle Type', stacked=True, title = "Russia", grid  =True) # bar chart RU
ax.figure.savefig('stacked_chart_Russia.png',bbox_inches="tight", dpi = 600 )
ax1 = df_ua.iloc[1:].plot.bar(x = 'Vehicle Type', stacked=True, title = "Ukraine", grid  =True) # bar chart UA
ax1.figure.savefig('stacked_chart_Ukraine.png',bbox_inches="tight", dpi = 600 )

#%% Russian/Ukrainian summary - subplot
fig1, (ax2, ax3) = plt.subplots(nrows=2, ncols=1) # two axes on figure
Tasks = df_ru.loc[0].loc[["Destroyed","Damaged","Abandoned","Captured"]]
my_labels = ["Destroyed","Damaged","Abandoned","Captured"]
ax2.pie(Tasks,labels=my_labels,autopct='%1.1f%%')
ax2.set_title("Russian losses")
ax2.axis('equal')
#ax2.plt.show()

Tasks_ua = df_ua.loc[0].loc[["Destroyed","Damaged","Abandoned","Captured"]]
my_labels = ["Destroyed","Damaged","Abandoned","Captured"]
ax3.pie(Tasks_ua,labels=my_labels,autopct='%1.1f%%')
ax3.set_title("Ukrainian losses")
ax3.axis('equal')
#ax3.show()
fig1.savefig('Pie_chart_RU_UA.png',bbox_inches="tight", dpi = 600 )

fig1, ax1 = plt.subplots()
Tasks = df_ru.loc[0].loc[["Destroyed","Damaged","Abandoned","Captured"]]
my_labels = ["Destroyed","Damaged","Abandoned","Captured"]
ax1.pie(Tasks,labels=my_labels,autopct='%1.1f%%')
ax1.set_title("Russian losses")
ax1.axis('equal')
fig1.savefig('Pie_chart_RU.png',bbox_inches="tight", dpi = 600 )
#ax2.plt.show()

fig1, ax1 = plt.subplots()
Tasks = df_ua .loc[0].loc[["Destroyed","Damaged","Abandoned","Captured"]]
my_labels = ["Destroyed","Damaged","Abandoned","Captured"]
ax1.pie(Tasks,labels=my_labels,autopct='%1.1f%%')
ax1.set_title("Ukrainian losses")
ax1.axis('equal')
fig1.savefig('Pie_chart_UA.png',bbox_inches="tight", dpi = 600 )
#ax2.plt.show()
#%% Russian losses per vehicle type
path_ru = os.path.join(os.getcwd(), 'Russia')
if not os.path.exists('Russia'):
    os.makedirs('Russia')

for i in range(1,len(df_ru)):
    fig1, ax1 = plt.subplots()
    Tasks = df_ru.loc[i].loc[["Destroyed","Damaged","Abandoned","Captured"]]
    my_labels = ["Destroyed","Damaged","Abandoned","Captured"]
    ax1.pie(Tasks,labels=my_labels,autopct='%1.1f%%')
    ax1.set_title(df_ru.loc[i].loc["Vehicle Type"])
    ax1.axis('equal')
    #plt.show()
    fig1.savefig(os.path.join(path_ru, 'Pie_chart_RU_'+df_ru.loc[i].loc["Vehicle Type"]+'.png'),bbox_inches="tight", dpi = 600 )
    
path_ua = os.path.join(os.getcwd(), 'Ukraine')
if not os.path.exists('Ukraine'):
    os.makedirs('Ukraine')
    
for i in range(1,len(df_ua)):
    fig1, ax1 = plt.subplots()
    Tasks = df_ua.loc[i].loc[["Destroyed","Damaged","Abandoned","Captured"]]
    my_labels = ["Destroyed","Damaged","Abandoned","Captured"]
    ax1.pie(Tasks,labels=my_labels,autopct='%1.1f%%')
    ax1.set_title(df_ua.loc[i].loc["Vehicle Type"])
    ax1.axis('equal')
    #plt.show()
    fig1.savefig(os.path.join(path_ua, 'Pie_chart_UA_'+df_ua.loc[i].loc["Vehicle Type"]+'.png'),bbox_inches="tight", dpi = 600 )