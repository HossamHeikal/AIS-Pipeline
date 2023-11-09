from airflow.www.security import SecureView
from flask_appbuilder.security.manager import AUTH_DB

AUTH_TYPE = AUTH_DB

# Create an admin user
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Admin"
AUTH_LDAP_SERVER = "ldap://ldapserver"
AUTH_LDAP_USE_TLS = False
AUTH_LDAP_SEARCH = "dc=example,dc=com"
AUTH_LDAP_BIND_USER = "cn=admin,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "password"

ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin"
