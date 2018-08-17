from PyPDF2 import PdfFileReader, PdfFileWriter
import io, os, glob
import re
import tempfile
import uuid

from io import BytesIO
from subprocess import Popen, PIPE
from PIL import Image


def __parse_buffer_to_png(data):
    images = []

    index = 0

    while index < len(data):
        file_size = data[index:].index(b'IEND') + 8 # 4 bytes for IEND + 4 bytes for CRC
        images.append(Image.open(BytesIO(data[index:index+file_size])))
        index += file_size

    return images


def __parse_format(fmt):
    if fmt[0] == '.':
        fmt = fmt[1:]
    if fmt == 'jpeg' or fmt == 'jpg':
        return 'jpeg', __parse_buffer_to_jpeg
    if fmt == 'png':
        return 'png', __parse_buffer_to_png
    # Unable to parse the format so we'll use the default
    return 'ppm', __parse_buffer_to_ppm


def __build_command(args, output_folder, first_page, last_page, fmt, uid, userpw):
    if first_page is not None:
        args.extend(['-f', str(first_page)])

    if last_page is not None:
        args.extend(['-l', str(last_page)])

    parsed_format, parse_buffer_func = __parse_format(fmt)

    if parsed_format != 'ppm':
        args.append('-' + parsed_format)

    if output_folder is not None:
        args.append(os.path.join(output_folder, uid))

    if userpw is not None:
        args.extend(['-upw', userpw])

    return args, parse_buffer_func

def convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_path -> Path to the PDF that you want to convert
            dpi -> Image quality in DPI (default 200)
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
            first_page -> First page to process
            last_page -> Last page to process before stopping
            fmt -> Output image format
            thread_count -> How many threads we are allowed to spawn for processing
            userpw -> PDF's password
    """

    page_count = 1

    if thread_count < 1:
        thread_count = 1

    if first_page is None:
        first_page = 1

    if last_page is None or last_page > page_count:
        last_page = page_count

    # Recalculate page count based on first and last page
    page_count = last_page - first_page + 1

    if thread_count > page_count:
        thread_count = page_count

    reminder = page_count % thread_count
    current_page = first_page
    processes = []
    for _ in range(thread_count):
        # A unique identifier for our files if the directory is not empty
        uid = str(uuid.uuid4())
        # Get the number of pages the thread will be processing
        thread_page_count = page_count // thread_count + int(reminder > 0)
        # Build the command accordingly
        args, parse_buffer_func = __build_command(['pdftoppm', '-r', str(dpi), pdf_path], output_folder, current_page, current_page + thread_page_count - 1, fmt, uid, userpw)
        # Update page values
        current_page = current_page + thread_page_count
        reminder -= int(reminder > 0)
        # Spawn the process and save its uuid
        processes.append((uid, Popen(args, stdout=PIPE, stderr=PIPE)))

    images = []
    for uid, proc in processes:
        data, _ = proc.communicate()

        if output_folder is not None:
            images += __load_from_output_folder(output_folder, uid)
        else:
            images += parse_buffer_func(data)

    return images

def __load_from_output_folder(output_folder, uid):
    return [Image.open(os.path.join(output_folder, f)) for f in sorted(os.listdir(output_folder)) if uid in f]

def convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_file -> Bytes representing the PDF file
            dpi -> Image quality in DPI
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
            first_page -> First page to process
            last_page -> Last page to process before stopping
            fmt -> Output image format
            thread_count -> How many threads we are allowed to spawn for processing
            userpw -> PDF's password
    """

    with tempfile.NamedTemporaryFile('wb') as f:
        f.write(pdf_file)
        f.flush()
        return convert_from_path(f.name, dpi=dpi, output_folder=output_folder, first_page=first_page, last_page=last_page, fmt=fmt, thread_count=thread_count, userpw=userpw)

def __parse_buffer_to_png(data):
    images = []

    index = 0

    while index < len(data):
        file_size = data[index:].index(b'IEND') + 8 # 4 bytes for IEND + 4 bytes for CRC
        images.append(Image.open(BytesIO(data[index:index+file_size])))
        index += file_size

    return images


# Main
# ====
#PDFs use units of 1/72in and their origin is at the bottom left
unitconstant =  (1.0/72.2545)
bottomy =       (6.35 / unitconstant)
leftxoffset  =  (1.69 / unitconstant)
topyoffset =    (10.30 / unitconstant)
rightxoffset =  (6.88 / unitconstant)
#get all the pdf files in the directory
group = glob.glob('*.pdf')
for pdf in group:
    #pdfWriter = PdfFileWriter()
    # input = PdfFileReader(open(pdf, 'rb')).getPage(0)
    # cropbox = input.cropBox
    # cropbox.upperLeft = (leftxoffset,topyoffset)
    # cropbox.lowerLeft = (leftxoffset,bottomy)
    # cropbox.upperRight = (rightxoffset,topyoffset)
    # cropbox.lowerRight = (rightxoffset,bottomy)
    # pdfWriter.addPage(input)
    # with open(pdf, "wb") as outputStream:
    #     pdfWriter.write(outputStream)
    print(os.path.splitext(os.path.basename(pdf))[0])

    convert_from_path(pdf, dpi=300, output_folder="E:\Label_Tool", first_page=None, last_page=None, fmt='png', thread_count=1, userpw=None)
    
#test_img = Image.open("Capture.JPG")
#test_img.show()

image_group = glob.glob('*.png')
for element in image_group:
    imageObj = Image.open(element,mode='r')
    imageObj.

 
   
    



    
  