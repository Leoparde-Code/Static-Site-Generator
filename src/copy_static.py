import os
import shutil

def copy_static_to_public(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    else:
        shutil.rmtree(destination)
        os.mkdir(destination)
    copy_everything(source, destination)



def copy_everything(source, destination):

    if not os.path.exists(destination):
        os.mkdir(destination)
    for item_name in os.listdir(source):
        source_path = os.path.join(source, item_name)
        destination_path = os.path.join(destination, item_name)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied {item_name}")
        else:
            copy_everything(source_path, destination_path)
