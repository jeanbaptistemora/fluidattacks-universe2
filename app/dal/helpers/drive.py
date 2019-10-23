# -*- coding: utf-8 -*-
"""Integrates Google Drive API."""


import io
import logging
import os
import httplib2
import rollbar
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload, HttpError  # pylint: disable=import-error
from oauth2client import client, tools
from oauth2client.file import Storage
from django.conf import settings

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class DriveAPI():
    """Class to consume the Google Drive API."""

    scopes = []
    client_secret_file = ""
    client_author_file = ""
    application_name = ""
    FILE = None

    def __init__(self):
        """ Class constructor """
        self.scopes = settings.DRIVE_SCOPES
        self.client_secret_file = settings.DRIVE_SECRET_FILE
        self.client_author_file = settings.DRIVE_AUTHOR_FILE
        self.application_name = settings.DRIVE_APP_NAME

    def download(self, drive_file_id=""):
        """ Download files from Google Drive in /tmp/. """
        filename = "/tmp/:id.tmp".replace(":id", drive_file_id)
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v3', http=http)
        request = drive_service.files().get_media(fileId=drive_file_id)
        fh_fd = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh_fd, request)
        done = False
        try:
            while not done:
                _, done = downloader.next_chunk(num_retries=3)

            fh_fd.flush()
            os.fsync(fh_fd)
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
        fh_fd = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh_fd, request)
        done = False
        try:
            while not done:
                _, done = downloader.next_chunk(num_retries=3)

            fh_fd.flush()
            os.fsync(fh_fd)
        except HttpError:
            rollbar.report_message('Error: Unable to download the image', 'error')

    def get_credentials(self):
        """ Gets the credentials to authenticate in the API. """
        store = Storage(self.client_author_file)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.client_secret_file,
                self.scopes
            )
            flow.user_agent = self.application_name
            credentials = tools.run_flow(flow, store)
        return credentials
