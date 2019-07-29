from dataclasses import dataclass

from enum import Enum


class Einvert(Enum):
    Yes = "true"
    No = "false"
    Default = ""


@dataclass
class TrspData:
    Satellite: str = ""
    Number: int = 0
    Uplink: str = ""
    Downlink: str = ""
    Beacon: str = ""
    Mode: str = ""
    Callsign: str = ""
    Status: str = "Active"

    # INVERT: Einvert = Einvert.Default

    def show(self):
        # if self.Number == 14781:
        #     if len(self.Mode.split(' ')) > 0:
        #         print(self)

        print('=' * 120)
        print(self)

    # print(self)+"\n"

    def format(self):
        """Return a TRSP Format file as a string
        [Mode V Digitalker (Voices Messages and Telemetry)]
DOWN_LOW=145950000
MODE=FM

[Mode V Imaging (Robot 36 SSTV from onboard cameras)]
DOWN_LOW=145950000
MODE=SSTV in FM carrier

[Mode V Telemetry (1000 baud (400 baud backup))]
DOWN_LOW=145920000
MODE=BPSK 1000 bps

[Mode U/V (B) Linear Transponder]
UP_LOW=435742000
UP_HIGH=435758000
DOWN_LOW=145922000
DOWN_HIGH=145938000
INVERT=true

[Mode V TLM Beacon (CW-2, BPSK-1000)]
DOWN_LOW=145919000
MODE=CW

[Mode V TLM Beacon (CW-1, BPSK-400)]
DOWN_LOW=145939000
MODE=CW


        """

        if self.Beacon is not '':
            part1 = "\n[Mode {0}  BEACON ({0}) ]\nMODE={0},DOWN_LOW={1}\n".format(self.Mode, self.Beacon)
        else:
            part1 = ""

        if self.Uplink != '' and self.Downlink != '.' :
            # Digi repeater .... No uplink
            part1 += "\n[Mode {0} Repeater ({0}) ]\nMODE={0},DOWN_LOW={1}\n".format(self.Mode, self.Downlink)

        return part1
