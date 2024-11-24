from connector import create_connection 
import create_tables
import seed
import queries

if __name__ == '__main__':
     with create_connection() as conn:
        if conn is not None:
            create_tables.create(conn)
            seed.seed_db(conn)
            queries.execute(conn)
        else:
            print("Error! cannot create the database connection.")
