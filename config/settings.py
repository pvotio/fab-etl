from decouple import config

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
OUTPUT_TABLE = config("OUTPUT_TABLE")
INSERTER_MAX_RETRIES = config("INSERTER_MAX_RETRIES", default=3, cast=int)
SFTP_HOST = config("SFTP_HOST")
SFTP_PORT = config("SFTP_PORT", cast=int)
SFTP_USER = config("SFTP_USER")
SFTP_PASSWORD = config("SFTP_PASSWORD")
MSSQL_SERVER = config("MSSQL_SERVER")
MSSQL_AD_LOGIN = config("MSSQL_AD_LOGIN", cast=bool, default=False)
MSSQL_DATABASE = config("MSSQL_DATABASE")

if not MSSQL_AD_LOGIN:
    MSSQL_USERNAME = config("MSSQL_USERNAME")
    MSSQL_PASSWORD = config("MSSQL_PASSWORD")
