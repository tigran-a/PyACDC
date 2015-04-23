#!/usr/bin/python3 
# also works with python 2

"""
    Example of usage CCHv2 class 

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

import json
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__file__)

import os,sys

from apiv2 import CCHv2
from api_key import key


if __name__ == "__main__":
   
    cch = CCHv2(apikey = key, host = "webservice.db.acdc-project.eu", port=3000)

    print("Requesting all reports for last 15 min") 
    r =  cch.get_reports()
    print(json.dumps(r))
    print(32*"-")

    print("Get all reports of AS1627")
    r =  cch.get_reports_by_asn(16276)
    print(json.dumps(r))
    print(32*"-")

    print("Get all reports of ip 10.0.0.1 (dumb stuff)")
    r =  cch.get_reports_by_ips("10.0.0.1")
    print(json.dumps(r))
    print(32*"-")

    print("Get all reports of ip 10.0.0.1 (dumb stuff) with report id =12 (?)")
    r =  cch.get_reports_by_ips("10.0.0.1", 12)
    print(json.dumps(r))
    print(32*"-")

    reportid= "552e5f937765624b450f5c00"
    print("Get report with id=%s"%reportid)
    r =  cch.get_report(reportid)
    print(json.dumps(r))
    print(32*"-")

    print("Submitting a test report")
    r = cch.submit_report( data = {
        'report_category': 'eu.acdc.minimal', 
        'report_type' : 'Test report of minimal schema',
        'timestamp' : '2015-02-27T17:00:11Z', 
        'source_key': 'uri',
        'source_value' : 'http://unknown.domain',
        'confidence_level': 0.01,
        'version': 1,
     }
    )
    print(json.dumps(r))
    print(32*"-")

    print("Requesting again all reports for last 15 min; should see the submitted one") 
    r =  cch.get_reports()
    print(json.dumps(r))
    print(32*"=")
