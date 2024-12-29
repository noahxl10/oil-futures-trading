from sqlalchemy import create_engine, engine
import models


# connect_tcp_socket initializes a TCP connection pool
# for a Cloud SQL instance of Postgres.
class DB:

    def __init__(self):

        db_host = ''
        db_user = ''
        db_pass = ''
        db_name = ''
        db_port = ''

        self.engine = create_engine(
            engine.url.URL.create(
                drivername="postgresql",
                username=db_user,
                password=db_pass,
                host=db_host,
                port=db_port,
                database=db_name,
            ),
        )
        

    def setup(self):
        models.Base.metadata.create_all(self.engine)
