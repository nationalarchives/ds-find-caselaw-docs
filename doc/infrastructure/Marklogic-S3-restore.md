### Restoring data from an S3 backup

1. Go to the web ui for the marklogic cluster, which will ask for basic auth you'll find username and password in 1password.
2. In Configure > Databases > caselaw-content click on the Backup/Restore tab in Marklogic for your the `caselaw-content`, initiate a restore, using the following as the
   `"Restore from directory": s3://example-prod-bucket/path/to/backup`. You only need to set `Forest topology changed` to `true`, if there has been a change.
3. Confirm that you want to restore the following forests to database caselaw-content from directory s3://example-prod-bucket/path/to/backup by selecting `ok` at bottom of page.
