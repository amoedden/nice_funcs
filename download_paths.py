#script to get filepaths from lhcbdirac

jobnum = 79 #needed to hardcode

for subjob in jobs(jobnum).subjobs:
	if(subjob.status != "completed"):
#		raise ValueError("UNFINISHED JOBS")
		pass

writefile = open("job_" + str(jobnum) + "_downloadpaths.txt", "w")

for subjob in jobs(jobnum).subjobs:
	writefile.write(subjob.outputfiles[0].lfn + "\n")

writefile.close()
