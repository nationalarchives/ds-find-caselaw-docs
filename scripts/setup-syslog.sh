#!/bin/bash
# script to set up syslog on marklogic servers
#

LOGHOST=$1
LOGPORT=$2

sudo wget -O /etc/papertrail-bundle.pem https://papertrailapp.com/tools/papertrail-bundle.pem
sudo yum -y install rsyslog-gnutls
{
  echo '$DefaultNetstreamDriverCAFile /etc/papertrail-bundle.pem'
echo '$ActionSendStreamDriver gtls'
echo '$ActionSendStreamDriverMode 1'
echo '$ActionSendStreamDriverAuthMode x509/name'
echo '$ActionSendStreamDriverPermittedPeer *.papertrailapp.com'
echo ""
echo "*.*    @@${LOGHOST}.papertrailapp.com:${LOGPORT}"
} | sudo tee /etc/rsyslog.d/99-papertrail.conf
sudo service rsyslog restart
sudo yum install -y https://github.com/papertrail/remote_syslog2/releases/download/v0.21/remote_syslog2-0.21-1.x86_64.rpm


{
echo "files:"
echo "  - /var/opt/MarkLogic/Logs/*Log.txt"
echo "exclude_files:"
echo '  - 7997_AccessLog.txt$'
echo "destination:"
echo "  host: $LOGHOST.papertrailapp.com"
echo "  port: $LOGPORT"
echo "  protocol: tls"
} | sudo tee /etc/log_files.yml

sudo service remote_syslog start
sudo ln -s /etc/init.d/remote_syslog /etc/rc3.d/S30remote_syslog
