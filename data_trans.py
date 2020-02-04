# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:22:10 2020

@author: luzgin
"""
import shutil # delete the main folder and sub-folders
import glob # for get list of files
import json # for reading json files
from PIL import Image
import os
import progressbar

# the number of images
#n = 500

# source folder with images
s_img_folder='source/dataset/'
# source folder with annotation
s_lab_folder='source/data/'

# main folder
data_folder = 'data/'
# delete the main folder and sub-folders
if os.path.exists(data_folder):
        shutil.rmtree(data_folder)
# create the main data folder
if not os.path.exists(data_folder):
    os.makedirs(name=data_folder,exist_ok = True)
# create sub-folders
img_folder=data_folder+'images/'
if not os.path.exists(img_folder):
    os.makedirs(name=img_folder,exist_ok = True)
lab_folder=data_folder+'labels/'
if not os.path.exists(lab_folder):
    os.makedirs(name=lab_folder,exist_ok = True)
    
# get list of file names without extantion
list_img_files=glob.glob(s_img_folder+'*.jpg')#[:n]
# print(list_img_files)  

# the main cycle. here we create the numpy array with structured information
main_table = list()
class_names = list()
# main cycle
pb = 0 # progress bar
#max_size = 256
with progressbar.ProgressBar(max_value=len(list_img_files)) as bar:
    for i in range(len(list_img_files)):
        # load annotation
        json_file = s_lab_folder+os.path.splitext(os.path.basename(list_img_files[i]))[0]+'.json'
        txt_file = lab_folder+os.path.splitext(os.path.basename(list_img_files[i]))[0]+'.txt'
        out_img_file = img_folder+os.path.splitext(os.path.basename(list_img_files[i]))[0]+'.jpg'
        # load image
        img = Image.open(list_img_files[i])
        if img.getbands()[0] == 'L':
            img = img.convert('RGB')        
        #c_img = img.resize((416,416))
        shutil.copyfile(list_img_files[i],out_img_file)        
        #c_img.save(out_img_file,'JPEG')
        # print(json_file)
        with open(json_file) as json_file:
            json_data = json.load(json_file)
            # create label file 
            label_data = list()
            for j in range(len(json_data['arr_boxes'])):
                # get coordinates and class
                x = int(json_data['arr_boxes'][j]['x'])
                y = int(json_data['arr_boxes'][j]['y'])
                w = int(json_data['arr_boxes'][j]['width'])
                h = int(json_data['arr_boxes'][j]['height'])
                class_lab = str(json_data['arr_boxes'][j]['class']) 
                # correction proportions
                if (x+w)>img.size[0]:
                    #print("Error w:{}!".format(img.size[0]-x-w))
                    w=img.size[0]-x
                if (y+h)>img.size[1]:
                    #print("Error h:{}!".format(img.size[1]-y-h))
                    h=img.size[1]-y
                # get proportions
                x = (x+0.5*w)/img.size[0]
                y = (y+0.5*h)/img.size[1]
                w = w/img.size[0]
                h = h/img.size[1]
                if  not class_lab in class_names:
                    class_names.append(class_lab)
                label_data.append([class_names.index(class_lab),x,y,w,h])
            #print(label_data)
            # save to file the label data
            with open(txt_file, 'w') as f:
                for item in label_data:
                    item = str(item)
                    item = item.replace(']','')
                    item = item.replace('[','')
                    item = item.replace(',','')
                    f.write(str(item)+'\n')
        bar.update(pb)
        pb+=1
# save coco names file
with open(data_folder+'classes.names', 'w', encoding="utf-8") as f:
    for item in class_names:
        item = str(item)
        f.write(str(item)+'\n')
f.close()
# save number classes
with open(data_folder+'classes.n', 'w', encoding="utf-8") as f:
    f.write(str(len(class_names))+'\n')        
f.close()



