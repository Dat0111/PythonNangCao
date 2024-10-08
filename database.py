# database.py
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# Thông tin kết nối cơ sở dữ liệu
DB_NAME = "student_management"
DB_USER = "postgres"  # Thay đổi nếu bạn sử dụng user khác
DB_PASSWORD = "huyng1234"  # Thay đổi mật khẩu theo cài đặt của bạn
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def add_student(name, student_id, birth_year):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, student_id, birth_year) VALUES (%s, %s, %s) RETURNING id;",
            (name, student_id, birth_year)
        )
        student_db_id = cursor.fetchone()[0]
        # Tạo bản ghi điểm mặc định
        cursor.execute(
            "INSERT INTO scores (student_id) VALUES (%s);",
            (student_db_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding student: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            SELECT s.id, s.name, s.student_id, s.birth_year, 
                   sc.math_score, sc.literature_score, sc.english_score
            FROM students s
            LEFT JOIN scores sc ON s.id = sc.student_id
            ORDER BY s.id;
        """)
        students = cursor.fetchall()
        return students
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_student(student_db_id, name, student_id, birth_year):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE students SET name = %s, student_id = %s, birth_year = %s WHERE id = %s;",
            (name, student_id, birth_year, student_db_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating student: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete_student(student_db_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id = %s;", (student_db_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting student: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_scores(student_db_id, math, literature, english):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE scores 
            SET math_score = %s, literature_score = %s, english_score = %s 
            WHERE student_id = %s;
            """,
            (math, literature, english, student_db_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating scores: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def export_data_to_txt(students, scores, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for student in students:
                f.write(f"Name: {student['name']}, MSSV: {student['student_id']}, Năm sinh: {student['birth_year']}\n")
                student_scores = scores.get(student['name'], {})
                f.write(f"Điểm: Toán: {student_scores.get('Math', 0)}, Văn: {student_scores.get('Literature', 0)}, Anh: {student_scores.get('English', 0)}\n\n")
        return True
    except Exception as e:
        print(f"Error exporting data: {e}")
        return False
