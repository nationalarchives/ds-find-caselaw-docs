# Marklogic logs

Marklogic syslogs, access and error logs for both prod and staging are all
stored in Papertrail

## Setup syslogs

There are two ways to set up syslogs in Papertrail

First method used on staging was to run their install script below after ssh
on to the instance

```
wget -qO - --header="X-Papertrail-Token: your-token-key" \
https://papertrailapp.com/destinations/30508421/setup.sh | sudo bash
```

You can amend the `setup.sh` accordingly to which port you are sending
logs to if required.

The second method used on prod is to manually configure according to
instructions in Papertrail

1. See which logger your system uses then run `ls -d /etc/*syslog*`
1. Download root certificates
1. Save papertrail-bundle.pem into /etc/papertrail-bundle.pem on the log sender:
1. sudo wget -O /etc/papertrail-bundle.pem \
   https://papertrailapp.com/tools/papertrail-bundle.pem

## Setup rsyslog manually

As root, edit `/etc/rsyslog.conf` with a text editor (like pico or vi).
Paste these lines at the end:

```
$DefaultNetstreamDriverCAFile /etc/papertrail-bundle.pem
$ActionSendStreamDriver gtls
$ActionSendStreamDriverMode 1
$ActionSendStreamDriverAuthMode x509/name
$ActionSendStreamDriverPermittedPeer *.papertrailapp.com

*.*    @@logs4.papertrailapp.com:port-number
```

Check that `rsyslog-gnutls` package is installed

Restart rsyslog to re-read the config file:
sudo service rsyslog restart

## Setup app logs from Marklogic

You need to check if `remote_syslog2` is installed on the instance and
locate the install path as it may be located in `/usr/local/bin`

```
sudo remote_syslog \
  -p port-number --tls \
  -d logs4.papertrailapp.com \
  --pid-file=/var/run/remote_syslog.pid \
  /path-to-log-file.txt
```
