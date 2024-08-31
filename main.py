from client import Engine
from config import logger, settings
from database.helper import create_inserter_objects
from transformer import transform


def main():
    logger.info("Initializing FAB Client Engine")
    engine = Engine()
    parsed_data = engine.fetch()
    logger.info("Transforming Data")
    df_transformed = transform(parsed_data)
    logger.info("Preparing Database Inserter")
    inserter = create_inserter_objects(
        server=settings.MSSQL_SERVER,
        database=settings.MSSQL_DATABASE,
        username=settings.MSSQL_USERNAME,
        password=settings.MSSQL_PASSWORD,
    )
    logger.info(f"Inserting Data into {settings.OUTPUT_TABLE}")
    inserter.insert(df_transformed, settings.OUTPUT_TABLE)
    logger.info("Application completed successfully")
    return


if __name__ == "__main__":
    main()
