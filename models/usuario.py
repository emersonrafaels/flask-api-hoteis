"""

    UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
    USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

    CONTÉM O MODELO DE DADOS PARA A CLASSE USUÁRIOS.

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


class UserModel(banco.Model):

    """

        UTILIZAÇÃO DO MICROFRAMEWORK FLASK PARA CRIAÇÃO DE UMA API DE HOTÉIS.
        USO DE SQLALCHEMY PARA BANCO DE DADOS E JWT PARA AUTENTICAÇÃO.

        CONTÉM O MODELO DE DADOS PARA A CLASSE USUÁRIOS.

        CONFIGURA O BANCO DE DADOS E A TIPAGEM DOS DADOS DA CLASSE.

        # Arguments
            json_request            - Required : Contendo informações necessários na requisição (Json)

        # Returns
            json_response           - Required : Contendo o response da requisição (Json)

    """


    # INICIANDO O NOME DA TABELA NO BANCO DE DADOS
    __tablename__ = 'usuarios'

    # CONFIGURANDO AS COLUNAS DO BANCO DE DADOS E AS TIPAGENS
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))


    def __init__(self, login, senha):

        self.login = login
        self.senha = senha


    def json(self):

        """

            RETORNANDO OS DADOS DO USUÁRIO EM FORMATO JSON.

            # Arguments
                json_request            - Required : Contendo informações necessários na requisição (Json)

            # Returns
                json_response           - Required : Contendo o response da requisição (Json)

        """

        return {
            'user_id': self.user_id,
            'login': self.login
            }


    @classmethod
    def find_user(cls, user_id):

        """

            REALIZANDO A QUERY NO BANCO DE DADOS EM BUSCA DO USUÁRIO REQUISITADO.

            # Arguments
                user_id                - Required : ID do usuário requisitado (Integer)

            # Returns
                json_response           - Required : Contendo o response da requisição (Json)

        """

        try:
            user = cls.query.filter_by(user_id=user_id).first()
            if user:
                return user
            return None
        except:
            return None


    @classmethod
    def find_by_login(cls, login):

        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None


    def save_user(self):

        banco.session.add(self)
        banco.session.commit()


    def delete_user(self):

        banco.session.delete(self)
        banco.session.commit()
