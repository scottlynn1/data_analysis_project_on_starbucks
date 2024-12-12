from os import environ

TARGET_URL = environ.get('TARGET_URL', default = "urrl")
print(TARGET_URL)
#TARGET_URL = environ.get('TARGET_URL')
#print(TARGET_URL)
TARGET_URL = environ.get('TARGET_URL', default = 'urrrrrrl')
print(TARGET_URL)