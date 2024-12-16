import os
import glob
from watchdog.events import FileSystemEvent
import watchdog.observers


for root, dirs, files in os.walk(os.getcwd()):
    print(files)