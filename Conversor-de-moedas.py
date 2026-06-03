import requests

class Conversor:
    def __init__(self, moeda_origem, moedas_destino, valor):
        self.moeda_origem = moeda_origem
        self.moedas_destino = moedas_destino
        self.valor = valor

    def cotacao(self, moeda):
        url = f'https://api.frankfurter.app/latest?from={self.moeda_origem}&to={moeda}'
        try:
            resposta = requests.get(url)
            dados = resposta.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
            print('\nErro na conexão!')
            return None
        if 'message' in dados:
            print('\nMoeda inválida!')
            return None
        taxa = dados['rates'][moeda]
        return taxa

    def converter(self):
        if self.cotacao(self.moedas_destino[0]) is None:
            return False
        print(f'\n{self.valor:.2f} {self.moeda_origem} =')
        sucesso = 0
        for moeda in self.moedas_destino:
            if moeda == self.moeda_origem:
                continue
            taxa = self.cotacao(moeda)
            if taxa is None:
                continue
            sucesso += 1
            result = self.valor * taxa
            print(f'  {result:.2f} {moeda}')
        if sucesso == 0:
            print('Todas as moedas são inválidas!\n')
            return False
        return True

def main():
    dados = pegar_dados()
    if dados is None:
        return
    moeda_origem, moedas_destino, valor = dados
    while True:
        c = Conversor(moeda_origem, moedas_destino, valor)
        if c.converter():
            break
        dados = pegar_dados()
        if dados is None:
            return
        moeda_origem, moedas_destino, valor = dados

def pegar_dados():
    try:
        resposta = requests.get('https://api.frankfurter.app/currencies')
    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        print('\nErro na conexão!')
        return None
    dados = resposta.json()
    print(f"Moedas disponíveis: {', '.join(dados.keys())}")
    moeda_origem = input('De qual moeda? ').upper()
    moedas_destino = input('Para quais moedas? ').upper().replace(',', '').split()
    try:
        valor = float(input('Qual valor? ').replace(',', '.'))
    except ValueError:
        print('Valor inválido!')
        return None
    return moeda_origem, moedas_destino, valor

main()