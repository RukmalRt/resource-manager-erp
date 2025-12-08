import psycopg2

conn = psycopg2.connect(
    host="db.rftiupczjyzaexorlenc.supabase.co",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="0602836390Ruk#",
    sslmode="require"
)
print("Connected!")
