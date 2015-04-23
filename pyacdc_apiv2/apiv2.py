#!/usr/bin/python3 
# also works with python 2

"""
    Lib for accessing ACDC CCH (API v2)

    (c) Copyright 2015 Tigran Avanesov, SnT, University of Luxembourg

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import sys
import os
import json

PACKAGE_PARENT = '.'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__file__)

import requests

from urltoolz import *


class CCHv2:

    def __init__(self, apikey, scheme="https", host = "webservice.db.acdc-project.eu", port=3000):

        self.session = requests.Session()

        # Disable ssl verification! TODO: remove from production
        self.session.verify = False

        self.baseurl = build_base_url(scheme, host, port) 
        self.apikey = apikey
        self.apiv = "v2"

        self.session.headers.update({
                "Authorization" : 'Token token="%s"'%self.apikey,
                "Content-Type" : "application/json",
            })

    def req(self, path="/", data=None, headers = None, reqtype = 'get'):
        """ gets the data """

        if headers is None: 
            headers = {}
        if data is None: 
            data = {}


        res = None
        try:
            r = None
            if reqtype == 'get': 
                r = self.session.get(url_join(self.baseurl, 'api', self.apiv, path), headers = headers, data = data)
            elif reqtype == 'post': 
                r = self.session.post(url_join(self.baseurl, 'api', self.apiv, path), headers = headers, data = json.dumps(data))
            else:
                log.error('Unsupported request type. Not implemented?')

            log.debug('Queried: %s', r.url)

            if r.status_code == 401:
                log.warning("Unauthorized: Your API key probably has no access for the requested data")
                log.warning("Reason: %s"%r.reason)
            else:
                r.raise_for_status()
                res = r.json()
        except Exception as e:
            log.error("Error getting data: %s",e)
        finally:
            return res

    def submit_report(self, data):
        """ submits a report

        e.g. 
        cchv2 = CCHv2(apikey="YOURKEY")
        r = cchv2.submit_report(data = {
            'report_category': 'eu.acdc.minimal', 
            'report_type' : 'Test v2',
            'timestamp' : '2014-09-30T17:00:11+02:00', 
            'source_key': 'uri',
            'source_value' : 'http://exit0.de',
            'confidence_level': 0.11,
            'version': 1,
         }
        )
        """
        return self.req(path="reports", data=data, reqtype = "post")

    def get_reports(self):
        """ get all reports submitted by the given api key (for the last x minutes, x = 15 usually) """
        return self.req(path="reports", reqtype = "get")

    def get_report(self, rep_id):
        """ get report with the given id (submitted for the last x minutes, x = 15 usually) """
        return self.req(path=url_join("reports", str(rep_id)), reqtype = "get")

    def get_reports_by_asn(self, asn):
        """ Gets reports for a given ASN (if allowed) """ 
        
        sasn = str(asn)
        if not sasn.startswith('AS'):
            sasn = 'AS' + sasn

        return self.req(path=url_join('asns', sasn), reqtype = "get")


    def get_reports_by_ips(self, ips, incident = None):
        """ Gets reports for a given IP (if allowed) ;
        Can also specify the incident id?""" 
        
        path = url_join('ips', ips)
        if incident is not None:
            path = url_join(path, str(incident))
        return self.req(path=path, reqtype = "get")

if __name__ == "__main__":

    print("To try the library, please, see examples-v2.py")

