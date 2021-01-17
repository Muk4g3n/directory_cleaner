import os, shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PATH = 'test'


def does_exist(directory):
    exists = False
    for i in os.listdir(PATH):
        if ((os.path.isdir(os.path.join(PATH, i))) and (i == directory)):
            exists = True
    return exists


def on_created(event):
    for i in os.listdir(PATH):

        if (os.path.isfile(os.path.join(PATH, i))):
            file_extension = os.path.splitext(i)[1]
            directory_create = ''
            if (file_extension == '.py'):
                directory_create = 'python'
            if (file_extension == '.jpg' or file_extension == '.png'
                    or file_extension == '.jpeg'):
                directory_create = 'images'
            if (file_extension == '.txt'):
                directory_create = 'text'

            if (not does_exist(directory_create)):
                os.mkdir(os.path.join(PATH, directory_create))

            shutil.move(os.path.join(PATH, i),
                        os.path.join(PATH, directory_create))


def on_modified(event):
    print("file has been moved")


if __name__ == "__main__":
    event_handler = FileSystemEventHandler()

    event_handler.on_created = on_created
    event_handler.on_modified = on_modified

    obs = Observer()
    obs.schedule(event_handler, PATH, recursive=True)
    obs.start()
    try:
        while (True):
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
        print("done")
    obs.join()
