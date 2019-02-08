#!/usr/bin/env python
import PyPDF2
import sys
import os
import argparse

usage_description = '''Adds the standard AWS NDA language footer and a "CONFIDENTIAL" watermark to PDFs.

The output file is named nda-<pdf_file> and is saved to the present working directory.'''

parser = argparse.ArgumentParser(description=usage_description)
parser.add_argument('pdf_file', nargs=1, help='The path to the PDF file to watermark.')
args = parser.parse_args()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

inputFileName = sys.argv[1]

watermark_path = resource_path('img/blank-nda.pdf')

inputPDF = open(inputFileName, 'rb')
pdfReader = PyPDF2.PdfFileReader(inputPDF)
pdfWatermarkReader = PyPDF2.PdfFileReader(open(watermark_path, 'rb'))
pdfWriter = PyPDF2.PdfFileWriter()

for pageNum in range(0, pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    pageObj.mergePage(pdfWatermarkReader.getPage(0))
    pdfWriter.addPage(pageObj)

resultPdfFileName = 'nda-' + os.path.basename(inputFileName)


resultPdfFile = open(resultPdfFileName, 'wb')
pdfWriter.write(resultPdfFile)
inputPDF.close()
resultPdfFile.close()