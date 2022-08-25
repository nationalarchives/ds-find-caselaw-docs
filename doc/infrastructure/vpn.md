# VPN

To access our staging and production marklogic clusters over their exposed
ports you need to use one of our 2 VPNS.

For access to all ports for data querying and admin task you need to be on the
dxw VPN.

If you only need access to port 8011 to have a locally running app with
realistic data you should be given access to the AWS VPN for the staging
account. You will be provided with a configuration file that can be user with
the [AWS client VPN software](https://aws.amazon.com/vpn/client-vpn-download/).

## generating a new certificate for the AWS VPN

- connect to an ec2 instance in the staging ecs cluster `dalmatian ecs
  ec2-access`
- `cd /mnt/efs/easy-rsa-ca/`
- create a new client certificate
- `docker run -it --rm -v $(pwd):/pki gcavalcante8808/easy-rsa build-client-full $USERNAME nopass`
- the CA passphrase is in the TNA vault in 1password
- create a new  ovpn config file and store it in 1password so you can share it
  with the user
- take an old one and replace the certificate and key in the `<cert>` and `<key>` sections with the one for the user found in `/mnt/efs/easy-rsa-ca/pki/{issued,private}`

## revoking an issued certificate

When someone leaves we should revoke their certificate.

- connect to an ec2 instance in the staging ecs cluster `dalmatian ecs
  ec2-access`
- `cd /mnt/efs/easy-rsa-ca/`
- revoke certificate
- `docker run -it --rm -v $(pwd):/pki gcavalcante8808/easy-rsa revoke
  $USERNAME`
- generate an updated CRL.
- `docker run -it --rm -v $(pwd):/pki gcavalcante8808/easy-rsa gen-crl`
- import the CRL into the VPN endpoint
- `aws ec2 import-client-vpn-client-certificate-revocation-list
  --certificate-revocation-list file:///mnt/efs/easy-rsa-ca/pki/crl.pem
  --client-vpn-endpoint-id $ENDPOINTID --region eu-west-2`

## creating a CA for the VPN


```
mkdir -p /mnt/efs/easy-rsa-ca
cd /mnt/efs/easy-rsa-ca/
docker run -it --rm -v $(pwd):/pki gcavalcante8808/easy-rsa init-pki
docker run -it --rm -v $(pwd):/pki gcavalcante8808/easy-rsa build-ca
docker run -it --rm -v $(pwd):/pki gcavalcante8808/easy-rsa build-server-full vpn.staging.caselaw.nationalarchives.gov.uk nopass
```

## setting up a client vpn end point
rough notes for setting up a client vpn endpoint.

```
aws acm import-certificate --certificate fileb://pki/issued/vpn.staging.caselaw.nationalarchives.gov.uk.crt --private-key fileb://pki/private/vpn.staging.caselaw.nationalarchives.gov.uk.key --certificate-chain fileb://pki/ca.crt
aws ec2 create-client-vpn-endpoint --server-certificate-arn arn:aws:acm:eu-west-2:REDACTED:certificate/REDACTED-f46b-444f-9a2f-1c79bd1b9b55 --client-cidr-block 10.250.0.0/22 --authentication-options Type=certificate-authentication,MutualAuthentication={ClientRootCertificateChainArn=arn:aws:acm:eu-west-2:REDACTED:certificate/REDACTED-f46b-444f-9a2f-1c79bd1b9b55} --connection-log-options Enabled=false

```
