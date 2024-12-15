from config import settings
from database import MSSQLDatabase


def init_db_instance():
    return MSSQLDatabase()


def get_latest_date():
    conn = init_db_instance()
    query = f"""
    SELECT TOP 1 mtime
    FROM {settings.OUTPUT_TABLE}
    ORDER BY mtime DESC
    """
    date = conn.select_table(query)["mtime"].to_list()[0]
    return date
