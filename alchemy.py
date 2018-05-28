from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:Stavstat12@127.0.0.1:3306/ga2')


class Admins(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    t_id = Column(Integer)
    name = Column(String(50))

    def __init__(self, t_id, name):
        self.t_id = t_id
        self.name = name

class Games(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(150))
    number_of_levels = Column(Integer)
    date = Column(DateTime)
    owner = Column(Integer)
    code = Column(String(50))
    #sequence = Column(String(50))

    def __init__(self, name, description, number_of_levels, date, owner, code):
        self.name = name
        self.description = description
        self.number_of_levels = number_of_levels
        self.date = date
        self.owner = owner
        self.code = code
        #self.sequence = sequence


class Levels(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    sn = Column(Integer)
    header = Column(String(50), nullable=True)
    task = Column(String(50), nullable=True)
    answer = Column(String(50), nullable=True)
    tip = Column(String(50), nullable=True)

    def __init__(self, game_id, sn, header, task, answer, tip):
        self.game_id = game_id
        self.sn = sn
        self.header = header
        self.task = task
        self.answer = answer
        self.tip = tip


class Gameplay(Base):
    __tablename__ = 'gameplay'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    game_id = Column(Integer)
    level_id = Column(Integer)
    #level = Column(Integer)
    start_time = Column(DateTime, nullable=True)
    finish_time = Column(DateTime, nullable=True)

    def __init__(self, chat_id, game_id, level_id, start_time, finish_time):
        self.game_id = game_id
        self.chat_id = chat_id
        self.level_id = level_id
        self.start_time = start_time
        self.finish_time = finish_time




Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)                           # Инициализация сессии
session = Session()


#session.add(Admins(235987482, 'beeline'))
#session.add(Games('ggg', 'ggg', 5, '2018-05-24 16:00:00', 235987482, 'IUP8W7'))



#session.commit()                                              # Запись в БД

#for i in session.query(Games).filter_by(owner=235987482).all():
#    print(i.id)

#s=session.query(Games).filter_by(owner=235987482).all()
#print(s[0].id)


#if i in session.query(Admins.id):
#    print('yes')

#print(list(session.query(Admins.id)))

#result = list(map(lambda x: x[0], session.query(Admins.id)))
#print(result)


#req = session.query(Levels).filter_by(id=17)
#game_id = req.first()

#print(game_id.game_id)
#req.delete()
