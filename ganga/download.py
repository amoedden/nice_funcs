#download script for ntuples from grid ----v1
#requires: 
#	download_paths.py must have created job_xx_downloadpaths.txt (must be in same folder)
#usage:
#	lb-run LHCbDIRAC latest bash -norc
#	python download.py  $jobnumber  $pathtodownload 

from sys import argv
import subprocess
import os
from warnings import warn


jobnum = argv[1]
downloadpath = argv[2]

filename = "job_" + jobnum + "_downloadpaths.txt"
file = open(filename, "r+")
patharray = file.read().split("\n")[:-1] #remove last line (just after \n)
file.close()

#now i have an array with all download paths

#get tuplename to check if it exists already (later)
tuplename = patharray[0].split("/")[-1] #always the same name
print(tuplename)

#no empty lines: nothing should be unfinished
if "" in patharray:
	warn("not all jobs finished")


#make dir for job download if not existent already
if(not os.path.isdir("{0}/{1}".format(downloadpath,jobnum).replace("//", "/"))):
	os.mkdir("{0}/{1}".format(downloadpath,jobnum).replace("//", "/"), 0700) #if downloadpath is given with / at the end, replace the //
else:
	print("jobdir already exists, skipping...")

#print("mkdir {0}/{1}".format(downloadpath,jobnum).replace("//", "/"))
#a counter for some things in the loop
ctr = 0

#make dirs for each subjob, download there
for path in patharray:
	if(path != ""):
		if(not os.path.isdir("{0}/{1}/{2}".format(downloadpath,jobnum,ctr).replace("//", "/"))):
			os.mkdir("{0}/{1}/{2}".format(downloadpath,jobnum,ctr).replace("//", "/"), 0700)
		else:
			print("dir for job {0} exists already...".format(ctr))


		#check if file exists, if not: download
		if(not os.path.isfile("{0}/{1}/{2}/{3}".format(downloadpath,jobnum,ctr,tuplename).replace("//", "/"))):
			#change to subjob directory
			os.chdir("{0}/{1}/{2}".format(downloadpath,jobnum,ctr).replace("//", "/"))
			#download file here
			process = subprocess.Popen("dirac-dms-get-file {0}".format(path), shell=True)
			process.wait()
		else:
			print("file exists {0} already".format(ctr))
	else:
		print("job {0} is not yet finished, skipping download...".format(ctr))
	ctr +=1
