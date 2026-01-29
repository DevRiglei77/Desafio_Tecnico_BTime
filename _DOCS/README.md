
1. **Criação do Ambiente Virtual**:
-- digite os seguintes comandos:

```sh
python -m venv venv
```

2. **Ativação do Ambiente Virtual**:

No Windows:
```sh
.\venv\Scripts\activate
```

No macOS/Linux:
```sh
source venv/bin/activate
```

Instalação das Dependências:
Certifique-se de que o ambiente virtual esteja ativado e execute:

```sh
pip install -r _APP/requirements.txt
```

3. **Configuração do Projeto**

Configuração do Arquivo .env:
Adicione as seguintes variáveis ao arquivo .env:

API_KEY_OPENWEATHERMAP = <chave da api>
### OBSERVAÇÃO  
- para obter a chave da api,basta fazer seu registro nesse site: 
- https://home.openweathermap.org/users/sign_up

___


4. **Exemplo para rodar o projeto**

python _APP/main.py