#!/usr/bin/python
import requests
import argparse
import os
import sys
import json
import urllib3
import io
import csv
from settings import authsettings


def main():
    """
    Do the stuff & things.

    Parse command line arguments and execute.
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = initargparser()
    args = parser.parse_args()

    token = staxxauth(authsettings['staxxurl'], authsettings['staxxport'],
                      authsettings['username'], authsettings['password'])

    iocs = staxxquery(authsettings['staxxurl'], authsettings['staxxport'],
                      token, args.query, args.format)

    writeiocs(iocs, args.path, args.name, args.format)


def initargparser():
    """
    Initialize and return the argument parser object.

    Inputs:
    None

    Returns:
    parser (argparser)

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="A valid Anomali STAXX API query.")
    parser.add_argument("-f", "--format",
                        help="Output file format. Default is 'j' (JSON).",
                        choices=['j', 'c'], default='j')
    parser.add_argument("-p", "--path",
                        help="Output path. Defaults to working directory.",
                        default=os.getcwd() + '/')
    parser.add_argument("-n", "--name",
                        help="Output filename. Defaults to 'iocs'.",
                        default="iocs")

    return parser


def staxxauth(staxxurl, staxxport, staxxuser, staxxpass):
    """
    Get an auth token from STAXX.

    Inputs:
    staxxurl (string) - the URL of the STAXX server.
    staxxport (string) - listening port of the STAXX server.
    staxxuser (string) - username to auth as.
    staxxpass (string) - password for staxxuser.

    Returns:
    authtoken (JSON)- the JSON auth token returned by the STAXX API.

    All of these arguments should be supplied in settings.py in the same
    folder netstaxx runs from in the authsettings dictionary.

    """
    uri = staxxurl + ':' + staxxport + '/api/v1/login'

    h = {'Content-Type': 'application/json'}
    d = json.dumps({'username': staxxuser, 'password': staxxpass})

    token = requests.post(uri, headers=h, data=d, verify=False)
    if token.status_code != 200:
        print('Failed to retrieve login token.')
        sys.exit()
    else:
        token_id = token.json()['token_id']

    return token_id


def staxxquery(staxxurl, staxxport, authtoken, query, format):
    """
    Retrieve IOCs for a given query.

    Inputs:
    authtoken (JSON) - the authtoken object returned by staxxauth().
    query (string) - the query to be used when interrogating the API.
    format (string) - argument that indicates how results are formatted.

    Returns:
    iocs (JSON or CSV)- IOC data from STAXX.

    """
    if format == 'j':
        ioctype = 'json'
    elif format == 'c':
        ioctype = 'csv'
    else:
        print('Invalid format. Valid choices are j (json) and c (csv).')

    uri = staxxurl + ':' + staxxport + '/api/v1/intelligence'
    d = json.dumps({"token": authtoken, "query": query,
                    "type": ioctype}).encode("utf-8")
    h = {'Content-Type': 'application/json'}

    iocs = requests.post(uri, d, headers=h, verify=False)

    return iocs.content


def writeiocs(iocs, path, name, format):
    """
    Write IOCs to disk.

    Inputs:
    iocs (JSON) - data collection returned from staxxquery().
    path (string) - file path.

    Returns: None.

    """
    filestring = path + name
    if format == 'j':
        filestring = filestring + '.json'
        print(filestring)
        with open(filestring, 'w') as outfile:
            outfile.write(iocs)
    elif format == 'c':
        filestring = filestring + '.csv'
        print(filestring)
        with open(filestring, 'w') as outfile:
            outfile.write(iocs)
    else:
        print('Bad format. Valid choices are (j)son and (c)sv.')


if __name__ == '__main__':
    main()
