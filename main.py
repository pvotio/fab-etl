from client import Engine
from client.sftp import sftp_session
from client.utils import get_external_ip
from config import logger, settings
from database.helper import init_db_instance
from transformer import transform


def main():
    external_ip = get_external_ip()
    if external_ip:
        logger.info(f"Machine external IP address: {external_ip}")

    logger.info("Initializing FAB Client Engine")
    sftp, transport = sftp_session(
        host=settings.SFTP_HOST,
        port=settings.SFTP_PORT,
        username=settings.SFTP_USER,
        password=settings.SFTP_PASSWORD,
    )
    logger.info("Preparing Database Connection")
    engine = Engine(sftp, transport)
    parsed_data = engine.fetch()
    if not parsed_data:
        logger.warning("No data collected. terminating the application...")
        return

    logger.info("Transforming Data")
    df_transformed = transform(parsed_data)
    logger.info(f"Inserting Data into {settings.OUTPUT_TABLE}")
    logger.info(f"\n{df_transformed}")
    conn = init_db_instance()
    res = conn.insert_table(df_transformed, settings.OUTPUT_TABLE)
    if res:
        engine.delete_sftp_files()
        logger.info("Application completed successfully")

    return


if __name__ == "__main__":
    main()
