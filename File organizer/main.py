import os
from pathlib import Path


List_of_Directories = {
    "Pictures": [".jpeg", ".jpg", ".gif", ".png", ".webP"],
    "Video": [".wmv", ".mov", ".mp4", ".mpg", "mpeg", ".mkv"],
    "Zip": [".7z", ".rar", ".zip", ".iso", ".tar", ".gz", ".dmg"],
    "Music": [".mp3", ".wav", ".wma", ".msv"],
    "Text": [".pdf", ".docx"]
}


File_Format_Dicitonary = {
    final_file_format: directory
    for directory, file_format_stored in List_of_Directories.items()
    for final_file_format in file_format_stored
}


def organizer(): 
    for entry in os.scandir():
        if entry.is_dir():
            continue
        file_path=Path(entry)
        final_file_format = file_path.suffix.lower()
        if final_file_format in File_Format_Dicitonary:
            directory_path = Path(File_Format_Dicitonary[final_file_format])
            os.makedirs(directory_path, exist_ok=True)
            os.rename(file_path, directory_path.joinpath(file_path))


try: 
    os.mkdir("Other")
except ValueError:
    print ("Failed to create directory")


for dir in os.scandir():
    try:
        if dir.is_dir():
            os.rmdir(dir)
        else:
                os.rename(os.getcwd() + '/' + str(Path(dir)), os.getcwd() + '/Other_Folder/' + str(Path(dir)))
    except ValueError:
        print ("Failed to create a new directory called Other. Folder may already exist")