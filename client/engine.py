import os

import mt940

from client import utils
from config import logger
from database.helper import get_latest_date


class Engine:

    DIR = "/outgoing"

    def __init__(self, sftp, transport):
        self.sftp = sftp
        self.transport = transport
        self.sftp_files = []
        self.raw_data = {}
        self.parsed_data = []

    def fetch(self):
        logger.info("Fetching files started.")
        self.load_sftp_files()
        self.read_sftp_files()
        self.parse()
        if not len(self.parsed_data):
            return False

        logger.info("Fetching files completed.")
        return self.parsed_data

    def load_sftp_files(self):
        logger.info("Loading SFTP files from directory: %s", self.DIR)
        files = self.sftp.listdir_attr(self.DIR)
        logger.info("SFTP files loaded from directory: %s", self.DIR)
        for file in files:
            if file.filename.endswith(".txt"):
                self.sftp_files.append(
                    (os.path.join(self.DIR, file.filename), file.st_mtime)
                )
                logger.debug("Added file: %s", file)

        self.sftp_files = sorted(self.sftp_files, key=lambda x: x[1])
        logger.info("Total files loaded: %d", len(self.sftp_files))
        return

    def skip_sftp_processed_files(self):
        try:
            last_mtime = get_latest_date()
            logger.debug(f"Most recent mtime: {last_mtime}")
            if self.sftp_files[-1][1] == last_mtime:
                return -1

            for i, (_, mtime) in enumerate(self.sftp_files):
                if mtime > last_mtime:
                    return i

        except Exception as e:
            logger.error(f"Error fetching or processing mtime: {str(e)}")
            return False

    def read_sftp_files(self):
        # skip_idx = self.skip_sftp_processed_files()
        # if not skip_idx:
        #     skip_idx = 0
        #     logger.info(f"No previous record found on database")
        #     logger.info(f"No skip strategy taken")
        # elif skip_idx == -1:
        #     logger.info(f"No new file detected on SFTP server")
        #     return
        # logger.info(f"Skip index: {skip_idx}")

        logger.info("Reading SFTP files.")
        for file, mtime in self.sftp_files:
            logger.debug("Reading file: %s", file)
            with self.sftp.open(file, "r") as f:
                self.raw_data[file] = (mt940.parse(f.read()), mtime)
                logger.debug("File read and parsed: %s", file)

        logger.info("All SFTP files have been read.")
        return

    def delete_sftp_files(self):
        num = 0
        logger.info("Deleting downloaded files from SFTP server")
        for file, _ in self.sftp_files:
            try:
                self.sftp.remove(file)
                num += 1
            except Exception as e:
                logger.error(f"Unable to delete {file} from SFTP server: {e}")

        logger.info(
            f"{num} out of {len(self.sftp_files)} files deleted from SFTP server"
        )

    def parse(self):
        logger.info("Parsing raw data.")
        for file, (d, mtime) in self.raw_data.items():
            trxs = {
                **utils.statement_to_dict(d.data),
                "file_name": os.path.basename(file),
                "mtime": mtime,
            }
            if len(d):
                for trx in d:
                    self.parsed_data.append(
                        {**trxs, **utils.transaction_to_dict(trx.data)}
                    )
                    logger.debug("Transaction parsed from file: %s", file)
            else:
                self.parsed_data.append(trxs)
                logger.debug("No transactions found in file: %s", file)

        logger.info(
            "Parsing completed. Total transactions parsed: %d", len(self.parsed_data)
        )
        return
