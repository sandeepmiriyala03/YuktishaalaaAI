from sqlalchemy import create_engine

connection_string = (
    "mssql+pyodbc://@localhost/YuktishaalaaAI?"
    "driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(
    connection_string,
    echo=True
)

