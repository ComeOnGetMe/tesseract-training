# Tesseract 3.02 Font Trainer
# V0.01 - 3/04/2013

# Complete the documentation 
import time
import os
from sys import argv
fontname = '9p'
language = 'mon'
directory = "./"

print 'Tesseract Font Builder'
print 'Assumes font_properties, training TIFFs and boxfiles already created'
print 'Note: Only up to 32 .tiff files are supported for training purposes'
count = 0
for files in os.listdir(directory):
    
    if files.endswith(".tif"):
        #Train the boxfiles
        command = 'tesseract {0}.{1}.exp{2}.tif {0}.{1}exp{2} nobatch box.train.stderr'.format(language, fontname, count)
        print '-----------------------\n' + command + '-----------------------\n'
        os.system(command)
        count = count + 1

trfilelist = ''
boxfilelist = ''
font_properties = ''

trfilelist = ' '.join([files for files in os.listdir(directory) if files.endswith('.tr')])
boxfilelist = ' '.join([files for files in os.listdir(directory) if files.endswith('.box')])

#Build the Unicharset File
command2 = 'unicharset_extractor ' + boxfilelist
print '-----------------------\n' + command2 + '-----------------------\n'
os.system(command2)

#Build the font properties file
# fontpropertiesfile = open('font_properties', 'a+') # saving into a file        
# fontpropertiesfile.write(font_properties)
# print 'Wrote font_properties file'
# fontpropertiesfile.close()

# #Clustering
command3 = 'shapeclustering -F font_properties -U unicharset ' + trfilelist
print '-----------------------\n' + command3 + '-----------------------\n'
os.system(command3)

#MFTraining
mftraining = 'mftraining -F font_properties -U unicharset -O '+ language +'.charset '+trfilelist
print '-----------------------\n' + mftraining + '-----------------------\n'
os.system(mftraining)

#CNTraining
command4 = 'cntraining ' + trfilelist
print '-----------------------\n' + command4 + '-----------------------\n'
os.system(command4)

#Rename necessary files
os.system('mv unicharset '+language+'.unicharset')
os.system('mv shapetable '+language+'.shapetable')
os.system('mv normproto '+language+'.normproto')
os.system('mv pffmtable '+language+'.pffmtable')
os.system('mv inttemp '+language+'.inttemp')
##Put it all together
command5 = 'combine_tessdata '+language+'.'
os.system(command5)

#Copy it over
# Don't forget to copy language.traineddata to your tessdata repo!
