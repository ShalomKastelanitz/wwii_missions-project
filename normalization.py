import psycopg2

# התחברות לבסיס הנתונים PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    database="wwii_missions4",
    user="postgres",
    password="1234",
    port="5432"
)

cursor = connection.cursor()

# יצירת טבלאות נפרדות לעמודות הנבחרות ונירמול הקשרים
def create_tables():
    cursor.execute("""
        -- יצירת טבלה חדשה לעמודת "Country"
        CREATE TABLE IF NOT EXISTS country (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE 
        );

        -- יצירת טבלה חדשה לעמודת "air_force"
        CREATE TABLE IF NOT EXISTS air_force (
            id SERIAL PRIMARY KEY,
            country_id INTEGER REFERENCES country(id),
            name VARCHAR(255) UNIQUE 
        );

        -- יצירת קשרים בטבלה המקורית (מפתחות זרים)
        ALTER TABLE mission
        ADD COLUMN country_id INTEGER REFERENCES country(id),
        ADD COLUMN air_force_id INTEGER REFERENCES air_force(id);
    """)
    connection.commit()

# הכנסת נתונים מנורמלים לטבלאות הנפרדות והוספת מפתחות זרים
def normalize_data():
    cursor.execute("SELECT DISTINCT Country FROM mission")
    countries = cursor.fetchall()

    cursor.execute("SELECT DISTINCT air_force"
                   ""
                   ", Country FROM mission")
    air_forces = cursor.fetchall()

    # הכנסת הערכים לטבלאות הנפרדות
    for country in countries:
        insert_into_table('country', country[0])

    for air_force, country in air_forces:
        country_id = get_country_id(country)
        cursor.execute("""
            INSERT INTO air_force (name, country_id) 
            VALUES (%s, %s) ON CONFLICT (name) DO NOTHING
        """, (air_force, country_id))

    # עדכון הטבלה המקורית עם המפתחות הזרים
    cursor.execute("SELECT mission_id, Country,air_force FROM mission")
    rows = cursor.fetchall()

    for row in rows:
        mission_id, country, air_force = row

        country_id = get_country_id(country)

        cursor.execute("SELECT id FROM air_force WHERE name = %s", (air_force,))
        air_force_id = cursor.fetchone()[0]

        cursor.execute("""
            UPDATE mission
            SET country_id = %s, air_force_id = %s
            WHERE mission_id = %s
        """, (country_id, air_force_id, mission_id))

    connection.commit()

# פונקציה להוספת ערכים חדשים לטבלת המדינות
def insert_into_table(table_name, value):
    cursor.execute(f"INSERT INTO {table_name} (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id", (value,))
    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(f"SELECT id FROM {table_name} WHERE name = %s", (value,))
    result = cursor.fetchone()
    return result[0]

# פונקציה לקבלת ה-id של מדינה
def get_country_id(country_name):
    cursor.execute("SELECT id FROM country WHERE name = %s", (country_name,))
    return cursor.fetchone()[0]

# מחיקת העמודות הישנות
def drop_old_columns():
    cursor.execute("""
        ALTER TABLE mission
        DROP COLUMN Country,
        DROP COLUMN \"air_force\";
    """)
    connection.commit()

# ביצוע התהליך
create_tables()
normalize_data()
drop_old_columns()

# סגירת החיבור
cursor.close()
connection.close()
