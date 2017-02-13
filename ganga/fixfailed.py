#script for resubmitting failed jobs
for job in jobs:
    for subjob in job.subjobs:
        if(subjob.status == "failed"):
            subjob.resubmit()
