from os import scandir, rename, makedirs, path, getenv
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "C:/Users/ikiga/Downloads"
dest_dir_music = source_dir + '/Music'
dest_dir_video = source_dir + '/Video'
dest_dir_image = source_dir + '/Image'
dest_dir_documents = source_dir + '/Documents'
dest_dir_app = source_dir + '/Applications'
dest_dir_compress_file = source_dir + '/Compressed'

video_extensions = ['.webm', '.mpg', '.mpeg', '.mp4', '.ogg', '.mp4v', '.m4v', '.avi', '.wmv', '.mov', '.flv']
audio_extensions = ['.m4a', '.flac', '.mp3', '.wav', '.wma', '.aac']
image_extensions = ['.png', '.gif', '.jpg', '.jpeg', '.webp']
document_extensions = ['.pdf', '.txt', '.doc','.xls', '.xlsx', '.ppt', '.pptx']
compress_extensions = ['.zip', '.rar', '.7z']
application_extensions = ['.exe', '.msi']


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest / name}"):
        name = f"{filename}{str(counter)}{extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if not exists(dest):
        makedirs(dest)

    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)

    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_application_files(entry, name)
                self.check_document_files(entry, name)
                self.check_compress_files(entry, name)

    @staticmethod
    def check_audio_files(entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_music, entry, name)
                logging.info(f"Moved: {name} -> {dest_dir_music}")

    @staticmethod
    def check_video_files(entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved: {name} -> {dest_dir_video}")

    @staticmethod
    def check_image_files(entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved: {name} -> {dest_dir_image}")

    @staticmethod
    def check_document_files(entry, name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved: {name} -> {dest_dir_documents}")

    @staticmethod
    def check_application_files(entry, name):
        for application_extension in application_extensions:
            if name.endswith(application_extension) or name.endswith(application_extension.upper()):
                move_file(dest_dir_app, entry, name)
                logging.info(f"Moved: {name} -> {dest_dir_app}")

    @staticmethod
    def check_compress_files(entry, name):
        for compress_extension in compress_extensions:
            if name.endswith(compress_extension) or name.endswith(compress_extension.upper()):
                move_file(dest_dir_compress_file, entry, name)
                logging.info(f"Moved: {name} -> {dest_dir_compress_file}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()