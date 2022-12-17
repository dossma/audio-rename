from tinytag import TinyTag  # tinytag is a library for reading music meta data of most common audio and video files in pure python
import os
# import shutil
import pathlib

'''
This program renames all audio files in the specified directory (including subdirectories) from their metadata in the pattern 
>artist - title.mp3<
When metadata for artist or title is not present, the program skips the file. 
Important: The program is not interactive: It overwrtites all file names without asking!   
'''

main_folder = r"C:\path\to\audio\folder"


def main():
    file_list = collect(main_folder)
    untouchedlist = []
    for file_old in file_list:
        file_dir = os.path.dirname(file_old)  # Verzeichnis der spezifischen Datei
        try:
            file_new = parse(file_old, file_dir)
            if file_new is not None:
                file_new = rename(file_new, file_dir)
                os.rename(file_old, file_new)
            else:
                untouchedlist.append(file_old)
                continue
        except Exception as e:
            print ("Datei", file_old, "liefert Fehler\n", e, "\n")
            untouchedlist.append("Fehler: " + str(e) + "-" + file_old)

    terminate(untouchedlist)


def collect(folder):

    file_list = [os.path.join(folder, name) for folder, subdirs, files in os.walk(folder) for name in files]

    return file_list


def parse(file, file_folder):

    audio = TinyTag.get(file)
    artist = audio.artist
    title = audio.title
    ext = os.path.splitext(file)[-1]  # Dateiendung extrahieren

    if isinstance(title, str) and isinstance(artist, str):  # Wenn Metadaten für Künstler und Titel vorhanden sind
        file = file_folder + "\\"  + artist + " - " + title + ext
    # elif not isinstance(artist, str):  # Wenn kein Künstler-Tag vorhanden ist
    #     file = file_folder + "\\" + title + ext
    # elif not isinstance(title, str):  # Wenn kein Künstler-Tag vorhanden ist
    #     file = file_folder + "\\" + title + ext
    else:
        print('\nSkipping file (insufficient metadata): ' + '\033[1m' + file + '\033[0m')
        file = None

    return file


def rename(filename, file_folder):
    # Unerlaubte Dateizeichen ersetzen

    filename = filename.split("\\")[-1]

    filename = filename.replace("\n", " - ")  # "\n" ersetzen mit Bindestrich
    filename = filename.replace("\\", "-")  # "n" ersetzen mit Bindestrich
    filename = filename.replace("/", "-")  # "/" ersetzen mit Bindestrich
    filename = filename.replace("?", "-")  # "/" ersetzen mit Bindestrich
    filename = filename.replace("\"", "!")  # "/" ersetzen mit Bindestrich
    filename = filename.replace(r"*", " ! ")  # "/" ersetzen mit Bindestrich
    filename = filename.replace(r"<", " ! ")  # "/" ersetzen mit Bindestrich
    filename = filename.replace(r">", " ! ")  # "/" ersetzen mit Bindestrich
    filename = filename.replace(r":", " - ")  # "/" ersetzen mit Bindestrich
    filename = filename.replace(r"|", "-")  # "/" ersetzen mit Bindestrich

    filename = file_folder + "\\" + filename

    return filename


def terminate(untouched):
    print("\nDONE!\n")
    if untouched:
        print ("Not renamed were:")
        for x in zip(untouched):
            print(x)


if __name__ == '__main__':
    main()
    # files = collect(folder_orig)
    # parse(...)
    # rename(files)
    # save(...)
    # terminate(...)
