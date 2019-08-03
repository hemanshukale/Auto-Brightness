############### MODULE FOR ADJUSTING SCREEN BRIGHTNESS ACCORDING TO SCREEN CONTENT #################
from PIL import Image
import os, time, traceback, numpy, sys, inspect
from mss import mss
from threading import Thread
from gi.repository import Gdk
import argparse
p3 = sys.version_info > (2,8)
def ins():
    return inspect.getframeinfo(inspect.stack()[1][0]).lineno # For debugging, prints line number which called this function

parser = argparse.ArgumentParser()
parser.add_argument("-nl", "--nolowpass", action="store_true", help='Disable Low pass filter' )

cmd_args  = parser.parse_args()
print(ins(), cmd_args)
if cmd_args.nolowpass :
    filter_weight = 0
    print('Low pass filter disabled')
else :
    filter_weight = 0.5 # weightage for low pass filter
    print('Low pass filter on')

bmin,bmax,offset = 0.02, 1, 0 # Min, Max limits, offsets for brightness in fraction(%)

screen = Gdk.Screen.get_default()
display_name = screen.get_monitor_plug_name(screen.get_primary_monitor()) # Get screen name to pass as an argument to change brightness
######## Here we change brightness using xrandr command as I couldn't get xbacklight to work with Ubuntu 18.04 LTS , however if you manage to get it work you can use that instead of xrandr #############
brightness_command = 'xrandr --output {} --brightness '.format(display_name) # Command for brightness change
# brightness_command = 'xrandr --output LVDS-1 --brightness '
# brightness_command = 'xrandr --output VGA-1-2 --brightness '
maxx = 255 # max for R,G,B values
kill = False # to kill threads



def command(comm):
    try:
        return ''.join(os.popen("timeout 1 " + comm + " 2>&1").readlines()) # Execute command in shell
    except:
        traceback.print_exc(); return None

def constrain(val, i,j): # Constraining Function
    if val < i: return i
    if val > j: return j
    return val

last_avg = 0.2 # variable stores value of last loop average

class Controller(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global bmin,bmax,offset,kill,maxx,last_avg,filter_weight
        print('Starting Controller')
        while True :
            try:
                time.sleep(0.05) # Add delay to avoid takinh too much processing power (default 50ms )
                if kill :
                    print('Exiting', ins())
                    os._exit(0)
                # t1 = time.time()
                with mss() as sct:
                    # Get rid of the first, as it represents the "All in One" monitor:
                    for monitor in sct.monitors[1:]:
                        # Get raw pixels from the screen
                        img = sct.grab(monitor) # Puts screenshot into variable
                        imn = numpy.array(img) # Converts image data to numpy array for faster processing
                        summ = imn.sum(axis=1).sum(axis=0) # Sums up the (width*height*3) sized array into 3 : RGB array
                        r,g,b = 0,0,0
                        xx,yy = img.size[0], img.size[1] # get width and height of screen
                        xy = xx*yy # get pixel area
                        r = summ[0]/xy
                        g = summ[1]/xy
                        b = summ[2]/xy
                        # print(r,g,b
                        avg = offset+1-(float(r+g+b)/float(maxx*3)) # get average of R,G,B
                        avg = constrain(round(((( 1 - filter_weight ) * avg) + ( filter_weight * last_avg)), 3), bmin, bmax) # apply low pass filter,  constrain into set limits and round
                        # print(avg
                        if abs(avg-last_avg) > 0.04 : command(brightness_command + str(avg)) # Excutes command for setting brightness only when diff between current and last frame > 2%
                        last_avg = avg # stores this frame's average
            except :
                traceback.print_exc()


class Input(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global offset, kill, p3
        print('Ready for input')
        while True:
            try:
                if kill:
                    print("Exiting", ins())
                    os._exit(0)
                st = ''
                st = raw_input() if not p3 else input() # for raw string input
                print('st:', st)
                offset += (float(st.count('+')) - float(st.count('-')))/50 # offset changes proportionally to number of plus / minus found (2% per count)
                offset = round(constrain(offset,-1, 1),3) # constraints offset to limits
                if st.lower() == 'exit' : # exit
                    kill = True
                    print('Exiting', ins())
                    os._exit(0)
                print('Curr offset ' , offset)
            except :
                traceback.print_exc()

try :
    if __name__ == '__main__':
        a = Controller()
        b = Input()
        a.start()
        b.start()
except :
    traceback.print_exc()

print('here')
while True:
    try :
        time.sleep(1)
    except KeyboardInterrupt as e:
        kill = True
        print("Exiting", ins())
        os._exit(0)
    except :
        traceback.print_exc()
