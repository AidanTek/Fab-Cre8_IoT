import sys
import os
import shutil
import hashlib
import urllib.request
import time
import getpass

print('''
Raspberry Pi Eduroam Setup Tool for Cardiff Metropolitan University
by Aidan Taylor. 2018.
for support, please contact me via artaylor@cardiffmet.ac.uk

This tool will automate your network setup for Eduroam connection. You need to
have your user login and password ready. Your password is only stored in the
relevant system location and is also hashed securely. Please note this script
will restart your Pi on completion. Press ctrl-c to exit or cancel restart.
''')

# User input:
login = input('Enter your user login (eg st00000@cardiffmet.ac.uk): ')
password = getpass.getpass('Enter your secure password (text hidden): ')
password2 = getpass.getpass('re-enter password: ')

while not password == password2:
	print('Passwords do not match')
	sys.exit()

# Hash the password:
hashpass = hashlib.new('md4')
hashpass.update(bytes(password, 'utf-16le'))
print('Password securely hashed')

# Generate the CA Certificate:
print('Creating certificate...')

if not os.path.exists("/etc/ca-certificates/"):
    path = 'mkdir /etc/ca-certificates'
    os.system(path)

cert = '''echo "-----BEGIN CERTIFICATE-----
MIIE1jCCA76gAwIBAgIJANPtI+HxqbTAMA0GCSqGSIb3DQEBBQUAMIGiMQswCQYD
VQQGEwJHQjEYMBYGA1UECBMPU291dGggR2xhbW9yZ2FuMRAwDgYDVQQHEwdDYXJk
aWZmMSgwJgYDVQQKEx9DYXJkaWZmIE1ldHJvcG9saXRhbiBVbml2ZXJzaXR5MScw
JQYJKoZIhvcNAQkBFhhzeXN0ZW1zQGNhcmRpZmZtZXQuYWMudWsxFDASBgNVBAMT
C1BmZW5jZUhBIENBMB4XDTE0MDUyODE1NDYyNFoXDTE5MDUyODE1NDYyNFowgaIx
CzAJBgNVBAYTAkdCMRgwFgYDVQQIEw9Tb3V0aCBHbGFtb3JnYW4xEDAOBgNVBAcT
B0NhcmRpZmYxKDAmBgNVBAoTH0NhcmRpZmYgTWV0cm9wb2xpdGFuIFVuaXZlcnNp
dHkxJzAlBgkqhkiG9w0BCQEWGHN5c3RlbXNAY2FyZGlmZm1ldC5hYy51azEUMBIG
A1UEAxMLUGZlbmNlSEEgQ0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
AQC9yc57nl5FFde3c/O4ApkDENeqj83EV3LZgb9Q+hYC14MChcpRsms12wcvfmP1
F/RXNTETx6fS38jSCsdfD9a6vBwJ1p1D+7XATGOVD4iw0v6dXzczvsxRruZKQ1du
hOJ5boozdRoeSxI33UVC0cpxMSV/S9v8ne558nVWmS4thjM1KIp6hXnG6FKEVCM5
BEfXOXvWE2urfEmfJYp3f58ZdQFY7O8ezmy6N+OumB6iOGRmdfOI2ZIBew6Q0A+c
eA/chiAdEDm1eicf7IIciC+ugcEId6NeAhFBluLNYqVLuCtIclQc6wZG3W4IDXK2
qCxNCz7iXccGe8M3eOrUogQpAgMBAAGjggELMIIBBzAdBgNVHQ4EFgQUCXrySbPl
cBs2o8xc9AW4OoxyFXwwgdcGA1UdIwSBzzCBzIAUCXrySbPlcBs2o8xc9AW4Ooxy
FXyhgaikgaUwgaIxCzAJBgNVBAYTAkdCMRgwFgYDVQQIEw9Tb3V0aCBHbGFtb3Jn
YW4xEDAOBgNVBAcTB0NhcmRpZmYxKDAmBgNVBAoTH0NhcmRpZmYgTWV0cm9wb2xp
dGFuIFVuaXZlcnNpdHkxJzAlBgkqhkiG9w0BCQEWGHN5c3RlbXNAY2FyZGlmZm1l
dC5hYy51azEUMBIGA1UEAxMLUGZlbmNlSEEgQ0GCCQDT7SPh8am0wDAMBgNVHRME
BTADAQH/MA0GCSqGSIb3DQEBBQUAA4IBAQAzz4WWHbgnlERfGJdcxi8J4zNqlHGp
7DKpkJrrqw/YEljO5XO7DeE6pe0dRQ3PVBa3ezDSqzIrocNNFE9+TN7r0F9wCLaT
7GBpstBYz0dwGyrTKbok+trhU7KQqxSNux50PS77mzdu+rlchDT5x49Sz32H4ly4
1eKE93QLEn+xDFjxrluJPyrWi9au3HXe4MCcPcGd4JyQDUQa272RD28VXWQxKVsl
Nlr7fyZRlfY9/BWW1XdRaBIzEEESytfVZNQaIR72pBr5GpHdYMRKUAWh0OBPs+e4
kTkufkTo0VxZlNVqrC18RaD6L4oUnz2VbzKpsWUGVwzsHLhSP03JRMtf
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIFOjCCBCKgAwIBAgIJALi5o8NUatjwMA0GCSqGSIb3DQEBBQUAMIGuMQswCQYD
VQQGEwJHQjEYMBYGA1UECBMPU291dGggR2xhbW9yZ2FuMRAwDgYDVQQHEwdDYXJk
aWZmMSgwJgYDVQQKEx9DYXJkaWZmIE1ldHJvcG9saXRhbiBVbml2ZXJzaXR5MSgw
JgYJKoZIhvcNAQkBFhluZXR3b3Jrc0BjYXJkaWZmbWV0LmFjLnVrMR8wHQYDVQQD
ExZDYXJkaWZmIE1ldCBlZHVyb2FtIENBMB4XDTE2MDgxOTEyMzUxNVoXDTIxMDgx
OTEyMzUxNVowga4xCzAJBgNVBAYTAkdCMRgwFgYDVQQIEw9Tb3V0aCBHbGFtb3Jn
YW4xEDAOBgNVBAcTB0NhcmRpZmYxKDAmBgNVBAoTH0NhcmRpZmYgTWV0cm9wb2xp
dGFuIFVuaXZlcnNpdHkxKDAmBgkqhkiG9w0BCQEWGW5ldHdvcmtzQGNhcmRpZmZt
ZXQuYWMudWsxHzAdBgNVBAMTFkNhcmRpZmYgTWV0IGVkdXJvYW0gQ0EwggEiMA0G
CSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDq268RQI+jUo+20f4pkqfnzxSevfY2
Um0fIbMXU578X3LF/jLtlh6No8pJ35/cfeORKX4Hrpu82DYijoaJ3iBlzlDmQbi8
/WnhDhrg2P7Q1Wp4/M9JkU2BXaH7y8JfPrmClFXNV0PqQcc6F7+LjDBnlQAarW49
TnR/eIae/G4GfKpr3jI3G+PGVn7xB0xpanWS8T0iNZZRNxeC/giJQAk05IVCtl2e
ZJo5xhLyy2VPBQ5R1UngWS9iqMACDibDM4zXebpHjv9ovZ1vu4EVcJFYx2rMy+iB
p/P8JFfZ+z+vtfXP1xMgoGDQ8DvK8jZTwvblKgW4mEaUts1SbEsbf4XtAgMBAAGj
ggFXMIIBUzAdBgNVHQ4EFgQUgDuG8X6VubbdQcAUQ/JaqCaR1VcwgeMGA1UdIwSB
2zCB2IAUgDuG8X6VubbdQcAUQ/JaqCaR1VehgbSkgbEwga4xCzAJBgNVBAYTAkdC
MRgwFgYDVQQIEw9Tb3V0aCBHbGFtb3JnYW4xEDAOBgNVBAcTB0NhcmRpZmYxKDAm
BgNVBAoTH0NhcmRpZmYgTWV0cm9wb2xpdGFuIFVuaXZlcnNpdHkxKDAmBgkqhkiG
9w0BCQEWGW5ldHdvcmtzQGNhcmRpZmZtZXQuYWMudWsxHzAdBgNVBAMTFkNhcmRp
ZmYgTWV0IGVkdXJvYW0gQ0GCCQC4uaPDVGrY8DAPBgNVHRMBAf8EBTADAQH/MDsG
A1UdHwQ0MDIwMKAuoCyGKmh0dHA6Ly9wa2kuY2FyZGlmZm1ldC5hYy51ay9lZHVy
b2FtX2NhLmNybDANBgkqhkiG9w0BAQUFAAOCAQEAsG2FGme30IhPSwDZDVRE5UYx
VfdACKv++iZXV+0sxc1sJ/aUeDNiBOkCt915rD7g6Jecvx+GC+DtEMHfVBi48Dm3
XbvY95o4bpXLqujdICq8TD/hqr22VvmZ67nCp8I/GzdTuMf6gpcwYC+8hISJ359D
+8TX7gB4JGhoQxC/tS3+7N15qCKuFl8iOEFR51jFJIZJyohQu7U4GLLIR0+jNUN8
umPAWMvpQqHBUL21xs5dplHFPDR6oZABVqPE4/UJ6E/nLy8mPJZ8/8ebXwgirQck
Pou2S5hy8IODIPAUKDBnOvhO+qwC5xSbLE4t6A2yjbt3fxoVi8XupQ2lN9rd9Q==
-----END CERTIFICATE-----" > /etc/ca-certificates/ca.pem
'''

os.system(cert)
print('Done')

# Update network settings:
print('Updating network settings...')
net_setup = '''        ssid="eduroam"
	key_mgmt=WPA-EAP
	pairwise=CCMP
	group=CCMP TKIP
	eap=PEAP
	ca_cert="/etc/ca-certificates/ca.pem"
	identity="{}"
	domain_suffix_match="ac.uk"
	phase2="auth=MSCHAPV2"
	password=hash:{}'''.format(login, hashpass.hexdigest())

#print(net_setup)

temp = open('temp', 'w')
with open(os.path.join('/etc/wpa_supplicant', 'wpa_supplicant.conf'), 'r') as f:
    for line in f:
        temp.write(line)
    line = 'network={\n' + net_setup + '\n}\n'
    temp.write(line)
temp.close()
shutil.move('temp', os.path.join('/etc/wpa_supplicant', 'wpa_supplicant.conf'))
print('done')

print('restarting Pi in...')
counter = 5
while counter > 0:
	print(counter)
	time.sleep(1)
	counter = counter-1

os.system('reboot')
