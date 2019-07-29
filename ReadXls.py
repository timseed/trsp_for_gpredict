import numpy as np
import pandas as pd
import xlrd
from trsp_data import *


def MhzToHz(Mhz):
    return Mhz * 1000000 if Mhz != np.NaN else 0


def CallCheck(Call):
    return Call if Call != np.NaN else ""

def ToInt(Num):
    try:
        return int(Num)
    except:
        return -1

df = pd.read_excel("satslist.xls", header=10)
df.rename(columns={'Unnamed: 7': 'Status'}, inplace=True)
print(df.columns)
# We want just the Active Sats
df_active = df[df.Status == '*']
df_active['Number'] = df_active.Number.apply(lambda x: ToInt(x))
#df_active['Uplink'] = df_active.Uplink.apply(lambda x: MhzToHz(x))
#df_active['Downlink'] = df_active.Downlink.apply(lambda x: MhzToHz(x))
#df_active['Beacon'] = df_active.Beacon.apply(lambda x: MhzToHz(x))
df_active['CallSign'] = df_active.Callsign.apply(lambda x: CallCheck(x))


#print(df_active)

for row in df_active.itertuples():
    sat_rec = TrspData(row.Satellite,
                       row.Number,
                       row.Uplink,
                       row.Downlink,
                       row.Beacon,
                       row.Mode,
                       row.Callsign,
                       row.Status)
    sat_rec.show()