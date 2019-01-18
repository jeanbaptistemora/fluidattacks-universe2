# -*- coding: utf-8 -*-
"""Integrates Google Drive API."""

from __future__ import print_function
import httplib2
import io
import logging
import os
import rollbar
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from django.conf import settings
from apiclient.http import MediaIoBaseDownload  # pylint: disable=import-error
from apiclient.http import HttpError  # pylint: disable=import-error

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class DriveAPI(object):
    """ Class to consume the Google Drive API. """

    SCOPES = []
    CLIENT_SECRET_FILE = ""
    CLIENT_AUTHOR_FILE = ""
    APPLICATION_NAME = ""
    FILE = None

    def __init__(self):
        """ Class constructor """
        self.SCOPES = settings.DRIVE_SCOPES
        self.CLIENT_SECRET_FILE = settings.DRIVE_SECRET_FILE
        self.CLIENT_AUTHOR_FILE = settings.DRIVE_AUTHOR_FILE
        self.APPLICATION_NAME = settings.DRIVE_APP_NAME

    def download(self, drive_file_id=""):
        """ Download files from Google Drive in /tmp/. """
        filename = "/tmp/:id.tmp".replace(":id", drive_file_id)
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http=http)
        request = drive_service.files().get_media(fileId=drive_file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        try:
            while not done:
                _, done = downloader.next_chunk(num_retries=3)

            fh.flush()
            os.fsync(fh)
            return filename
        except HttpError:
            rollbar.report_message('Error: Unable to download the file', 'error')
            return None

    def download_images(self, drive_file_id=""):
        """ Download images from Google Drive in /tmp/. """
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
        try:
            while not done:
                _, done = downloader.next_chunk(num_retries=3)

            fh.flush()
            os.fsync(fh)
        except HttpError:
            rollbar.report_message('Error: Unable to download the image', 'error')

    def get_credentials(self):
        """ Gets the credentials to authenticate in the API. """
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
