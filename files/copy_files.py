import glob
import json
import os
import shutil
import tempfile
import tqdm

from jinja2 import Environment, FileSystemLoader

#TODO: alert if select more files than have on usb

def client_data_dump(client):
    with open(client['dest_dir']+'/data.json', 'w', encoding='utf-8') as f:
        json.dump(client, f, ensure_ascii=False, indent=4)
        f.close

def copy_files(files, orig_dir=None, client=None):
    if not orig_dir:
        return copy_to_localhost(files)
    elif orig_dir:
        return copy_to_smb(files, orig_dir, client)
    else:
        raise Exception('Invalid copy option')

def copy_to_localhost(files):
    dest_dir = tempfile.mkdtemp()

    print('Copiando para diretório temporário... ')
    with tqdm.tqdm(total=len(files)) as pbar:
        for file in files:
            shutil.copy(file,dest_dir)
            pbar.update()

    return dest_dir

def copy_to_smb(files, orig_dir, client):
    dest_dir = os.getenv("COPY_DEST_DIR")

    if 'tandem' in client['jump_type']:
        full_dest_dir = dest_dir+'/tandem/'+client['date']+'/'+client['name']
    else:
        full_dest_dir = dest_dir+'/atleta/'+client['name']+'/'+client['jump_type']

    client['dest_dir'] = full_dest_dir

    # Create target Directory if don't exist
    if not os.path.exists(full_dest_dir):
        os.makedirs(full_dest_dir)

    files = client['videos']

    print('Copiando para o servidor!... ')
    with tqdm.tqdm(total=len(files)) as pbar:
        for file in files:
            file_name = file.split('/')[-1]
            shutil.copy(orig_dir+'/'+file_name,full_dest_dir)
            os.chmod(full_dest_dir+'/'+file_name, 0o644)
            pbar.update()

    shutil.rmtree(orig_dir)
    create_index(client)
    client_data_dump(client)

def create_index(client):
    files = []
    TEMPLATE_FILE = "./templates/index.j2"
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)

    for file in client['videos']:
        files.append(file.split("/")[-1])

    client['videos'] = files

    index_file = j2_env.get_template(TEMPLATE_FILE).render(files=files)

    with open(client['dest_dir']+'/index.html', 'w') as f:
        f.write(index_file)
        f.close

def find_files_to_copy(mountpoint, num_files):
    mp4_files = glob.glob(mountpoint + "/DCIM/**/*.MP4", recursive=True)
    mp4_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    list_file = mp4_files[:num_files]

    print('{} Arquivos encontrados ...'.format(num_files))
    return list_file

def search_videos(mountpoint):
    qnt_files = int(input('Quantos arquivos foram criados?: '))
    return find_files_to_copy(mountpoint, qnt_files)
