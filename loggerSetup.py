'''
Created on Jan 4, 2014

@author: phcostello
'''

#Can use this file to setup up logging and alter
#can set the log handlers, formatters and level

#the logger here is 'root' so in files which you want to use this logging template make
#sure you have 'logger = logging.getLogger('root.'+ name_you_want_to_use)

#then just import this file before you set up other loggers 
#Set up top level logging
import logging
import os

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create file handler and set level to debug
log_file_name = 'collector.log'
if(os.path.exists(log_file_name)):
    os.remove(log_file_name)
fh = logging.FileHandler(filename=log_file_name)
fh.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)


