# Auto-Brightness
Screen Brightness adjusts automatically per screen content 

If you all develop in dark mode like me but need to switch to webpages constantly (which sadly are still in the OHH MY EYES!!! mode) you might need to constantly change brightness whenever you change windows... This script is just for that, it averages up the pixel values over the screen and adjusts the brightness (inversely) proportional to it.  

Currently the R, G and Bs are computed separately so as to keep an option of having individual sensitivities / offsets in later commits. 

This model is inversely proportional to RGB values sum, models based on differences to last frame can also be considered later.

Low pass filter is used by default to smoothe the sudden changes in brightness, just pass argument <-nl> to disable it. 

**Arguments:**  
-nl : Deactivate low pass filter (smoothing change) for crisp response   

**Script Inputs:**  
In case the content adjusted brightness is too low or high in some cases, an offset can be set up.
**'+'** and **'-'** are accepted inputs and increase / decrease brightness by 2% respectively. 
Multiple inputs are accepted. ex. **'++++++'** will increase the offset brightness by 12% (2% for each '+')
Press enter after every input

**Planned updates :** 
Offset storage to disk  
Currently mean of pixels is used to compute brightness, Median, Mode functionalities can be added later 

Python Modules Used : PIL, os, time, traceback, numpy, sys, inspect, mss, threading, gi.repository, argparse

Just run the file AutoBri.py, adjust the offsets if needed and save your eyes!

**PS:**
This might have some bugs, Do let me know (hemanshu.kale@gmail.com) in case of any random problems / bugs
Tested currently only on Ubuntu 18.04LTS, will add cross platform functionalities soon..
