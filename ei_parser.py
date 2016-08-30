#!/usr/bin/env python
# title           :EiParser
# description     :This is the base class to inherit from that parses crytek files
# author          :Chris Sprance / Entrada Interactive
# date            :06/02/15
# usage           : Formats all the recipe items
# notes           :
# python_version  :2.7.5
# ==============================================================================

import xml.etree.cElementTree as ET
import logging
import os


class EiParser(object):
    """This class contains all the methods to parse Crytek files"""

    def __init__(self, db):
        super(EiParser, self).__init__()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs/' + self.__class__.__name__ + 'parser.log', level=0, format='')
        self.db = db
        self.etree = ET.ElementTree
        self.file_type = str()
        self.file = str()
        self.files = list()
        self.idx = int()
        self.folder = str()
        self.p4 = self.db.p4 if self.db.use_p4 else None
        self.db.commit_changes = True

    def filter(self):
        """filter is the method run on each individual self.file"""
        self.logger.debug('Filtering etree object', self.etree)

    def open_from_folder(self):
        """This method contains the code necessary to collect all self.file_type from a folder recursively"""
        for root, dirs, files in os.walk(self.folder):
            for f in files:
                if f.endswith(self.file_type):
                    self.files.append(os.path.join(root, f))
            self.start_filtering()

    def parse_xml(self):
        """Parse the self.file and set the parsed etree to self.etree"""
        self.etree = ET.parse(open(self.file)).getroot()

    def start_filtering(self):
        """start filtering is run after collecting all the files"""
        for self.idx, self.file in enumerate(self.files):
            try:
                # start everything off but fail silently and log it if there is an error opening a particular file
                self.parse_xml()
            except Exception, e:
                self.logger.error(e)
            # filter the file if it passes Etree parsing
            self.filter()

    def start_parsing(self):
        """Start Parsing The layer or layers"""
        if len(self.folder) > 1:
            self.open_from_folder()
        else:
            self.files.append(self.file)
            self.start_filtering()
        # after everything has been parsed and inserted commit all the changes to the database
        if self.db.commit_changes is True:
            self.db.conn.commit()
        return True
