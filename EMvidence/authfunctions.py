import database
import hashlib

#-------------------------------------------------------------------------------
def is_logged_in(cookie_value):
  return_value = False
  if (cookie_value=='logged-out' or cookie_value=='wrong-credentials' or cookie_value=='undefined' or cookie_value=='new'):
    return_value = False
  else:
    return_value = True
  return return_value

#-------------------------------------------------------------------------------
def is_passwd_correct(uname, passwd):
  '''
  This function takes a username and a password as parameters and lookup in the
  database. Returns true if the username and passwords matches. Returns false otherwise.
  '''

  # the value to return at the end
  return_value = False

  # open database connection
  db_con = database.createDBConnection(database.database_name)

  # Take the password hash of the user from database
  true_passwd_hash = database.getUserPasswordHash(db_con, str(uname))

  # check if the user exists
  if true_passwd_hash is None:
    return_value = False
  else:
    # hash the user entered password
    hasher = hashlib.sha1()
    hasher.update(passwd.encode('utf-8'))
    entered_passwd_hash = hasher.hexdigest()

    # Check if the passwords are correct
    if entered_passwd_hash == true_passwd_hash:
      # updating the login timestamp
      database.updateLoginTimestamp(db_con, 1)
      return_value = True
    else:
      return_value = False
  
  # closing database connection
  database.closeDBConnection(db_con)
  return return_value


