def execute(conn):
    cur = conn.cursor()
    try:
        print('1. Отримати всі завдання певного користувача.')
        print(getUserTasks(cur, 5))

        print('\n2. Вибрати завдання за певним статусом')
        print(getTasksByStatus(cur, 'completed'))

        print('\n3. Оновити статус конкретного завдання.')
        print('Before')
        print(getTaskById(cur, 2))
        print('After')
        print(updateTaskStatus(cur, 2, 'in progress'))

        print('\n4. Отримати список користувачів, які не мають жодного завдання.')
        print(getUsersWithoutTasks(cur))

        print('\n5. Додати нове завдання для конкретного користувача.')
        print(addUserTask(cur, ('New Task', 'Task description', 'new', 7)))
        
        print('\n6. Отримати всі завдання, які ще не завершено.')
        print(getIncompleteTasks(cur))

        print('\n7. Видалити конкретне завдання.')
        print(deleteTaskById(cur, 20))

        print('\n8. Знайти користувачів з певною електронною поштою.')
        print(getUsersByEmail(cur, 'example.com'))


        print('\n9. Оновити ім\'я користувача.')
        print('Before')
        print(getUserById(cur, 1))
        print('After')
        print(updateUserName(cur, 1, 'TEST'))

        print('\n10. Отримати кількість завдань для кожного статусу')
        print(getTasksQtyByStatus(cur))

        print('\n11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.')
        print(getTasksByUserEmail(cur, 'example.com'))

        print('\n12. Отримати список завдань, що не мають опису')
        setTaskDescription(cur, 4, None)
        print(getTasksWithoutDescription(cur))

        print('\n13. Вибрати користувачів та їхні завдання, які є у статусі \'in progress\'')
        print(getTasksAndUsersByTaskStatus(cur, 'in progress'))

        print('\n14. Вибрати користувачів та їхні завдання, які є у статусі ')
        print(getUsersTasksQty(cur))

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()

def getTaskById(cur, id):
    sql = "SELECT * FROM tasks WHERE id = %s"
    cur.execute(sql, (id,))
    return cur.fetchone()

def getUserById(cur, id):
    sql = "SELECT * FROM users WHERE id = %s"
    cur.execute(sql, (id,))
    return cur.fetchone()

def getUserTasks(cur, user_id):
    sql = "SELECT * FROM tasks WHERE user_id = %s;"
    cur.execute(sql, (user_id,))
    return cur.fetchone()

def getTasksByStatus(cur, status):
    sql = """
    SELECT * 
    FROM tasks
    WHERE status_id = (
        SELECT id 
        FROM status 
        WHERE name = %s
    );
    """
    cur.execute(sql, (status,))
    return cur.fetchall()

def updateTaskStatus(cur, task_id, newStatus):
    sql = """
    UPDATE tasks
    SET status_id = (
        SELECT id 
        FROM status 
        WHERE name = %s
    )
    WHERE id = %s
    RETURNING tasks.*;
    """
    cur.execute(sql, (newStatus, task_id,))
    return cur.fetchone()

def getUsersWithoutTasks(cur):
    sql = """
    SELECT * 
    FROM users
    WHERE id NOT IN (
        SELECT DISTINCT user_id 
        FROM tasks
    );
    """
    cur.execute(sql)
    return cur.fetchall()

def addUserTask(cur, newTask):
    sql = """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, 
            (SELECT id FROM status WHERE name = %s), 
            %s)
    RETURNING tasks.*;
    """
    cur.execute(sql, newTask)
    return cur.fetchone()

def getIncompleteTasks(cur):
    sql = """
    SELECT * 
    FROM tasks
    WHERE status_id != (
        SELECT id 
        FROM status 
        WHERE name = 'completed'
    );
    """
    cur.execute(sql)
    return cur.fetchall()

def deleteTaskById(cur, task_id):
    sql = "DELETE FROM tasks WHERE id = %s;"
    cur.execute(sql, (task_id, ))
    return f'Task with id {task_id} deleted'

def getUsersByEmail(cur, email):
    pattern = f"%{email}%"
    sql = """
    SELECT * 
    FROM users
    WHERE email LIKE %s;
    """
    cur.execute(sql, (pattern,))
    return cur.fetchall()

def updateUserName(cur, user_id, newName):
    sql = """
    UPDATE users
    SET fullname = %s
    WHERE id = %s
    RETURNING users.*;
    """
    cur.execute(sql, (newName, user_id,))
    return cur.fetchone()

def getTasksQtyByStatus(cur):
    sql = """
    SELECT s.name AS status_name, COUNT(t.id) AS task_count
    FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name;
    """
    cur.execute(sql)
    return cur.fetchall()

def getTasksByUserEmail(cur, email):
    pattern = f"%{email}%"
    sql = """
    SELECT t.*
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s;
    """
    cur.execute(sql, (pattern,))
    return cur.fetchall()

def setTaskDescription(cur, task_id, description):
    sql = "UPDATE tasks SET description = %s where id = %s"
    cur.execute(sql, (description, task_id))

def getTasksWithoutDescription(cur):
    sql = """
    SELECT * 
    FROM tasks
    WHERE description IS NULL OR description = '';
    """
    cur.execute(sql)
    return cur.fetchone()

def getTasksAndUsersByTaskStatus(cur, status):
    sql = """
    SELECT u.fullname, t.title, t.description
    FROM users u
    INNER JOIN tasks t ON u.id = t.user_id
    WHERE t.status_id = (
        SELECT id 
        FROM status 
        WHERE name = %s
    );
    """
    cur.execute(sql, (status,))
    return cur.fetchall()

def getUsersTasksQty(cur):
    sql = """
    SELECT u.fullname, COUNT(t.id) AS task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id;
    """
    cur.execute(sql)
    return cur.fetchall()
