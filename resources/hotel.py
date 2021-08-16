"""

    UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
    USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

    CONTÉM OS RECURSOS DISPONÍVEIS PARA A CLASSE DE HOTÉIS:

    1) GET DE TODOS OS HOTÉIS CADASTRADOS
    2) GET DE UM HOTEL ESPECíFICO
    3) POST PARA CADASTRO DE UM NOVO HOTEL
    4) PUT PARA ALTERAÇÃO DE UM HOTEL EXISTENTE
    5) DEL PARA DELETAR UM HOTEL.

    AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
    ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
    REQUISIÇÃO HTTP COM A FLAG BEARER.

    # Arguments
        json_request            - Required : Contendo informações necessários na requisição (Json)

    # Returns
        json_response           - Required : Contendo o response da requisição (Json)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "16/08/2021"


from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.hotel import HotelModel


class Hoteis(Resource):

    """

        UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
        USO DE SQLALCHEMY PARA BANCO DE DADOS.

        CONTÉM AS FUNÇÕES PARA OS HOTÉIS:

        1) GET DE TODOS OS HOTÉIS CADASTRADOS

        # Arguments
            json_request            - Required : Contendo informações necessários na requisição (Json)

        # Returns
            json_response           - Required : Contendo o response da requisição (Json)

    """


    def get(self):

        """

            FUNÇÃO GET PARA OBTER OS HOTÉIS CADASTRADOS

            # Arguments

            # Returns
                json_response           - Required : Todos os hotéis cadastrados (Json)

        """

        # OBTENDO TODAS OS HOTEIS
        # SEMELHANTE A UM SELECT * FROM hoteis
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    """

        UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
        USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

        CONTÉM AS FUNÇÕES PARA OS HOTÉIS:

        1) GET DE UM HOTEL ESPECíFICO
        2) POST PARA CADASTRO DE UM NOVO HOTEL
        3) PUT PARA ALTERAÇÃO DE UM HOTEL EXISTENTE
        4) DEL PARA DELETAR UM HOTEL.

        AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
        ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
        REQUISIÇÃO HTTP COM A FLAG BEARER.

        # Arguments
            json_request            - Required : Contendo informações necessários na requisição (Json)

        # Returns
            json_response           - Required : Contendo o response da requisição (Json)

    """

    # OBTENDO OS VALORES ENVIADOS NO JSON_REQUEST.
    # OBTENDO INFORMAÇÕES DE: NOME, ESTRELAS, DIARIA E CIDADE.
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')


    def get(self, hotel_id):

        """

            FUNÇÕES GET PARA OBTER UM HOTEL ESPECÍFICO.

            # Arguments
                hotel_id               - Required : O ID do hotel desejado.
                                                    É enviado via URL (String)

            # Returns
                json_response           - Required : O hotel cadastrado ou o
                                                     hotel não existe (Json)

        """

        # BUSCANDO O HOTEL ENVIADO
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            # CASO O HOTEL: ENCONTRADO
            return hotel.json()
        # CASO O HOTEL: NÃO ENCONTRADO
        return {'message': 'Hotel not found.'}, 404


    @jwt_required
    def post(self, hotel_id):

        """

            FUNÇÃO POST PARA CADASTRAR UM NOVO HOTEL.
            USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

            AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
            ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
            REQUISIÇÃO HTTP COM A FLAG BEARER.

            # Arguments
                hotel_id               - Required : O ID do hotel desejado.
                                                    É enviado via URL (String)

            # Returns
                json_response           - Required : Validador de execução da função (Json)

        """

        # VERIFICANDO SE O HOTEL JÁ EXISTE
        if HotelModel.find_hotel(hotel_id):
            # CASO HOTEL: CADASTRADO
            # BAD REQUEST
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400

        # CASO HOTEL: NÃO CADASTRADO
        # OBTENDO OS DADOS ENVIADOS POR JSON
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        try:
            # SALVANDO O HOTEL NO BANCO DE DADOS
            hotel.save_hotel()
            return hotel.json(), 201
        except:
            # INTERNAL SERVER ERROR
            return {"message": "An error ocurred trying to create hotel."}, 500


    @jwt_required
    def put(self, hotel_id):

        """

            FUNÇÃO PUT PARA ATUALIZAR INFORMAÇÕES OU CADASTRAR UM HOTEL.
            USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

            AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
            ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
            REQUISIÇÃO HTTP COM A FLAG BEARER.

            # Arguments
                hotel_id               - Required : O ID do hotel desejado.
                                                    É enviado via URL (String)

            # Returns
                json_response           - Required : Validador de execução da função (Json)

        """

        # OBTENDO OS DADOS ENVIADOS POR JSON
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        # BUSCANDO O HOTEL ENVIADO
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        try:
            if hotel_encontrado:
                # CASO HOTEL: ENCONTRADO
                # REALIZA-SE O UPDATE DAS INFORMAÇÕES DO HOTEL
                hotel_encontrado.update_hotel(**dados)
                hotel_encontrado.save_hotel()
                return hotel_encontrado.json(), 200

            # CASO HOTEL: NÃO ENCONTRADO
            # REALIZE-SE O CADASTRO DO HOTEL
            # SALVANDO O HOTEL NO BANCO DE DADOS
            hotel.save_hotel()
            return hotel.json(), 201
        except:
            # INTERNAL SERVER ERROR
            return {"message": "An error ocurred trying to create hotel."}, 500


    @jwt_required
    def delete(self, hotel_id):

        """

            FUNÇÃO DELETE PARA DELETAR UM HOTEL.
            USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

            AO FAZER LOGIN, UM TOKEN JWT DE AUTENTICAÇÃO É CRIADO E RETORNADO PARA O CLIENT.
            ESSE TOKEN DEVE SER ENVIADO PARA AS VIEWS ATRAVÉS DO HEADER AUTHORIZATION DE CADA
            REQUISIÇÃO HTTP COM A FLAG BEARER.

            # Arguments
                hotel_id               - Required : O ID do hotel desejado.
                                                    É enviado via URL (String)

            # Returns
                json_response           - Required : Validador de execução da função (Json)

        """

        # BUSCANDO O HOTEL ENVIADO
        hotel = HotelModel.find_hotel(hotel_id)

        try:
            if hotel:
                # CASO HOTEL: ENCONTRADO
                # REALIZA-SE O DELETE DO HOTEL
                hotel.delete_hotel()
                return {'message': 'Hotel deleted.'}

            # CASO HOTEL: NÃO ENCONTRADO
            return {'message': 'Hotel not found.'}, 404
        except:
            # INTERNAL SERVER ERROR
            return {"message": "An error ocurred trying to create hotel."}, 500
