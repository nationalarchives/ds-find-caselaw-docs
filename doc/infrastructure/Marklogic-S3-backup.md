### Backup data to S3

1. Go to the web ui for the marklogic cluster, which will ask for basic auth you'll find username and password in 1password.
2. In Configure > Databases > caselaw-content click on the Backup/Restore tab in Marklogic for your the `caselaw-content`, initiate a backup, using the following as the
   "Back up to directory": `s3://example-prod-bucket/path/to/backup`.
3. Confirm that you want to back up the following forests to  caselaw-content to directory s3://example-prod-bucket/path/to/backup by selecting `ok` at bottom of page

### Schedule a Database Backup

1. First, navigate to prod Marklogic server, which will ask for basic auth.
   Username and password are both in 1password `TNA` vault under `caselaw` or `caselaw-staging`.
2. In Configure > Databases > caselaw-content > Scheduled Backups click on the `Create` tab in Marklogic then set the following below:
3. backup directory: `s3://example-prod-bucket/path/to/backup`.
4. backup type : `daily`
5. backup period : `1`
6. backup start time: `22:00`
7. max backups: `31`
8. Leave default settings for backup security, backup schemes, back up triggers database, include replicas, incremental backup, journal archiving and purge journal archive
9. Select `ok`
