import time
import ldap,ldap.asyncsearch
from config import *
from log import *


class Lwrapper:
    def __init__(self):
        self.admin = ADMIN_CRED['username']
        self.admin_pass = ADMIN_CRED["password"]
        self.svc = SVC_CRED['username']
        self.svc_pass = SVC_CRED["password"]
    def _connect(self, user: str = None, password: str = None):
        try:
            conn = ldap.initialize('ldap://DC01.nullbyte.exe')
            conn.protocol_version = 3
            conn.set_option(ldap.OPT_REFERRALS, 0)
            user = user if user else self.svc
            password = password if password else self.svc_pass
            conn.simple_bind_s(user,password)
            logger.info("Successfully bound to the LDAP server.")
            return conn
        except ldap.LDAPError as e:
            logger.info(f"LDAP error: {e}")
            return

    def getPayload(self,username)->dict:
        # remove in future
        if self.admin==username:
            return {'username':'Administrator','ou':[],'upn':'Administrator@nullbyte.exe'}
        # until here
        response={}
        conn = self._connect()
        base_dn = 'DC=nullbyte,DC=exe'
        search_filter = '(&(objectClass=user)(objectCategory=person)(userPrincipalName='+username+'))'
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, ['name'])
        if result:
            for dn, entry in result:
                if dn!=None:
                    name=entry['name'][0].decode('utf-8')
                    ou=[part.split('=')[1] for part in dn.split(',') if part.startswith('OU=')]
                    response['username']=name
                    response['ou']=ou if ou else []
                    response['upn']=username
        conn.unbind()     
        return response
    
    def getAllUsers(self)->list:
        names = []
        conn=self._connect
        try:
            s = ldap.asyncsearch.Dict(conn)
            s.startSearch('DC=nullbyte,DC=exe',ldap.SCOPE_SUBTREE,'(&(objectClass=user)(objectCategory=person))',)
            while True:
                result = s.processResults()
                if result is not None:
                    break
                time.sleep(1)
            results = s.allEntries
            if results:
                for entry in results:
                    names.append(str(entry).split(',')[0][3:])
        except ldap.LDAPError as e:
           raise ChildProcessError(f"Error While Processing Results: {e}")
        finally:
            conn.unbind_s()
        return names

    def Authenticate(self,username,password)->bool:
        #remove in future
        if self.admin==username and self.admin_pass==password:
            return True
        # until here
        conn = ldap.initialize('ldap://DC01.nullbyte.exe') 
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)

        try:
            conn.simple_bind_s(username, password)
            logger.info("Authentication successful.")
            return True
        except ldap.INVALID_CREDENTIALS:
            logger.warning("Invalid credentials for user: %s", username)
            return False
        except ldap.LDAPError as e:
            logger.error("LDAP error: %s", str(e))
            return False
        except Exception as e:
            logger.error("An unexpected error occurred: %s", str(e))
            return False
        finally:
            conn.unbind()