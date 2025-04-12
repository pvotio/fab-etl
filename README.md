# First Abu Dhabi Bank SWIFT Message Loader

This application is designed to load SWIFT messages from an SFTP server belonging to the First Abu Dhabi Bank. It handles the fetching of SWIFT files, their transformation, and subsequent insertion into a Microsoft SQL Server database.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Setup](#setup)
  - [Pre-requisites](#pre-requisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Contributing](#contributing)

## Project Description

This project automates the process of fetching SWIFT messages from an SFTP server, parsing them, transforming the data, and inserting it into a specified table in a Microsoft SQL Server database.

## Features

- **SFTP Integration**: Securely connects to an SFTP server to download SWIFT message files.
- **SWIFT Message Parsing**: Automatically parses SWIFT messages using the MT940 format.
- **Data Transformation**: Transforms the parsed data to match the required database schema.
- **Database Insertion**: Inserts the transformed data into an SQL Server table.
- **SFTP Cleanup**: Automatically deletes processed files from the SFTP server after successful insertion.


## Setup

### Pre-requisites

- Python 3.x
- Microsoft SQL Server instance
- SFTP credentials for accessing the SWIFT message files

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pvotio/fab_etl
   cd fab
   ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

Set up the environment variables by renaming `.env.sample` to `.env` and filling in the following values:

- `LOG_LEVEL`: Level of logging (default: INFO)
- `OUTPUT_TABLE`: The name of the table where the transformed data will be inserted.
- `SFTP_HOST`: The host of the SFTP server.
- `SFTP_PORT`: The port of the SFTP server.
- `SFTP_USER`: The username for SFTP login.
- `SFTP_PASSWORD`: The password for SFTP login.
- `MSSQL_SERVER`: The SQL Server address.
- `MSSQL_DATABASE`: The database name in SQL Server.
- `MSSQL_USERNAME`: The username for SQL Server login.
- `MSSQL_PASSWORD`: The password for SQL Server login.


## Usage

1. Ensure that the environment variables are correctly configured.
2. Run the application:
    ```bash
    python main.py
    ```

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
