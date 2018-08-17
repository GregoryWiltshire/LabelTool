import os, glob, pdf2image
from PIL import Image

# Main
#set our margin to 90px
margin = 90

#create a new image, white background, size of letter paper
multiplelabels = Image.new('RGB', (2550,3301), color=(255,255,255))
#get all the pdf files in the directory
group = glob.glob('*.pdf')
croppedlabels = list()

for pdf in group:
    bytes = pdf2image.convert_from_path(pdf, dpi=300, output_folder=None, first_page=None, last_page=None, fmt='png', thread_count=1, userpw=None)
    #booty = Image.frombuffer('RGB',(2550,3301),bytes[0], decoder_name='raw')
    #bytes[0].show()
    
    #grab the first image in the list, crop
    croppedimage = bytes[0].crop((513,215,2070,1370))
    #rotate the label 90degrees CCW
    croppedimage = croppedimage.rotate(90,expand=1)
    croppedlabels.append(croppedimage)
    #delete pdfs after processing
    os.remove(pdf)

#Dimensions of our cropped labels
    X = 1155
    Y = 1557

#if we have more than 1 label, place top left and right
if(len(croppedlabels) > 1):
    multiplelabels.paste(croppedlabels.pop(),(margin,margin-10))
    multiplelabels.paste(croppedlabels.pop(),(margin + X,margin-10))
    #if we have more labels place bottom left
    if(len(croppedlabels) > 0):
        img3 = croppedlabels.pop()
        multiplelabels.paste(img3,(margin + X,margin + Y))
        #if we have more labels place bottom right
        if(len(croppedlabels) > 0):
            img4 = croppedlabels.pop()
            multiplelabels.paste(img4,(margin,margin + Y))

#multiplelabels.show()
#save in current directory as png file
multiplelabels.save(os.getcwd() + os.sep + "multiplelabels.png",format="png")