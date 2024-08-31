from client import sftp, utils
from config import logger


class Engine:

    def __init__(self):
        self.sftp_files = []
        self.raw_data = {}
        self.parsed_data = []

    def fetch(self):
        self.load_sftp_files()
        self.read_sftp_files()
        self.parse()
        return self.parsed_data

    def load_sftp_files(self):
        pass

    def read_sftp_files(self):
        pass

    def parse(self):
        for _, d in self.raw_data.items():
            trxs = utils.statement_to_dict(d.data)
            if len(d):
                for trx in d:
                    self.parsed_data.append(
                        {**trxs, **utils.transaction_to_dict(trx.data)}
                    )
            else:
                self.parsed_data.append(trxs)
