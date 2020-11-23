# -*- coding: utf-8 -*-
""" Class to secure a PDF of findings. """
from typing import cast
import os
from aioextensions import (
    in_process,
)
from fpdf import FPDF
from PyPDF4 import PdfFileWriter, PdfFileReader
from backend.dal import project as project_dal
from backend.typing import Historic


# Constants
STARDIR = os.environ['STARTDIR']


class PDF(FPDF):  # type: ignore
    user = ''

    def set_user(self, user: str) -> None:
        self.user = user

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font('Times', '', 12)
        self.cell(0, 10, 'Only for %s' % self.user, 0, 0, align='L')
        self.cell(0, 10, 'Page %s' % str(
            int(self.page_no()) - 1), 0, 0, align='R')


class SecurePDF():
    """ Add basic security to PDF. """
    # pylint: disable=too-many-instance-attributes
    # eight arguments are reasonable (pylnt limit -> 7)
    result_dir = ''
    watermark_tpl = ''
    footer_tpl = ''
    secure_pdf_username = ''
    secure_pdf_usermail = ''
    secure_pdf_filename = ''
    passphrase = ''

    def __init__(self, passphrase: str):
        """Class constructor."""
        self.base = (
            f'{STARDIR}/integrates/backend_new/packages/'
            'integrates-back/backend/reports'
        )

        self.watermark_tpl = os.path.join(
            self.base,
            'resources/themes/watermark_integrates_en.pdf')
        self.footer_tpl = os.path.join(
            self.base,
            'resources/themes/overlay_footer.pdf')
        self.result_dir = os.path.join(self.base, 'results/results_pdf/')
        self.passphrase = passphrase

    async def create_full(
        self,
        usermail: str,
        basic_pdf_name: str,
        project: str
    ) -> str:
        """ Execute the security process in a PDF. """
        self.secure_pdf_usermail = usermail
        self.secure_pdf_username = usermail.split('@')[0]
        project_info = await project_dal.get_attributes(
            project.lower(), ['historic_configuration']
        )
        historic_configuration = cast(
            Historic, project_info.get('historic_configuration', [{}])
        )
        if (project_info and
                historic_configuration[-1].get('type') == 'continuous'):
            self.secure_pdf_filename = await in_process(
                self.lock, basic_pdf_name
            )
        else:
            water_pdf_name = await in_process(
                self.overlays, basic_pdf_name
            )
            self.secure_pdf_filename = await in_process(
                self.lock, water_pdf_name
            )
        return self.result_dir + self.secure_pdf_filename

    def overlays(self, in_filename: str) -> str:
        """ Add watermark and footer to all pages of a PDF. """
        pdf_foutname = 'water_' + in_filename
        footer_pdf = PDF()
        footer_pdf.set_user(self.secure_pdf_usermail)
        footer_pdf.alias_nb_pages()
        input = PdfFileReader(open(self.result_dir + in_filename, 'rb')) # noqa
        for i in range(1, input.getNumPages()):
            footer_pdf.add_page()
        footer_pdf.add_page()
        footer_pdf.output(self.footer_tpl)
        footer_pdf.close()
        output = PdfFileWriter()
        overlay_watermark = PdfFileReader(open(self.watermark_tpl, 'rb'))
        overlay_footer = PdfFileReader(open(self.footer_tpl, 'rb'))
        for i in range(0, input.getNumPages()):
            page = input.getPage(i)
            page.mergePage(overlay_watermark.getPage(0))
            if i != 0:
                page.mergePage(overlay_footer.getPage(i))
            output.addPage(page)
        output_stream = open(self.result_dir + pdf_foutname, 'wb')
        output.write(output_stream)
        output_stream.close()
        return pdf_foutname

    def lock(self, in_filename: str) -> str:
        """  Add a passphrase to a PDF. """
        pdf_foutname = self.secure_pdf_username + '_' + in_filename
        output = PdfFileWriter()
        input = PdfFileReader(open(self.result_dir + in_filename, 'rb')) # noqa
        for i in range(0, input.getNumPages()):
            output.addPage(input.getPage(i))
        output_stream = open(self.result_dir + pdf_foutname, 'wb')
        output.encrypt(self.passphrase, use_128bit=True)
        output.write(output_stream)
        output_stream.close()
        return pdf_foutname
