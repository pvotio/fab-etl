# FAB MT940 ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline that securely connects to an SFTP server to retrieve **MT940 financial statement files**, parses and transforms the content into structured data, and loads the result into a **Microsoft SQL Server** database.

## Overview

### Purpose

This pipeline automates the processing of MT940 files typically used in financial transaction reporting. It is designed to:
- Retrieve `.txt` files in MT940 format from a secure SFTP server.
- Parse and normalize banking statement and transaction records.
- Enrich with metadata (e.g., filename, modified time).
- Insert the result into a relational SQL Server table.

This is especially useful for compliance reporting, account reconciliation, and financial data aggregation tasks.

## Source of Data

All data comes from an SFTP endpoint hosted by the **FAB (First Abu Dhabi Bank)** or another entity serving MT940 exports. Key details:

- Files reside in the `/outgoing` directory.
- Each file follows the MT940 SWIFT format and is parsed using the `mt-940` library.
- Timestamp-based filtering is used to avoid reprocessing files.

Access to the server requires valid credentials and whitelisted IPs.

## Application Flow

The main process, executed from `main.py`, includes:

1. **External IP Logging**:
   - Retrieves and logs the machine’s external IP for traceability.

2. **Connect to SFTP**:
   - Establishes an authenticated session using `paramiko`.

3. **Read MT940 Files**:
   - Loads `.txt` files, reads content, and parses each into statements and transaction rows.

4. **Parse & Transform**:
   - MT940 fields are decoded into a normalized dictionary via a custom transformer.

5. **Insert into SQL Server**:
   - Results are inserted into the table defined by `OUTPUT_TABLE`.
   - Previously inserted files are tracked using `mtime` (last-modified timestamp).

6. **Cleanup**:
   - Successfully processed files are deleted from the server to prevent duplication.

## Project Structure

```
fab-etl-main/
├── client/               # SFTP and MT940 logic
│   ├── engine.py         # Fetch, parse, and manage ETL state
│   └── sftp.py           # Secure connection handler
├── config/               # Logging and settings loader
├── database/             # SQL Server interface helpers
├── transformer/          # Data transformation utilities
├── main.py               # Entrypoint for pipeline
├── .env.sample           # Environment config template
├── Dockerfile            # Containerization support
```

## Environment Variables

Create a `.env` file based on `.env.sample`. Key fields:

| Variable | Description |
|----------|-------------|
| `SFTP_HOST`, `SFTP_PORT` | SFTP connection info |
| `SFTP_USER`, `SFTP_PASSWORD` | SFTP credentials |
| `OUTPUT_TABLE` | Target SQL Server table name |
| `INSERTER_MAX_RETRIES` | Max DB insert retries |
| `MSSQL_*` | SQL Server configuration |
| `LOG_LEVEL` | Logging verbosity |

## Docker Support

Build and run this ETL as a container:

```bash
docker build -t fab-etl .
docker run --env-file .env fab-etl
```

## Requirements

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

Key libraries:
- `mt-940`: MT940 parsing
- `pandas`: Data wrangling
- `paramiko`: SFTP communication
- `SQLAlchemy`, `pyodbc`: Database access
- `fast-to-sql`: Bulk data loading

## Running the Pipeline

Make sure the `.env` is correctly configured, then run:

```bash
python main.py
```

Logs will indicate:
- Files downloaded
- Records parsed and inserted
- Cleanup and deletion confirmation

## License

This project is licensed under MIT. Use of MT940 files and connection to remote servers must comply with data agreements and IT security standards.
