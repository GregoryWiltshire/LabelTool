import glob
from PyPDF2 import PdfFileReader, PdfFileWriter
#PDFs use units of 1/72in and their origin is at the bottom left
unitconstant =  (1.0/72.2545)
bottomy =       (6.35 / unitconstant)
leftxoffset  =  (1.69 / unitconstant)
topyoffset =    (10.30 / unitconstant)
rightxoffset =  (6.88 / unitconstant)
#get all the pdf files in the directory
group = glob.glob('*.pdf')
for pdf in group:
    pdfWriter = PdfFileWriter()
    input = PdfFileReader(open(pdf, 'rb')).getPage(0)
    cropbox = input.cropBox
    cropbox.upperLeft = (leftxoffset,topyoffset)
    cropbox.lowerLeft = (leftxoffset,bottomy)
    cropbox.upperRight = (rightxoffset,topyoffset)
    cropbox.lowerRight = (rightxoffset,bottomy)
    pdfWriter.addPage(input)
    with open("cropped"+pdf, "wb") as outputStream:
        pdfWriter.write(outputStream)
