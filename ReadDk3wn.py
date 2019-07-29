import numpy as np
import pandas as pd
import os
from trsp_data import *

def GetData():
    df = pd.read_html('http://www.dk3wn.info/p/?page_id=29535')
    sats = df[0]
    sats.to_pickle('dk3wn.pickle')
    print("Data Pickled")

def MhzToHz(Mhz):
    return Mhz * 1000000 if Mhz != np.NaN else 0


def CallCheck(Call):
    return Call if Call != np.NaN else ""


if not os.path.isfile('dk3wn.pickle'):
    print("Need to pull the Web Page")
    GetData()
else:
    print("Data Already here")
sats = pd.read_pickle('./dk3wn.pickle')
# Remove the Not yet active Sats
sats = sats[(sats.Status == 'ACTIVE') & (sats.NORAD != 'tbd')]
#sats['Downlink'] = sats.Downlink.apply(lambda x: MhzToHz(x))



# How Many Modes are there ?
sats['ModeCnt'] = sats.Mode.apply(lambda x: len(x.split(' ')))

# Look for the expression SK (BPSK FSK etc) in the Mode Setting... this complicates the parsing.
sats['DIGITAL'] = sats.Mode.apply(lambda x: 1 if 'SK' in x.upper() else 0)
sats.Callsign.replace('nan', "")

for row in sats[(sats.DIGITAL == 0) & (sats.ModeCnt ==1)].itertuples():
    sat_rec = TrspData(row.Satellite,
                       row.NORAD,
                       row.Uplink,
                       row.Downlink,
                       row.Beacon,
                       row.Mode,
                       row.Callsign,
                       row.Status)
    print("Norad ID {}".format(row.NORAD))
    print(sat_rec.format())