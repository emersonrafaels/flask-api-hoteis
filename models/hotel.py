"""

    UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
    USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

    CONTÉM O MODELO DE DADOS PARA A CLASSE HOTÉIS.

    CONFIGURA O BANCO DE DADOS E A TIPAGEM DOS DADOS DA CLASSE.

    # Arguments
        json_request            - Required : Contendo informações necessários na requisição (Json)

    # Returns
        json_response           - Required : Contendo o response da requisição (Json)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "16/08/2021"


from sql_alchemy import banco


class HotelModel(banco.Model):

    """

        UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
        USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

        CONTÉM O MODELO DE DADOS PARA A CLASSE HOTÉIS.

        CONFIGURA O BANCO DE DADOS E A TIPAGEM DOS DADOS DA CLASSE.

        # Arguments
            json_request            - Required : Contendo informações necessários na requisição (Json)

        # Returns
            json_response           - Required : Contendo o response da requisição (Json)

    """

    # INICIANDO O NOME DA TABELA NO BANCO DE DADOS
    __tablename__ = 'hoteis'

    # CONFIGURANDO AS COLUNAS DO BANCO DE DADOS E AS TIPAGENS
    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))


    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):

        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade


    def json(self):

        """

            RETORNANDO OS DADOS DO HOTEL EM FORMATO JSON.

            # Arguments
                json_request            - Required : Contendo informações necessários na requisição (Json)

            # Returns
                json_response           - Required : Contendo o response da requisição (Json)

        """

        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }


    @classmethod
    def find_hotel(cls, hotel_id):

        """

            REALIZANDO A QUERY NO BANCO DE DADOS EM BUSCA DO HOTEL REQUISITADO.

            # Arguments
                hotel_id               - Required : ID do hotel requisitado (String)

            # Returns
                json_response           - Required : Contendo o response da requisição (Json)

        """

        try:
            hotel = cls.query.filter_by(hotel_id=hotel_id).first()
            if hotel:
                return hotel
            return None
        except:
            return None


    def save_hotel(self):

        banco.session.add(self)
        banco.session.commit()


    def update_hotel(self, nome, estrelas, diaria, cidade):

        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade


    def delete_hotel(self):

        banco.session.delete(self)
        banco.session.commit()
