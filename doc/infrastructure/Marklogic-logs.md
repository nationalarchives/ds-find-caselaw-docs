# MarkLogic logs

The instances in the MarkLogic clusters are configured to send their logs to the
TNA Papertrail account. Once configured we send system logs using rsyslog and
MarkLogic logs using remote_syslog2 to Papertrail. We explicitly exclude the
logs for the service running on port 7997 since that is only used by the load
balancers to determine if the Marklogic server on that instance is available.

## Setup remote logging

We have to configure remote logging ourselves when a instance is created within a
cluster. In the future we hope to have remote logging configured on creation.

We have scripted the configuration and have added it to this repo. On a new
instance you should run the following `wget
https://https://raw.githubusercontent.com/nationalarchives/ds-find-caselaw-docs/main/scripts/setup-syslog.sh
-O /tmp/setup-syslog.sh ; bash /tmp/setup-syslog.sh $LOGHOST $LOGPORT`
where $LOGHOST and $LOGPORT are the values that papertrail provides. e.g logs7
and 1337

You can test that logs are being sent by running `logger testlog; curl
localhost:8011/testlog` and searching Papertrail for `testlog`

