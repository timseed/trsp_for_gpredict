import pandas as pd
import numpy as np
import requests
import json

# Update this to your Home QTH in GPredict
MyQth = "Areanas.qth"   

if MyQth == "Areanas.qth":
   print("")
   print("You are almost certainly using the programmers QTH please edit and update the value MyQth\n"*5)
   print("")

#
# No More changes below are needed
#


print("Getting Modes")
data_modes=requests.get('https://db.satnogs.org/api/modes')
df_modes = pd.DataFrame.from_records(json.loads(data_modes.content))

print("Getting satellites")
data_satellites=requests.get('https://db.satnogs.org/api/satellites')
df_satellites = pd.DataFrame.from_records(json.loads(data_satellites.content))

print("Getting transmitters")
data_transmitters=requests.get('https://db.satnogs.org/api/transmitters')
df_transmitters = pd.DataFrame.from_records(json.loads(data_transmitters.content))

df = df_transmitters.merge(df_satellites,on=['norad_cat_id'],how='left')
print("Data Merged")
df.set_index(['norad_cat_id'],inplace=True)

# It is really this simple
df=df[df.alive == 1]


def f_check(f):
    """
    Remove the NaN values and check the data.
    :param f frequency
    returns: int value of 0 or the int value of the specified frequency in Hertz
    """
    try:
        if f>1:
            return int(f)
        else:
            return int(0)
    except:
        return int(0)
    
df['downlink_low_mhz'] =df.downlink_low.apply(lambda x: f_check(x))
df['downlink_high_mhz']=df.downlink_high.apply(lambda x: f_check(x))
df['uplink_low_mhz']   =df.uplink_low.apply(lambda x: f_check(x))
df['uplink_high_mhz']  =df.uplink_high.apply(lambda x: f_check(x))
print("Freq checked")
pre_idx=-1
of=None
print("Trsp generation started")
for index, record in df.iterrows():
    if index != pre_idx:
        if of:
            of.close()    
        of=open(f"{index}.trsp","wt")
        pre_idx=index
    if record['mode'] in ['CW','FM','FMN','USB']:
        #Mode more simple
        title=f"[Mode {record['mode']} {record['description']}]"
    else:
        #Mode Complex Modes
        title=f"[Mode {record['mode']} (Baud {record['baud']} {record['description']})]"
    of.write(f"{title}\n")
    
    # Invert Rule
    if record['invert']:
        of.write(f"INVERT=true\n")
        
    # Baud Rule
    if record['baud']>0.0:
        of.write(f"MODE={record['mode']} {record['baud']}\n")
    else:
        of.write(f"MODE={record['mode']}\n")
    
    #Downlink Rule
    if record['downlink_high_mhz'] == 0:
        #print(f"Uplink is {record['downlink_high_mhz']} ")
        of.write(f"DOWN_LOW={record['downlink_low_mhz']}\n")
    else:
        of.write(f"DOWN_HIGH={record['downlink_high_mhz']}\n")                            
        of.write(f"DOWN_LOW={record['downlink_low_mhz']}\n")  

    #Uplink Rule
    if record['uplink_high_mhz'] != 0:
        of.write(f"UP_LOW={record['uplink_high_mhz']}\n")
    if record['uplink_low_mhz'] != 0:
        of.write(f"UP_LOW={record['uplink_low_mhz']}\n") 
                 
    of.write("\n\n")
print("Trsp generation started")

print("Module generation started")
for mode in df['mode'].unique():
        norad_ids=[]
        for index,rec in df.iterrows():
              if rec['mode']==mode:
                  norad_ids.append(index)
        if norad_ids != [] and mode:
             file_name=mode[0].upper()+mode[1:].lower()
             with open(f"{file_name}.mod","wt") as mod_file:
                # We need this header
                # You will need a Qth of the same name ... or alter the code/gpredict
                mod_file.write("[GLOBAL]\nQTHFILE=Arenas.qth\nSATELLITES=")
                norad_ids = list(set(norad_ids))
                norad_ids.sort() #They may as well be Numeric in order
                sat_line=';'.join([str(i) for i in norad_ids])
                mod_file.write(f"{sat_line}\n")
print("Module generation finished")

print("""
Please now check the files called .mod and .trsp in this directory.

If they look ok then do the following commands. Please understand
this will overwrite ANYTHING you have previously entered in GPredict (Transponder and Modules).

Transponders.

cp *.trsp ~/.config/Gpredict/trsp/

And for the modules

cp *.mod ~/.config/Gpredict/Modules

""")
