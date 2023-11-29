#!/bin/bash

# Navigate to the directory containing your files
cd /var/log/nginx

# Run AWS S3 sync command
aws s3 sync . s3://mern-1999


## chmod +x cron-job-upload-logs.sh
## crontab -e
## */30 * * * * /path/to/sync_script.sh --> every half n hour
