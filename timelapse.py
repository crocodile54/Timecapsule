from guizero import App, PushButton, Slider, Text, ButtonGroup, Picture, Combo, TextBox
from time import sleep
from threading import Thread
from mote import Mote
from picamera import PiCamera
from PIL import Image

cam = PiCamera()
mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)
mote.clear()
mote.show()
running = False
brightness = 0
tbp = 3600
r = 1
b = 1
g = 1

def set_motes():
    global r
    global b
    global g
    global brightness
    if colour.value=="white":
        r = 1
        b = 1
        g = 1
    if colour.value=="green":
        r = 0
        b = 0
        g = 1
    if colour.value=="red":
        r = 1
        b = 0
        g = 0
    if colour.value=="blue":
        r = 0
        b = 1
        g = 0
    if colour.value=="yellow":
        r = 1
        b = 0
        g = 1
    if colour.value=="pink":
        r = 1
        b = 1
        g = 0
    r=r*int(brightness)
    g=g*int(brightness)
    b=b*int(brightness)
    print(r,g,b)
    for channel in range(4):
        for pixel in range(16):
            mote.set_pixel(channel + 1, pixel, r, g, b)
        sleep(0.01)
    mote.show()

def thread_starting():
    global running
    running = True
    t = Thread(target=starttimelapse2)
    t.start()

def previewstart():
    global picture
    picture.hide()
    cam.capture("preview.jpg")
    im = Image.open("preview.jpg")
    im.thumbnail((240,180),Image.ANTIALIAS)
    im.save('arse.png')
    picture = Picture(app, image="arse.png", grid=[0,4])
    picture.height= 180
    picture.width = 240
    picture.show()



def starttimelapse2():
    no = 1
    global tbp
    global running
    global picture
    global button
    global r
    global g
    global b
    global brightness
    print('Time Lapse Has Started!')
##    cam.start_preview()
    sleep(2)
    cam.capture("warmup.jpg")
    endbutton.enable()
    button.disable()
    previewbutton.disable()
    while running:
        picture.hide()
        set_motes()
        sleep(0.5)
        filename = str(filename_choice.value) + str(no).zfill(4) + (".jpg")
        filename_choice.disable()
        cam.iso = 100
        # Wait for the automatic gain control to settle
        sleep(2)
        # Now fix the values
        cam.shutter_speed = cam.exposure_speed
        cam.exposure_mode = 'off'
        g = cam.awb_gains
        cam.awb_mode = 'off'
        cam.awb_gains = g
        cam.capture(filename)
        print(tbp)
        print('Captured %s' % filename)
        im = Image.open(filename)
        im.thumbnail((240,180),Image.ANTIALIAS)
        im.save('arse.png')
        picture = Picture(app, image="arse.png", grid=[0,4])
        picture.height= 180
        picture.width = 240
        picture.show()
        no = no+1
        sleep(0.1)
        mote.clear()
        mote.show()
        sleep(tbp)


    

def finishtimelapse():
    global running
    print('Time Lapse Has Ended!')
    running = False
    button.enable()
    previewbutton.enable()
    filename_choice.enable()

def bright(value):
    global brightness
    brightness = value
    #print('Brightness is now: '+ str (brightness))
    set_motes()
    
def space(value):
    global tbp
    #print('space between is ' + str(int (value)*int (choice.value)) + 'seconds')
    tbp = (int (value)*int (choice.value))

def colour():
    global r
    global b
    global g
    #global brightness
    # print('colour is ' + str(colour.value))
    #r=r*int(brightness)
    #g=g*int(brightness)
    #b=b*int(brightness)
    set_motes()



app = App(title="Ozzy's TimeLapse Booth", height=500, width=700, layout="grid")

messager = Text(app, text="Brightness =", grid=[0,1])

slider = Slider(app, grid=[1,2], end="60", command=space)
slider.width= 150
slider.text_color = "red"
choice = ButtonGroup(app, options=[["seconds",1], ["minutes",60], ["hours",3600]], selected=1, grid=[0,2])

brightnessslider = Slider(app, grid=[1,1], end="255", command=bright)
brightnessslider.width=150


button = PushButton(app, command=thread_starting, text="Start", grid=[1,3])
button.bg = 'green'

endbutton = PushButton(app, command=finishtimelapse, text="End", grid=[3,3])
endbutton.bg = 'red'

filename_choice = TextBox(app, text = "Filename", grid=[1,4])

picture = Picture(app, image="arse.png", grid=[0,4])
picture.height= 180
picture.width = 240

colour = Combo(app, options=["white", "green", "red", "blue", "yellow", "pink"], selected="white", grid=[2,1], command=set_motes)

previewbutton = PushButton(app, text="Preview",command=previewstart, grid=[2,3])

endbutton.disable()
app.display()
