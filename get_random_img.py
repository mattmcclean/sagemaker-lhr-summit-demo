#!/usr/bin/env python

import os
import random

# set the data directory
dir_name = '/home/ec2-user/environment/data/dogscats/test1/'

# Set the SageMaker endpoint name
endpoint_name = 'london-summit-demo-endpoint'

file_name = dir_name + random.choice(os.listdir(dir_name)) 
print(file_name)