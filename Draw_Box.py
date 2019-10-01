import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from pathlib import Path
from generate_xml import write_xml

# global constant
img = None
top_left_list = []
bottom_right_list = []
object_list = []
obj='Player'
def line_select_callback(click,release):
    global top_left_list
    global bottom_right_list
    global object_list
    object_list.append(obj)
    top_left_list.append(((int(click.xdata),int(click.ydata))))
    bottom_right_list.append(((int(release.xdata),int(release.ydata))))
    print(f'object_list: {object_list}')
    print(f'top_left_list: {top_left_list}')
    print(f'bottom_right_list: {bottom_right_list}')

def object_change(event):
    global obj
    global object_list
    global top_left_list
    global bottom_right_list
    if event.key == 'f':
        print('------------------------->Football')
        obj='Football'
    if event.key == 'r':
        print('------------------------->Referee')
        obj='Referee'
    if event.key =='d':
        print('------------------------->Goalpost')
        obj='Goalpost'
    if event.key == 'w':
        print('------------------------->Player')
        obj='Player'
    if event.key == 's':
        print('------------------------->Holding the ball')
        obj='Holding the ball'
    if event.key == 'a':
        object_list=object_list[:-1]
        top_left_list=top_left_list[:-1]
        bottom_right_list =bottom_right_list[:-1]
        print(f'object_list: {object_list}')
        print(f'top_left_list: {top_left_list}')
        print(f'bottom_right_list: {bottom_right_list}')

def onkeypress(event):
    global object_list 
    global top_left_list
    global bottom_right_list
    global img
    if event.key == 'q':
        print(top_left_list,bottom_right_list)
        write_xml(image_folder, path, object_list, top_left_list, bottom_right_list, savedir) 
        top_left_list = []
        bottom_right_list = []
        object_list = []
        plt.close()

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

# constants
folder_name = input('What is your part?')
image_folder = f'images/{folder_name}_Gray'
savedir = 'ann'
path_list = sorted(Path(image_folder).glob('*.png'))
if __name__=='__main__':
    for i,path in enumerate(path_list):
        fig, ax = plt.subplots(1)
        image = cv2.imread(str(path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print('File name: ',str(path.name),f' Progress: {i+1}/{len(path_list)}')
        plt.imshow(image)

        toggle_selector.RS = RectangleSelector(
        ax,line_select_callback,
        drawtype='box',useblit=True,
        button=[1],minspanx=5,minspany=5,
        spancoords='pixels',interactive=True
        )
        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event',onkeypress)
        OBJ = plt.connect('key_press_event',object_change)
        plt.show()