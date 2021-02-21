import httpx
import websockets
import os

for path, dir_list, file_list in os.walk("."):
    for file_name in file_list:
        print(os.path.join(path, file_name))