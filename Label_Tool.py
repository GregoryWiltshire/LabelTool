import glob,os
from PyPDF2 import PdfFileMerger, PdfFileReader


group = glob.glob('*.pdf')
merger = PdfFileMerger()
for pdf in group:
    page = PdfFileReader(pdf,"rd") 

    #merger.append(page)
    merger.append(page)

merger.write("dingus.pdf")


   
    


   
