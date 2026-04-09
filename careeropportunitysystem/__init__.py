import pymysql

# This tricks Django into thinking the mysqlclient version is 2.2.1
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()