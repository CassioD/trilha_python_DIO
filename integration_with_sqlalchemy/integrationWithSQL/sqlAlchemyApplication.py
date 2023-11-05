from sqlalchemy import Column, create_engine, inspect, select, func
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey

Base = declarative_base()


class Client(Base):
    __tablename__ = "client_account"  # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(9))
    address = Column(String)

    accounts = relationship(
        "Account", back_populates="client", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (f"Client("
                f"id = {self.id},"
                f"Name = {self.name},"
                f"cpf = {self.cpf},"
                f"address = {self.address}")


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agency = Column(String)
    num = Column(Integer)
    client_id = Column(Integer, ForeignKey("client_account.id"), nullable=False)
    saldo = Column(DECIMAL)

    client = relationship("Client", back_populates="accounts")

    def __repr__(self):
        return (f"Account ("
                f"id = {self.id},"
                f"Tipo = {self.tipo},"
                f"Agência = {self.agency},"
                f"Número = {self.num},"
                f"Saldo = {self.saldo})")


print(Account.__tablename__)
print(Client.__tablename__)

# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# depreciado - será removido em um futuro release
# print(engine.table_name())

inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("client_account"))

print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    cassio = Client(
        name='Cássio',
        cpf='123456789',
        address= 'Rua dos maridos',
    )

    sandy = Client(
        name= 'Sandy',
        cpf= '987654321',
        address= 'Rua Amoreira'
    )

    patrick = Client(
        name='Patrick',
        cpf='741285963',
        address= 'Rua Bartolomeu'
    )

    # enviando para o BD (persistência de dados)
    session.add_all([cassio, sandy, patrick])

    session.commit()

stmt = select(Client).where(Client.name.in_(['cassio', 'sandy', 'patrick']))
print('\nRecuperando usuários a partir de condição de filtragem')
for client in session.scalars(stmt):
    print(client)

stmt_address = select(Account).where(Account.client_id.in_([2]))
print('\nRecuperando os endereços de email do usuário')
for account in session.scalars(stmt_address):
    print(account)

order_stmt = select(Client).order_by(Client.name.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(order_stmt):
    print(result)

stmt_join = select(Client.name, Account.saldo).join_from(Account, Client)
for result in session.scalars(stmt_join):
    print(result)


connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("Executando statment a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Client)
print('Total de instâncias em Client')
for result in session.scalars(stmt_count):
    print(result)
