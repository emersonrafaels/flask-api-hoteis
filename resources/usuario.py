"""

    UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
    USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

    CONTÉM AS FUNÇÕES PARA OS USUÁRIOS:

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


from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

from models.usuario import UserModel


# OBTENDO OS VALORES ENVIADOS NO JSON_REQUEST.
# OBTENDO INFORMAÇÕES DE: LOGIN E SENHA.
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank.")


class User(Resource):

    """

        UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
        USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

        CONTÉM AS FUNÇÕES PARA OS USUÁRIOS:

        1) GET DE UM USUÁRIO ESPECíFICO
        2) DEL PARA DELETAR UM USUÁRIO.

        AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
        ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
        REQUISIÇÃO HTTP COM A FLAG BEARER.

        # Arguments
            json_request            - Required : Contendo informações necessários na requisição (Json)

        # Returns
            json_response           - Required : Contendo o response da requisição (Json)

    """

    # /usuarios/{user_id}
    def get(self, user_id):

        """

            FUNÇÕES GET PARA OBTER UM USUÁRIO ESPECÍFICO.

            # Arguments
                user_id                 - Required : O ID do usuário desejado.
                                                     É enviado via URL (Integer)

            # Returns
                json_response           - Required : O usuário cadastrado ou o
                                                     usuário não existe (Json)

        """

        # BUSCANDO O USUÁRIO ENVIADO
        user = UserModel.find_user(user_id)

        if user:
            # CASO O USUÁRIO: ENCONTRADO
            return user.json()
        # CASO O USUÁRIO: NÃO ENCONTRADO
        return {'message': 'User not found.'}, 404


    @jwt_required
    def delete(self, user_id):

        """

            FUNÇÃO DELETE PARA DELETAR UM USUÁRIO.
            USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

            AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
            ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
            REQUISIÇÃO HTTP COM A FLAG BEARER.

            # Arguments
                user_id                 - Required : O ID do usuário desejado.
                                                     É enviado via URL (Integer)

            # Returns
                json_response           - Required : Validador de execução da função (Json)

        """

        # BUSCANDO O USUÁRIO ENVIADO
        user = UserModel.find_user(user_id)

        try:
            if user:
                # CASO O USUÁRIO: ENCONTRADO
                # REALIZA-SE O DELETE DO USUÁRIO
                user.delete_user()
                return {'message': 'User deleted.'}

            # CASO O USUÁRIO: NÃO ENCONTRADO
            return {'message': 'User not found.'}, 404
        except:
            # INTERNAL SERVER ERROR
            return {"message": "An error ocurred trying to create hotel."}, 500


class UserRegister(Resource):

    """

        UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
        USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

        CONTÉM AS FUNÇÕES PARA OS USUÁRIOS:

        1) POST PARA CADASTRAR UM NOVO USUÁRIO

        AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
        ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
        REQUISIÇÃO HTTP COM A FLAG BEARER.

        # Arguments
            json_request            - Required : Contendo informações necessários na requisição (Json)

        # Returns
            json_response           - Required : Contendo o response da requisição (Json)

    """

    # /cadastro
    def post(self):

        """

            FUNÇÃO POST PARA CADASTRAR UM NOVO USUÁRIO.
            USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

            AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
            ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
            REQUISIÇÃO HTTP COM A FLAG BEARER.

            # Arguments
                user_id                 - Required : O ID do usuário desejado.
                                                     É enviado via URL (Integer)

            # Returns
                json_response           - Required : Validador de execução da função (Json)

        """

        # OBTENDO OS DADOS ENVIADOS POR JSON
        dados = atributos.parse_args()

        # VERIFICANDO SE O USUÁRIO JÁ EXISTE
        if UserModel.find_by_login(dados['login']):
            # CASO USUÁRIO: CADASTRADO
            return {"message": "The login '{}' already exists.".format(dados['login'])}

        # CASO USUÁRIO: NÃO CADASTRADO
        user = UserModel(**dados)

        try:
            # SALVANDO O HOTEL NO BANCO DE DADOS
            user.save_user()
            return user.json(), 201
        except:
            # INTERNAL SERVER ERROR
            return {"message": "An error ocurred trying to create hotel."}, 500


class UserLogin(Resource):

    """

        UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
        USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

        CONTÉM AS FUNÇÕES PARA OS USUÁRIOS:

        1) POST PARA REALIZAR LOGIN E OBTER O TOKEN DE AUTENTICAÇÃO

        AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
        ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
        REQUISIÇÃO HTTP COM A FLAG BEARER.

        # Arguments
            json_request            - Required : Contendo informações necessários na requisição (Json)

        # Returns
            json_response           - Required : Contendo o response da requisição (Json)

    """


    @classmethod
    def post(cls):

        # OBTENDO OS DADOS ENVIADOS POR JSON
        dados = atributos.parse_args()

        # VERIFICANDO SE O USUÁRIO JÁ EXISTE
        user = UserModel.find_by_login(dados['login'])

        try:
            # VERIFICANDO A VALIDAÇÃO DE EXISTÊNCIA DO USUÁRIO
            # VERIFICANDO A SENHA ENVIADA.
            if user and safe_str_cmp(user.senha, dados['senha']):

                # CASO AMBOS VÁLIDOS

                # TOKEN DE ACESSO CRIADO E ATRIBUÍDO AO USUÁRIO
                token_de_acesso = create_access_token(identity=user.user_id)

                # ENVIANDO O TOKEN AO USUÁRIO
                return {'access_token': token_de_acesso}, 200

            # CASO NÃO VÁLIDOS
            # UNAUTHORIZED
            return {'message': 'The username or password is incorrect.'}, 401
        except:
            # INTERNAL SERVER ERROR
            return {"message": "An error ocurred trying to create hotel."}, 500
