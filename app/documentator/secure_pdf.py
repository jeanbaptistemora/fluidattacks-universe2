# -*- coding: utf-8 -*-
""" Class to secure a PDF of findings. """
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.
import time
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from ..dal import integrates_dal


class SecurePDF():
    """ Add basic security to PDF. """

    result_dir = ''
    watermark_tpl = ''
    secure_pdf_username = ''
    secure_pdf_filename = ''

    def __init__(self):
        """Class constructor."""
        self.base = '/usr/src/app/app/documentator/'
        self.watermark_tpl = os.path.join(
            self.base,
            'resources/themes/watermark_integrates_en.pdf')
        self.result_dir = os.path.join(self.base, 'results/')

    def create_full(self, username, basic_pdf_name, project):
        """ Execute the security process in a PDF. """
        self.secure_pdf_username = username
        project_info = integrates_dal.get_project_dynamo(project.lower())
        if project_info and project_info[0].get('type') == 'continuous':
            self.secure_pdf_filename = self.lock(basic_pdf_name)
        else:
            water_pdf_name = self.watermark(basic_pdf_name)
            self.secure_pdf_filename = self.lock(water_pdf_name)
        return self.result_dir + self.secure_pdf_filename

    def watermark(self, in_filename):
        """ Add a watermark to all pages of a PDF. """
        pdf_foutname = 'water_' + in_filename
        input = PdfFileReader(open(self.result_dir + in_filename, 'rb')) # noqa
        output = PdfFileWriter()
        watermark = PdfFileReader(open(self.watermark_tpl, 'rb'))
        for i in range(0, input.getNumPages()):
            overlay = watermark.getPage(0)
            page = input.getPage(i)
            page.mergePage(overlay)
            output.addPage(page)
        output_stream = open(self.result_dir + pdf_foutname, 'wb')
        output.write(output_stream)
        output_stream.close()
        return pdf_foutname

    def lock(self, in_filename):
        """  Add a password to a PDF. """
        pdf_foutname = self.secure_pdf_username + "_" + in_filename
        password = time.strftime('%d%m%Y') + self.secure_pdf_username
        output = PdfFileWriter()
        input = PdfFileReader(open(self.result_dir + in_filename, 'rb')) # noqa
        for i in range(0, input.getNumPages()):
            output.addPage(input.getPage(i))
        output_stream = open(self.result_dir + pdf_foutname, 'wb')
        output.encrypt(password, use_128bit=True)
        output.write(output_stream)
        output_stream.close()
        return pdf_foutname
