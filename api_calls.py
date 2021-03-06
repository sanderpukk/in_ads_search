"""
Manage the api address
"""

import ssl
import requests
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QTabWidget
from PyQt5.QtCore import QUrl, QUrlQuery, pyqtSignal, QEventLoop, QCoreApplication


class ApiCalls:
    def __init__(self, dialog=None):
        self.dialog = dialog
        self.search_term = ""
        self.base_url = "https://inaadress.maaamet.ee/inaadress/gazetteer"
        self.my_context = ssl._create_unverified_context()
        self.params = {}
        self.search_responses = {}
        self.search_addresses = []
        self.search_dictionary = {}

    def tr(self, message):
        return QCoreApplication.translate('InAdsSearch', message)

    def clearPreviousSearch(self):
        self.search_responses = {}
        self.search_addresses = []

    def formatResponse(self, request_data):
        self.clearPreviousSearch()
        try:
            self.search_responses = request_data.json()['addresses']
            for full_response in self.search_responses:
                taisaadress = full_response['taisaadress']
                self.search_addresses.append(taisaadress)
                self.search_dictionary[taisaadress] = full_response
        except (IndexError, KeyError, TypeError):
        # data does not have the inner structure you expect
            self.dialog.response_list.addItem("No match found")

    def displayAddress(self):
        self.dialog.response_list.clear()
        # Just to make it visually better, limiting the response display list
        if len(self.search_addresses) >= 7:
            for x in range(7):
                self.dialog.response_list.addItem(self.search_addresses[x])
        elif len(self.search_addresses) >= 1:
            self.dialog.response_list.addItems(self.search_addresses)
        else:
           self.dialog.response_list.addItem("No match found")

    def searchAddress(self, term):
        self.search_term = term
        self.params = {'address': term}
        r = requests.get(url=self.base_url, params=self.params)
        self.formatResponse(r)
        self.displayAddress()
        self.dialog.addres_text_box.cleared.connect(self.clearAddresses)

    def clearAddresses(self):
        self.search_responses = {}
        self.search_addresses = []
        self.search_dictionary = {}
        self.dialog.response_list.clear()
