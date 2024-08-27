from psycopg2 import connect
from env import port, host, database, user, password

def create_tables():
    with connect(
        port=port, 
        host=host, 
        database=database, 
        user=user, 
        password=password
    ) as conn:
        
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(
                """
                create table messages(
                id bigserial not null primary key,
                title varchar(50) not null,
                content text not null
                );
                """
            )

            cur.execute(
                """
                create table tasks(
                id bigserial not null primary key,
                title varchar(50) not null,
                content text,
                checked boolean not null
                );
                """
            )

            cur.execute(
                """
                insert into messages (title, content) 
                values 
                ('Breakfast', 'Eggs, bread, milk'),
                ('Sport', 'Football, basketball, formula 1');
                """
            )

            cur.execute(
                """
                insert into tasks (title, checked) 
                values 
                ('Make breakfast', TRUE),
                ('Play football', FALSE);
                """
            )

            cur.execute('select * from messages')

            messages = cur.fetchall()

            cur.execute('select * from tasks')

            tasks = cur.fetchall()

            print(f'{messages=}, {tasks=}')


def get_messages():
    with connect(
        port=port, 
        host=host, 
        database=database, 
        user=user, 
        password=password
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM messages")
            rows = cur.fetchall()

            description = cur.description

            if (not rows) or description is None:
                return []

            colnames = [desc[0] for desc in description]

            messages = [dict(zip(colnames, row)) for row in rows]

            return messages



def add_message(message):
    with connect(
        port=port, 
        host=host, 
        database=database, 
        user=user, 
        password=password
    ) as conn:
        with conn.cursor() as cur:
            title = message['title']    
            content = message['content']    
            cur.execute(
                """
                insert into messages (title, content)
                values (%s, %s)
                """, (title, content)
            )

            conn.commit()

            return get_messages()

def delete_message(message_id):
    with connect(
        port=port, 
        host=host, 
        database=database, 
        user=user, 
        password=password
    ) as conn:
        
        with conn.cursor() as cur:
            cur.execute('delete from messages where id = %s;', (message_id,))

            conn.commit()
            
            return get_messages()


def get_tasks():
    with connect(
        port=port, 
        host=host, 
        database=database, 
        user=user, 
        password=password
    ) as conn:

        with conn.cursor() as cur:
            cur.execute('select * from tasks;')

            rows = cur.fetchall()

            description = cur.description

            if (not rows) or description is None:
                return []
            
            colnames = [desc[0] for desc in description]

            tasks = [dict(zip(colnames, row)) for row in rows]

            conn.commit()

            return tasks



def add_task(task):
    with connect(
        port=port, 
        host=host, 
        database=database, 
        user=user, 
        password=password
    ) as conn:
        with conn.cursor() as cur:
            title = task['title']    
            # content = task['content']
            checked = task['checked']    
            cur.execute(
                """
                insert into tasks (title, checked)
                values (%s, %s)
                """, (title, checked)
            )

            conn.commit()

            return get_tasks()

def delete_task(task_id):
    with connect(
        port=port, 
        host=host, 
        database=database, 
        user=user, 
        password=password
    ) as conn:
        
        with conn.cursor() as cur:
            cur.execute('delete from tasks where id = %s;', (task_id,))

            conn.commit()
            
            return get_tasks()




if __name__ == '__main__':
    create_tables()
