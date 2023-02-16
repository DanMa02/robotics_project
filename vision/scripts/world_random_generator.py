# -*- coding: utf-8 -*-
"""
Created on 3 May  2022

@author: mfocchi
"""

from __future__ import print_function

import os
import rospkg

# import for world changes
import random
import xml.etree.ElementTree as ET
WORLD_DIR = rospkg.RosPack().get_path('ros_impedance_controller') + '/worlds/'

LEGO_NAMES = [  'X1-Y1-Z2',
                'X1-Y2-Z1',
                'X1-Y2-Z2',
                'X1-Y2-Z2-CHAMFER',
                'X1-Y2-Z2-TWINFILLET',
                'X1-Y3-Z2',
                'X1-Y3-Z2-FILLET',
                'X1-Y4-Z1',
                'X1-Y4-Z2',
                'X2-Y2-Z2',
                'X2-Y2-Z2-FILLET']

#world random generator

def changeposition (myroot):
    counter = 0  # counter for the number of iterations
    listposition = []; # list of the position of the objects
    # iterating through the price values.
    for position in myroot.iter('pose'):
        #do noting on the first and second iteration
        if counter < 2:
            counter = counter + 1
            continue
        print("old:"+position.text)
        # create new random position
        new_position = str(round(random.uniform(0, 0.5), 2)) + ' ' + str(round(random.uniform(0.2, 0.8), 2)) + ' ' + '0.9' + ' 0 0 0'
        while (checkposition(new_position, listposition)):
            new_position = str(round(random.uniform(0, 0.5), 2)) + ' ' + str(round(random.uniform(0.2, 0.8), 2)) + ' ' + '0.9' + ' 0 0 0'

        position.text = new_position        
        listposition.append(position.text)
        counter = counter + 1
        print(position.text)
    print("array:")
    print(listposition)  

def changeblock (myroot):
    counter = 0  # counter for the number of iterations
    listposition = []; # list of the position of the objects
    # iterating through the price values.
    for block_name in myroot.iter('uri'):
        #do nothing on first 3 iterations
        if counter < 3:
            counter = counter + 1
            continue
        new_block = random.choice(LEGO_NAMES)
        block_name.text = 'model://' + new_block
        print(block_name.text)



def checkposition(actpose, listposition):
    print ("check")
    for pose in listposition:
        if (actpose==pose):
            return True
        else:
            return False

if __name__ == '__main__':

    #get user input

    number = int(input("Enter numer of blocks: "))

    #cases from 1 to 11
    if number == 1:
        mytree = ET.parse(WORLD_DIR+'legopiece1.world')
        myroot = mytree.getroot()
        changeposition(myroot)
        choice = int(input("Change bocks? 1 for yes, 0 for no: "))
        if choice == 1:
            changeblock(myroot)
        #apply the changes
        mytree.write(WORLD_DIR+'legopiece1.world')
        #self.world_name = 'legopiece1.world'
    elif number == 2:
        mytree = ET.parse(WORLD_DIR+'legopiece2.world')
        myroot = mytree.getroot()
        changeposition(myroot)
        choice = int(input("Change bocks? 1 for yes, 0 for no: "))
        if choice == 1:
            changeblock(myroot)
        #apply the changes
        mytree.write(WORLD_DIR+'legopiece2.world')
        #self.world_name = 'legopiece2.world'
        
    elif number == 3:
        mytree = ET.parse(WORLD_DIR+'legopiece3.world')
        myroot = mytree.getroot()
        changeposition(myroot)
        choice = int(input("Change bocks? 1 for yes, 0 for no: "))
        if choice == 1:
            changeblock(myroot)
        #apply the changes
        mytree.write(WORLD_DIR+'legopiece3.world')
        #self.world_name = 'legopiece3.world'
        '''
    elif number == 4:

    elif number == 5:

    elif number == 6:

    elif number == 7:

    elif number == 8:

    elif number == 9:

    elif number == 10:

    elif number == 11: 
        '''


    #os.system("cd ~/ros_ws; catkin_make install; source devel/setup.bash")
    #self.world_name = 'lego.world'
    #self.world_name = None # only the workbench
    #self.world_name = 'empty.world'
    #self.world_name = 'palopoli.world'

    print("Initialized ur5 generic  controller---------------------------------------------------------------")

    
        