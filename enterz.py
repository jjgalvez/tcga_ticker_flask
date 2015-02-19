__author__ = 'galvezjj'

from Bio import Entrez, Medline
import datetime


class TCGA:
    def __init__(self, maxdate):
        self.age = ''
        self.EZ = Entrez
        self.EZ.email = 'jose.galvez@nih.gov'
        self.maxdate = maxdate
        self.recordObj = None
        self.medlineData = None
        self.records()

    def _getRecord(self, maxdate=None):
        '''
        Call the initial pubmed search and set up the search history.
        :param maxdate:
        :return: set the pubmed records object
        '''
        if not maxdate:
            maxdate = self.maxdate
        print('record called')
        record = self.EZ.read(
            self.EZ.esearch(
                db='pubmed',
                term='tcga',
                retmax=2000,
                mindate='2000/01/01',
                maxdate=maxdate.strftime('%Y/%m/%d'),
                usehistory='y'
            )
        )
        self.recordObj = record


    def _getDate(self, ret=20):
        '''
        Retrieve some number of records from pubmed referencing the initial search
        :param ret: number or records to return
        :return: set the medlineData object
        '''
        webenv = self.recordObj['WebEnv']
        query_key = self.recordObj['QueryKey']
        # start = int(self.record()['Count']) - ret
        fetch = self.EZ.efetch(
            db='pubmed',
            rettype='medline',
            retmode='text',
            # retstart=start,
            retmax = ret,
            webenv=webenv,
            query_key=query_key
        )
        records = Medline.parse(fetch)
        self.medlineData =  list(records)


    def records(self):
        '''
        run a pubmed search and retrieve the records
        :return: pubmed record and medline data objects
        '''
        delta = datetime.datetime.now()-self.maxdate
        if not self.recordObj:
            self._getRecord()
            self._getDate()
        elif delta.days >= 1:
            self.maxdate = datetime.datetime.now()
            self._getRecord(maxdate=self.maxdate)
            self._getDate()

        return self.recordObj, self.medlineData