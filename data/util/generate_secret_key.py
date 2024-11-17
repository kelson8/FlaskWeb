import os

# https://stackoverflow.com/questions/34902378/where-do-i-get-secret-key-for-flask
print(os.urandom(20).hex())
