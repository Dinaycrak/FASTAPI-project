import psycopg2
#psql 'postgresql://neondb_owner:npg_4AEpq0CdGsNM@ep-royal-smoke-afutcih1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
def get_db_connection():
    return psycopg2.connect(
        host="ep-royal-smoke-afutcih1-pooler.c-2.us-west-2.aws.neon.tech",
        port="5432",
        user="neondb_owner",
        password="npg_4AEpq0CdGsNM",
        dbname="neondb"
    )