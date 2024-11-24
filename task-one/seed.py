from faker import Faker
from random import randint, choice

def seed_db(conn):
    cur = conn.cursor()
    try:
        fake = Faker()
        populate_users(cur, fake, 10)
        populate_tasks(cur, fake, 20)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()

def populate_users(cur, fake, n):
    usersList = []
    for _ in range(n):
        name = fake.name()
        email = fake.email()
        usersList.append([name, email])
    users = tuple(map(tuple, usersList))
    cur.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s);", users)

def populate_tasks(cur, fake, n):
    cur.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cur.fetchall()]
    taskList = []
    for _ in range(n):
        title = fake.sentence()
        description = fake.text()
        status_id = randint(1, 3)
        user_id = choice(user_ids)
        taskList.append([title, description, status_id, user_id])
    tasks = tuple(map(tuple, taskList))
    cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);", tasks)
