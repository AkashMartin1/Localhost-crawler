from sqlalchemy import create_engine, MetaData, Column, String, Integer, DateTime, Text, Table, Boolean
from sqlalchemy.engine.reflection import Inspector


class Database:
    def __init__(self):
        pass

    def connect(self):
        engine = create_engine('postgresql://admin:admin@localhost/search_engine', echo=True)
        engine.connect()
        inspector = Inspector.from_engine(engine)
        table_names = ["records", "domains", "trackers"]
        for table_name in table_names:
            if table_name not in inspector.get_table_names():
                print(table_name + " not exists")
                print("Creating " + table_name)
                metadata = MetaData(bind=engine)
                if table_name == "records":
                    main_table = Table(table_name, metadata,
                                       Column('id', Integer, primary_key=True, autoincrement='ignore_fk'),
                                       Column('title', String(100)),
                                       Column('meta_data', String(200)),
                                       Column('text', Text),
                                       Column('snapshot', Text),
                                       Column('url', Text),
                                       Column('updated_at', DateTime))
                    metadata.create_all()
                elif table_name == "domains":
                    main_table = Table(table_name, metadata,
                                       Column('id', Integer, primary_key=True, autoincrement='ignore_fk'),
                                       Column('name', String(100)),
                                       Column('disabled', Boolean),
                                       Column('Blocked', Boolean))
                    metadata.create_all()
                elif table_name == "trackers":
                    main_table = Table(table_name, metadata,
                                       Column('id', Integer, primary_key=True, autoincrement='ignore_fk'),
                                       Column('last_url', Text))
                    metadata.create_all()
        engine = create_engine('postgresql://admin:admin@localhost/search_engine', echo=True)
        return engine.connect()