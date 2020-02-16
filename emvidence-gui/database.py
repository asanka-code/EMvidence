import sqlite3
from sqlite3 import Error
import time
import datetime

# a global variable of this module
database_name = r"emvidence-database.db"

def createDBConnection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

def closeDBConnection(conn):
    conn.close()

def updateLoginTimestamp(conn, user_id):
    # create timestamp
    timestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    sql = ''' UPDATE users SET last_login_timestamp=? WHERE id=?; '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp, user_id,))
    conn.commit()

def updateLogoutTimestamp(conn, user_id):
    # create timestamp
    timestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    sql = ''' UPDATE users SET last_logout_timestamp=? WHERE id=?; '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp, user_id,))
    conn.commit()

def createUser(conn, username, password, description):
    # user creation timestamp
    timestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # parameters to the SQL query
    admin_user = (username, password, description, timestamp, timestamp)

    sql = ''' INSERT INTO users(uname, password_hash, description, last_login_timestamp, last_logout_timestamp)
              VALUES(?,?,?,?,?); '''
    cur = conn.cursor()
    cur.execute(sql, admin_user)
    conn.commit()
    return cur.lastrowid

##############################################################

def createTable(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

def selectData(conn, task_id):
    sql = ''' SELECT * FROM tasks WHERE id=?; '''
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    task = cur.fetchone() #retrieve the first row
    print(task) #Print the first column retrieved(user's name)
    

def initializeDB(database_name):
    # database name    
    #database_name = r"emvidence-database.db"

    # tables
    sql_create_datasets_table = """ CREATE TABLE IF NOT EXISTS datasets (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        directory_path text NOT NULL,
                                        description text NOT NULL,                                        
                                        timestamp text NOT NULL,
                                        user_id integer NOT NULL,
                                        iot_device_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (id),
                                        FOREIGN KEY (iot_device_id) REFERENCES iotdevices (id)
                                    ); """
 
    sql_create_emtraces_table = """ CREATE TABLE IF NOT EXISTS emtraces (
                                        id integer PRIMARY KEY,
                                        filename text NOT NULL,
                                        hash_value text NOT NULL,                                    
                                        dataset_id integer NOT NULL,
                                        FOREIGN KEY (dataset_id) REFERENCES datasets (id)
                                ); """

    sql_create_iotdevices_table = """ CREATE TABLE IF NOT EXISTS iotdevices (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        description text NOT NULL
                                    ); """                            

    sql_create_modules_table = """ CREATE TABLE IF NOT EXISTS modules (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        description text NOT NULL,
                                        timestamp text NOT NULL,
                                        iot_device_id integer NOT NULL,
                                        FOREIGN KEY (iot_device_id) REFERENCES iotdevices (id)
                                    ); """                            

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        uname text NOT NULL,
                                        password_hash text NOT NULL,
                                        description text NOT NULL,
                                        last_login_timestamp text NOT NULL,
                                        last_logout_timestamp text NOT NULL                                       
                                    ); """                            

    # creating connection
    db_con = createDBConnection(database_name)
    if db_con is not None:
        print("Connection established...")

        # create tables
        createTable(db_con, sql_create_users_table)
        createTable(db_con, sql_create_iotdevices_table)
        createTable(db_con, sql_create_datasets_table)
        createTable(db_con, sql_create_emtraces_table)        
        createTable(db_con, sql_create_modules_table)         
        print("Tables are created...")

        # create the admin user
        createUser(db_con, 'admin', 'admin-hash', 'this is the admin')
        print("Created the admin user...")

    else:
        print("No DB connection!")

    # closing connection
    db_con.close()

########################################################

def testingDatabse():
    # initialize the database - only once
    #initializeDB(database_name)

    # open database connection
    db_con = createDBConnection(database_name)
    # updating the login timestamp
    updateLoginTimestamp(db_con, 1)
    # closing database connection
    closeDBConnection(db_con)

    time.sleep(10)

    # open database connection
    db_con = createDBConnection(database_name)
    # updating the login timestamp
    updateLogoutTimestamp(db_con, 1)
    # closing database connection
    closeDBConnection(db_con)