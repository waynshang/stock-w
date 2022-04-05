from sqlite3 import connect
def create_table(connection, cursor, table_name, columns):
  cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
  connection.commit()

def insert_value(connection, cursor, table_name, columns, values):
  insert_string = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({values})"
  print(insert_string)
  cursor.execute(insert_string)
  connection.commit()

def insert_values(connection, cursor, table_name, columns, numbers, values):
  cursor.executemany(f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({numbers})", values)
  connection.commit()

def update_values(connection, cursor, table_name, update_values, where_condition):
  cursor.execute(f"UPDATE {table_name} SET {update_values} WHERE {where_condition}")
  connection.commit()  
 
def select_values(connection, cursor, table_name, columns, where_condition):
  rows = cursor.execute(f"SELECT {columns} from {table_name} where {where_condition}").fetchall()
  if not rows: return []
  return rows[0]

def init_db(db_name):
  connection = connect(db_name)
  return connection

