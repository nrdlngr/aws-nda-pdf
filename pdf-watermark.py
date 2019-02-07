#!/usr/bin/env python
import PyPDF2
import sys
import os

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

resultPdfFileName = 'nda-' + inputFileName

resultPdfFile = open(resultPdfFileName, 'wb')
pdfWriter.write(resultPdfFile)
inputPDF.close()
resultPdfFile.close()