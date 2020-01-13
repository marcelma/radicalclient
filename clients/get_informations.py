import datetime

def tandem_passenger_information():
    client = {}
    client['name'] = input('Nome do passageiro?: ')
    client['date'] = datetime.date.today().strftime("%d/%m/%Y")
    client['cell_phone'] = int(input('Qual o numero do celular do passageiro?: '))
    client['cell_so'] = input('Qual o Tipo do celular?: ')
    client['instagram'] = input('Qual o instagram do passageiro?: ')
    client['instrutor'] = input('Nome do instrutor?: ')
    client['instrutor_cell'] = ''
    client['jump_type'] = 'tandem'
    client['videos'] = []
    client['remote_dir'] =''

    return client
