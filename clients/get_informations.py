import datetime

# TODO: validate name with spaces

def client_informations():
    client = {}
    client['name'] = input('Nome do passageiro?: ')
    client['date'] = datetime.date.today().strftime("%Y/%m/%d")
    client['cell_phone'] = int(input('Qual o numero do celular do passageiro com ddd? (92912345678): '))
    client['instagram'] = input('Qual o instagram do passageiro?: ')
    client['instrutor'] = input('Nome do instrutor?: ')
    client['instrutor_cell'] = ''
    client['jump_type'] = input('Qual tipo de Salto? (tandem): ')
    client['videos'] = []
    client['dest_dir'] = ''

    return client
