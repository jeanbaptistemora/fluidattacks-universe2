# -*- coding: utf-8 -*-
""" Integrates Google Drive API """

from __future__ import print_function
import httplib2
import io
from magic import Magic
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from django.conf import settings

from apiclient.http import MediaIoBaseDownload # pylint: disable=import-error
from apiclient.http import HttpError # pylint: disable=import-error

class DriveAPI(object):
    """ Clase para consumir la API de Google Drive """

    SCOPES = []
    CLIENT_SECRET_FILE = ""
    CLIENT_AUTHOR_FILE = ""
    APPLICATION_NAME = ""
    FILE = None

    def __init__(self, drive_file_id = ""):
        """ Constructor de la clase """

        self.SCOPES = settings.DRIVE_SCOPES
        self.CLIENT_SECRET_FILE = settings.DRIVE_SECRET_FILE
        self.CLIENT_AUTHOR_FILE = settings.DRIVE_AUTHOR_FILE
        self.APPLICATION_NAME = settings.DRIVE_APP_NAME
        if(drive_file_id != ""):
            self.FILE = self.download(drive_file_id)

    def download(self, drive_file_id = ""):
        """ Descarga los archivos de google drive en /tmp/ """
        filename = "/tmp/:id.tmp".replace(":id", drive_file_id)
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        file_id = drive_file_id
        drive_service = discovery.build('drive', 'v3', http=http)
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            try:
                status, done = downloader.next_chunk()# pylint: disable=unused-variable                
            except HttpError:
                pass
        if done:
            mime = Magic(mime=True)
            mime_type = mime.from_file(filename)
            if mime_type in ["image/png", "image/jpeg", "image/gif", "text/x-c", "text/x-python", "text/plain", "text/html"]:
                return fh
        return None

    def download_images(self, drive_file_id = ""):
        """ Descarga los archivos de google drive en /tmp/ """
        hard_path = "/usr/src/app/app/documentator/images/"
        filename = hard_path + ":id.png".replace(":id", drive_file_id)
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        file_id = drive_file_id
        drive_service = discovery.build('drive', 'v3', http=http)
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            try:
                status, done = downloader.next_chunk()# pylint: disable=unused-variable                
            except HttpError:
                pass
        if done:
            mime = Magic(mime=True)
            mime_type = mime.from_file(filename)
            if mime_type in ["image/png", "image/jpeg", "image/gif"]:
                return fh
        return None

    def get_credentials(self):
        """ Obtiene las credenciales para autenticar la API """
        
        store = Storage(self.CLIENT_AUTHOR_FILE)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.CLIENT_SECRET_FILE, 
                self.SCOPES
            )
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store)
        return credentials
