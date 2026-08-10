import socket
import ssl
from datetime import datetime, timezone

get_ip = socket.gethostbyname('google.com')

with ssl.create_default_context().wrap_socket(socket.create_connection((get_ip,443),timeout=5),server_hostname='google.com') as ssocket:
    get_cert = ssocket.getpeercert()['notAfter']
    # cert_date = datetime.strptime(get_cert,'%b %d %H:%M:%S %Y %Z').replace(tzinfo=timezone.utc)
    # curr_date = datetime.now(timezone.utc)
    # days_diff = (cert_date - curr_date).days
    print(get_cert)
    
