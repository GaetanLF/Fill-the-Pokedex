# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 08:36:35 2021

@author: Gaetan LF
"""



#----------------------------------- PACKAGES --------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import os
#-----------------------------------------------------------------------------



#---------------- PLEASE MODIFY THOSE PATHS IF NECESSARY ---------------------
driverPath = ".//chromedriver.exe"
pathfile = ".//Pokemon.csv"
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
def driverGUI(path,GUI=True):
    '''
    It launches the driver and decides whether the GUI should be printed on screen or not.
    
    path : Driver path
    GUI : Boolean for GUI, default True
    '''
    if GUI == False:
        options = Options()
        options.headless = True # Options hide the GUI (Chrome will not be seen as launched)
        driver = webdriver.Chrome(options=options, executable_path=driverPath) # Chrome is launched
    else:
        driver = webdriver.Chrome(executable_path=driverPath) # Chrome is launched
    return(driver)
#-----------------------------------------------------------------------------


        
#----- Activation of the driver (with GUI or not). Uses Chrome. --------------
driver = driverGUI(driverPath,GUI=False)
#-----------------------------------------------------------------------------



#---------------------------- DB IMPORTATION ---------------------------------
df = pd.read_csv(pathfile)
namesVariables = ['height','weight','catchRate','maleRatio','hatchSteps','evolLevel']
for newVar in namesVariables:
    df[newVar] = np.nan # New variables are temporarly filled with NaN.
#-----------------------------------------------------------------------------



#------- Defining full xpaths on the webpage and scrapped variables ----------
xPathList = [['/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[6]/td[1]/table/tbody/tr[1]/td[2]',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[6]/td[2]/table/tbody/tr[1]/td[2]',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr/td',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[4]/td[1]/table/tbody/tr[2]/td/a/span[1]',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[5]/td/table/tbody/tr/td[2]/table/tbody/tr/td',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[9]/td/table/tbody/tr[1]/td'],
             ['/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[6]/td[1]/table/tbody/tr[3]/td[2]',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[6]/td[2]/table/tbody/tr[3]/td[2]',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr/td',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[4]/td[1]/table/tbody/tr[2]/td/a/span[1]',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[5]/td/table/tbody/tr/td[2]/table/tbody/tr/td',
             '/html/body/div[1]/div[2]/div/div[7]/div/div[1]/div[4]/table[2]/tbody/tr[9]/td/table/tbody/tr[1]/td']]

# Two lists for two loops.


scrappedVariables = [i for i in range(0,6,1)] # List of 6 elements, 6 scrapped vars
emptyValues = [] # Will contain all pokemon names for which we do not have any informations.
#-----------------------------------------------------------------------------



#-------------------------- Preparing logs -----------------------------------
try:
    os.mkdir('.//Exports')
except:
    pass

with open('.//Exports//log.txt','a+') as dataFile:
    dataFile.write('\n\n ====== SCRAPPING LOG ======\n\n')
#----------------------------------------------------------------------------- 



#------------------------ CORE SCRAPPING LOOP --------------------------------
# We take the source code and parse it.
for Pkmn in df['Name'].tolist(): # For each Pokemon's name in the list

    url = f'https://bulbapedia.bulbagarden.net/wiki/{Pkmn}_(Pok%C3%A9mon)'
    driver.get(url) # We get the right url
    print(f'Getting informations for {Pkmn} on {url} ...')
    with open('.//Exports//log.txt','a+') as dataFile:
        try:
            dataFile.write(f'Getting informations for {Pkmn} on {url} ...\n')
        except:
            dataFile.write('Getting informations for a Pokemon whose name couldn\'t be encoded ...\n')
    try:
        for sVar in range(0,len(scrappedVariables),1): # For each variable in the scrapped list
            scrappedVariables[sVar] = driver.find_element_by_xpath(xpath=xPathList[0][sVar]).text # We scrap.
            df[namesVariables[sVar]].loc[df['Name'] == Pkmn] = scrappedVariables[sVar]
    except:
        print(f'There is no such information for {Pkmn}, it should be fill by hand.')
        with open('.//Exports//log.txt','a+') as dataFile:
            try:
                dataFile.write(f'\nThere is no such information for {Pkmn}, it should be fill by hand.\n')
            except:
                dataFile.write('\nThere is no such information for a Pokemon whose name couldn\'t be encoded, it should be fill by hand.\n')
        emptyValues.append(Pkmn)
#-----------------------------------------------------------------------------



#---------------Intermediary  scrapping report -------------------------------
print(f'\n\n FIrst scrapping finished. {len(emptyValues)} pokemons missing.')
with open('.//Exports//log.txt','a+') as dataFile:
            dataFile.write(f'\n\n scrapping finished. {len(emptyValues)} pokemons missing.\n')
#-----------------------------------------------------------------------------



#---------------------- Screening Mega Pokemons ------------------------------
megaStr = [emptyValues[i].lower().find("mega") for i in range(0,len(emptyValues),1)] 
# For each missing Pokemon, check if "Mega" is in the name. Returns either the index or -1 (if not in str)
MegaPkmn = []
MissingPkmn = []
for i in range(0,len(megaStr),1):
    if megaStr[i] == -1:
        MissingPkmn.append(emptyValues[i])
    else:
        MegaPkmn.append(emptyValues[i][megaStr[i]+5:])
del emptyValues # Since we do not need it anymore, it has been split.
del megaStr
#-----------------------------------------------------------------------------



#---------------------- SECOND SCRAPPING LOOP MEGA POKEMONS ------------------
print("\n Second scrapping loop starting.")
with open('.//Exports//log.txt','a+') as dataFile:
            dataFile.write('Second scrapping for Mega Pokemons.\n')
for MPkmn in MegaPkmn: # For each identified mega Pokemon
    url = f'https://bulbapedia.bulbagarden.net/wiki/{MPkmn}_(Pok%C3%A9mon)'
    driver.get(url) # We get the right url
    print(f'Getting informations for {MPkmn} on {url} ...')
    with open('.//Exports//log.txt','a+') as dataFile:
        try:
            dataFile.write(f'Getting informations for {Pkmn} on {url} ...\n')
        except:
            dataFile.write('Getting informations for a Pokemon whose name couldn\'t be encoded ...\n')
    try:
        for sVar in range(0,len(scrappedVariables),1): # For each variable in the scrapped list
            scrappedVariables[sVar] = driver.find_element_by_xpath(xpath=xPathList[1][sVar]).text # We scrap.
            df[namesVariables[sVar]].loc[df['Name'] == MPkmn+"Mega "+MPkmn] = scrappedVariables[sVar]
    except:
        print(f'There is no such information for {MPkmn}\'s mega form, it should be fill by hand.')
        with open('.//Exports//log.txt','a+') as dataFile:
            try:
                dataFile.write(f'\nThere is no such information for {MPkmn}\'s mega form, it should be fill by hand.\n')
            except:
                dataFile.write('\nThere is no such information for a Pokemon\'s mega form whose name couldn\'t be encoded, it should be fill by hand.\n')
                
print('Second scrapping loop finished.')
with open('.//Exports//log.txt','a+') as dataFile:
            dataFile.write('\n Second scrapping loop finished.\n')
#-----------------------------------------------------------------------------



# ---------------- Cleaning the dataframe ------------------------------------
def suppressAst(x):
    if str(x)[-1] =="*":
        return str(x)[:-1]
    else:
        return str(x)
    
def modifEvolLevel(x):
        if str(x)[-1]=='n':
            return(np.nan)
        else:
            return(float(str(x)[-1]))
        
def modifHatchSteps(x):
    '''
    Puts the mean.
    '''
    if str(x)[-5:] == 'steps':
        val = str(x)[:-5].split()
        return(np.mean(np.array([float(val[0]),float(val[2])])))
    else:
        return(np.nan)
    
def modifMaleRatio(x):
    if str(x) == 'nan':
        return(np.nan)
    X = str(x).split()
    if str(X[1]).lower() == 'female':
        return(1-0.01*float(str(X[0][:-1])))
    elif str(X[1]).lower() == 'male':
        return(0.01*float(str(X[0][:-1])))
    else:
        print("Warning, fail while screening the pokemon's gender.")
        return (x)
    
def modifStats(x):
    if str(x) == 'nan':
        return(np.nan)
    return(float(str(x).split()[0]))
    
    
df['evolLevel'] = df['evolLevel'].apply(suppressAst).apply(modifEvolLevel)

df['hatchSteps'] = df['hatchSteps'].apply(modifHatchSteps)

df['maleRatio'] = df['maleRatio'].apply(modifMaleRatio)

df['catchRate'] = df['catchRate'].apply(modifStats)
df['height'] = df['height'].apply(modifStats)
df['weight'] = df['weight'].apply(modifStats)
#-----------------------------------------------------------------------------



df.to_csv("PokemonNew.csv")
