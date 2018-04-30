#!/usr/bin/env python

import getopt
import sys
import os
import random
import json

import boto3

def call_endpoint(endpoint_name, image_file):
    print "Calling endpoint: " + endpoint_name + " with image file: " + image_file
    
    runtime = boto3.Session().client('runtime.sagemaker')
    with open(image_file, 'rb') as f:
        payload = f.read()
        payload = bytearray(payload)
    response = runtime.invoke_endpoint(EndpointName=endpoint_name, 
                                   ContentType='application/x-image', 
                                   Body=payload)
    result = response['Body'].read()
    print json.loads(result)
    
def usage():
    print "Usage: " + sys.argv[0] + " -e <endpoint-name> -i <image-file>"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:i:v", ["help", "endpoint=", "image="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
    endpoint = None
    image_file = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--endpoint"):
            endpoint = a
        elif o in ("-i", "--image"):
            image_file = a            
        else:
            assert False, "unhandled option"
    
    if not endpoint:
        print "Endpoint name not defined"
        usage()
        sys.exit(2)

    if not image_file:
        print "Image file not defined"
        usage()
        sys.exit(2)
        
    call_endpoint(endpoint, image_file)

if __name__ == "__main__":
    main()