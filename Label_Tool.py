# array = {1,2,3,4}
# for x in array:
#     print (x)


import glob,os
from PyPDF2 import PdfFileMerger, PdfFileReader


group = glob.glob('*.pdf')
merger = PdfFileMerger()
for pdf in group:
    page = PdfFileReader(pdf,"rd") 

    #merger.append(page)
    merger.append(page)

merger.write("dingus.pdf")


   
    


    # for x in shit:
    #     print(x)
    #print(info.title)
    #pageObj = pdfReader.getPage(0)
    #text = pageObj.extractText()
    #text = text[-200:]
    #print(text)
  