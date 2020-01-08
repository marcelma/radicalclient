import glob
import os
import shutil
import tempfile
import tqdm

def find_files_to_copy(mountpoint, num_files):
    mp4_files = glob.glob(mountpoint + "/DCIM/**/*.MP4", recursive=True)
    mp4_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    list_file = mp4_files[:num_files]

    print('{} Arquivos encontrados ...'.format(num_files))
    return list_file

def copy_to_localhost(files):
    dst = tempfile.mkdtemp()

    with tqdm.tqdm(total=len(files)) as pbar:
        for file in files:
            shutil.copy(file,dst)
            pbar.update()

    return dst

def copy_to_smb(files):
    print('smb ...')
    print(files)
