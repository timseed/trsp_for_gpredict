# GPredict - Generate TRSP and MOV groups

I like using GPredict, however I find it painful in 

  - time
  - complexity 

to setup the groups of Satelites that I wish to follow. Furthermore when I have, it is almost a certainty that the transponder information is not present.

This small python script is an attempt to connect that.

# Requirements

You need to the following

  - Python3

When you have python3.7 installed then you will need to add

  - requests
  - pandas
  - numpy

This is done like this

    pip instal requests, pandas, numpy

You can then run the supplied python script - called trsp.py

    python3 trsp.py

If you see a message of 

    You are almost certainly using the programmers QTH please edit and update the value MyQth

You need to edit the trsp.py file, and replace the value of Areanas with your Qth as you entered in GPredict. Else ... The Modules will be developed from my house and not yours.


