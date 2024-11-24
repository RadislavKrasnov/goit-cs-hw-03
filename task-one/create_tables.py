def create(conn):
    sql = """
    DROP TABLE IF EXISTS tasks;
    DROP TABLE IF EXISTS status;
    DROP TABLE IF EXISTS users;

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );

    CREATE TABLE status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );

    INSERT INTO status (name) 
    VALUES 
        ('new'),
        ('in progress'),
        ('completed');

    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES status (id),
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        cur.close()
