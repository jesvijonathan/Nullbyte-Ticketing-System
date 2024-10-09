# import os
# import time
# import ldap,ldap.asyncsearch
# from config import *
# from modules.log import *

class Lwrapper:
    def __init__(self):
        pass

    def getAllUsers(self)->list:
        return []
    def Authenticate(self,username,password)->bool:
        return True

# class Lwrapper:
#     def __init__(self):
#         self.admin = ADMIN_CRED["username"]
#         self.admin_pass = ADMIN_CRED["password"]

#     def getAllUsers(self)->list:
#         names = []
#         try:
#             conn = ldap.initialize('ldap://DC01.nullbyte.exe')
#             conn.protocol_version = 3
#             conn.set_option(ldap.OPT_REFERRALS, 0)
#             conn.simple_bind_s(self.admin, self.admin_pass)
#             logger.info("Successfully bound to the LDAP server.")
#         except ldap.LDAPError as e:
#             raise ConnectionError(f"Error Connecting To LDAP: {e}")
#         try:
#             s = ldap.asyncsearch.Dict(conn)
#             s.startSearch('DC=nullbyte,DC=exe',ldap.SCOPE_SUBTREE,'(&(objectClass=user)(objectCategory=person))',
#             )
#             while True:
#                 result = s.processResults()
#                 if result is not None:
#                     break
#                 time.sleep(1)
#             results = s.allEntries
#             if results:
#                 for entry in results:
#                     names.append(str(entry).split(',')[0][3:])
#         except ldap.LDAPError as e:
#            raise ChildProcessError(f"Error While Processing Results: {e}")
#         finally:
#             conn.unbind_s()
#         return names

#     def Authenticate(self,username,password)->bool:
#         if self.admin==username and self.admin_pass==password:
#             return True
#         elif ADMIN_CRED_2["username"]==username and ADMIN_CRED_2["password"]==password:
#             return True
#         conn = ldap.initialize('ldap://DC01.nullbyte.exe') 
#         conn.protocol_version = 3
#         conn.set_option(ldap.OPT_REFERRALS, 0)

#         try:
#             conn.simple_bind_s(username, password)
#             logger.info("Authentication successful.")
#             return True
#         except ldap.INVALID_CREDENTIALS:
#             logger.warning("Invalid credentials for user: %s", username)
#             return False
#         except ldap.LDAPError as e:
#             logger.error("LDAP error: %s", str(e))
#             return False
#         except Exception as e:
#             logger.error("An unexpected error occurred: %s", str(e))
#             return False
#         finally:
#             conn.unbind()