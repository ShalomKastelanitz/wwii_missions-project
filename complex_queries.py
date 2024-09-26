import psycopg2

# חיבור לדאטה בייס
connection = psycopg2.connect(
    host="localhost",
    database="wwii_missions4",
    user="postgres",
    password="1234",
    port="5432"
)

# מחזיר את חיל האוויר שביצע הכי הרבה פעולות לפי שנה
def get_mission_data(year, connection):
    try:
        # יצירת אובייקט cursor
        cursor = connection.cursor()


        query = """
        SELECT 
            air_force,
            target_city,
            COUNT(*) AS mission_count
        FROM mission
        WHERE EXTRACT(YEAR FROM mission_date) = %s
        GROUP BY air_force, target_city
        ORDER BY mission_count DESC
        LIMIT 1;
        """

        # הרצת השאילתא
        cursor.execute(query, (year,))

        # קבלת התוצאה
        result = cursor.fetchone()

        if result:
            mission_data = {
                "air_force": result[0],
                "target_city": result[1],
                "mission_count": result[2]
            }
        else:
            mission_data = None

        # הרצת EXPLAIN ANALYZE
        explain_query = f"""
        EXPLAIN ANALYZE
        {query}
        """
        cursor.execute(explain_query, (year,))
        explain_result = cursor.fetchall()

        return mission_data, explain_result

    except Exception as e:
        print("Error:", e)
        return None, None

    finally:
        # סגירת ה-cursor
        cursor.close()

# קלט מהמשתמש והדפסת התוצאה
year_input = int(input("אנא הקש את השנה: "))
mission_data, explain_data = get_mission_data(year_input, connection)

if mission_data:
    print("Air Force:", mission_data["air_force"])
    print("Target City:", mission_data["target_city"])
    print("Mission Count:", mission_data["mission_count"])
else:
    print("לא נמצאו נתונים לשנה", year_input)

# הדפסת תוכנית הביצוע של השאילתא
print("\nEXPLAIN ANALYZE:")
for row in explain_data:
    print(row)

# סגירת החיבור
connection.close()

def get_average_damage_assessment(connection):
    try:
        cursor = connection.cursor()

        query = """
        SELECT 
            country,
          count (bomb_damage_assessment) AS average_damage_assessment
        FROM mission
        WHERE attacking_aircraft > 5
        GROUP BY country
        ORDER BY average_damage_assessment DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        # בניית רשימה של תוצאות
        damage_assessments = []
        for row in results:
            damage_assessments.append({
                "country": row[0],
                "average_damage_assessment": row[1]
            })

        return damage_assessments

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        cursor.close()
