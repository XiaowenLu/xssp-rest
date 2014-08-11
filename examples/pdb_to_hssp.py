"""
This example client takes a PDB file, sends it to the REST service which
converts it to a HSSP file. The HSSP content is then output to the console.

Example:

    python pdb_to_hssp 1crn.pdb http://localhost:5000/
"""

import argparse
import json
import requests
import time


def pdb_to_hssp(pdb_file_path, rest_service_url):
    with open(pdb_file_path) as pdb_file:
        pdb_content = pdb_file.read()

    r = requests.post(rest_service_url + 'api/create/hssp/from_pdb/',
                      data={'pdb_content': pdb_content})
    r.raise_for_status()
    job_id = json.loads(r.text)['id']
    print "Job submitted successfully. Id is: '{}'".format(job_id)

    ready = False
    while not ready:
        r = requests.get(rest_service_url +
                         'api/job/hssp_from_pdb/{}/status/'.format(job_id))
        r.raise_for_status()

        status = json.loads(r.text)['status']
        print "Job status is: '{}'".format(status)
        if status in ['SUCCESS', 'FAILURE', 'REVOKED']:
            ready = True
        else:
            time.sleep(5)
    else:
        r = requests.get(rest_service_url +
                         'api/job/hssp_from_pdb/{}/result/'.format(job_id))
        r.raise_for_status()
        result = json.loads(r.text)['result']
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert a PDB file to a HSSP file')
    parser.add_argument('pdb_file_path')
    parser.add_argument('rest_service_url')
    args = parser.parse_args()

    result = pdb_to_hssp(args.pdb_file_path, args.rest_service_url)
    print result
