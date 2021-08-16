"""

    UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
    USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

    ESSA API PERMITE:

    PARA OS HOTÉIS.
    1) GET DE TODOS OS HOTÉIS CADASTRADOS
    2) GET DE UM HOTEL ESPECíFICO
    3) POST PARA CADASTRO DE UM NOVO HOTEL
    4) PUT PARA ALTERAÇÃO DE UM HOTEL EXISTENTE
    5) DEL PARA DELETAR UM HOTEL.

    PARA OS USUÁRIOS.
    1) GET DE UM USUÁRIO ESPECíFICO
    2) DEL PARA DELETAR UM USUÁRIO.
    3) POST PARA CADASTRAR UM NOVO USUÁRIO
    4) POST PARA REALIZAR LOGIN E OBTER O TOKEN DE AUTENTICAÇÃO
    5) POST PARA REALIZAR LOGOUT E FINALIZAR O TOKEN DE AUTENTICAÇÃO.

    AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
    ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
    REQUISIÇÃO HTTP COM A FLAG BEARER.

    # Arguments
        json_request            - Required : Contendo informações necessários na requisição (Json)

    # Returns
        json_response           - Required : Contendo o response da requisição (Json)

"""


from inspect import stack

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin


# INSTANCIANDO A APLICAÇÃO FLASK
# __NAME__ PERMITE QUE O FLASK SAIBA ONDE O PROJETO ESTÁ LOCALIZADO
app = Flask(__name__)

# INICIANDO AS CONFIGURAÇÕES DO BANCO DE DADOS (USANDO SQLALCHEMY)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'

# INICIANDO A APLICAÇÃO FLASK
api = Api(app)

# INSTANCIANDO O JWT PARA A APLICAÇÃO
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():

    """

        ESSE HOOK DE REQUISIÇÃO É EXECUTADO ANTES DA PRIMEIRA REQUISIÇÃO SER TRATADA.

        OS HOOKS DE REQUISIÇÃO SÃO IMPLEMENTADOS COMO DECORADORES.

        ESSA FUNÇÃO CRIA O BANCO (OU APENAS VERIFICA QUE O BANCO JÁ ESTÁ EXISTENTE)
        ANTES DA PRIMEIRA REQUISIÇÃO.

        # Arguments

        # Returns

    """

    try:
        banco.create_all()
    except Exception as ex:
        print("ERRO NA FUNÇÃO: {} - {}".format(stack[0][3], ex))

# ADICIONANDO AS VIEWS
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':

    from sql_alchemy import banco

    # INICIALIZA O APLICATIVO COM CONFIGURAÇÃO DE BANCO DE DADOS
    banco.init_app(app)

    app.run(debug=True)
