from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import database
from database import *

# Khởi tạo cửa sổ
win = Tk()
win.title("Quản Lý Sinh Viên")
win.geometry("800x600")  # Bạn có thể điều chỉnh kích thước cửa sổ

# Tạo Notebook để chứa các tab
notebook = ttk.Notebook(win)
notebook.pack(pady=10, expand=True, fill='both')

# Tạo tab chính
main_tab = Frame(notebook)
notebook.add(main_tab, text="Quản Lý Sinh Viên")

# Tạo tab mới
new_tab = Frame(notebook)
notebook.add(new_tab, text="Quản Lý Điểm")

# Hàm tải danh sách sinh viên từ cơ sở dữ liệu
def load_students():
    students = database.get_all_students()
    listbox.delete(0, END)
    for student in students:
        student_info = f"{student['name']} - {student['student_id']} - {student['birth_year']}"
        listbox.insert(END, student_info)

# Hàm cập nhật danh sách sinh viên trong tab quản lý điểm
def update_student_list():
    students = database.get_all_students()
    student_listbox.delete(0, END)
    for student in students:
        score_info = {
            'Math': student['math_score'],
            'Literature': student['literature_score'],
            'English': student['english_score']
        }
        total_score = sum(score_info.values())
        student_listbox.insert(END, f"{student['name']} - Tổng điểm: {total_score} - Toán: {score_info['Math']}, Văn: {score_info['Literature']}, Anh: {score_info['English']}")

# Hàm thêm sinh viên
def add_student():
    student_name = name_entry.get()
    student_id = id_entry.get()
    birth_year = birth_year_entry.get()

    if student_name and student_id and birth_year:
        try:
            birth_year_int = int(birth_year)
        except ValueError:
            messagebox.showwarning("Thông báo", "Năm sinh phải là số nguyên.")
            return

        success = database.add_student(student_name, student_id, birth_year_int)
        if success:
            messagebox.showinfo("Thông báo", "Thêm sinh viên thành công.")
            load_students()
            update_student_list()
            name_entry.delete(0, END)
            id_entry.delete(0, END)
            birth_year_entry.delete(0, END)
        else:
            messagebox.showerror("Lỗi", "Thêm sinh viên thất bại. Có thể MSSV đã tồn tại.")
    else:
        messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")

# Hàm sửa sinh viên
def edit_student():
    selected_index = listbox.curselection()
    if selected_index:
        students = database.get_all_students()
        student = students[selected_index[0]]
        student_db_id = student['id']

        student_name = name_entry.get()
        student_id = id_entry.get()
        birth_year = birth_year_entry.get()

        if student_name and student_id and birth_year:
            try:
                birth_year_int = int(birth_year)
            except ValueError:
                messagebox.showwarning("Thông báo", "Năm sinh phải là số nguyên.")
                return

            success = database.update_student(student_db_id, student_name, student_id, birth_year_int)
            if success:
                messagebox.showinfo("Thông báo", "Sửa sinh viên thành công.")
                load_students()
                update_student_list()
                name_entry.delete(0, END)
                id_entry.delete(0, END)
                birth_year_entry.delete(0, END)
            else:
                messagebox.showerror("Lỗi", "Sửa sinh viên thất bại. Có thể MSSV đã tồn tại.")
        else:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để sửa")

# Hàm xóa sinh viên
def delete_student():
    selected_index = listbox.curselection()
    if selected_index:
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?")
        if confirm:
            students = database.get_all_students()
            student = students[selected_index[0]]
            student_db_id = student['id']
            success = database.delete_student(student_db_id)
            if success:
                messagebox.showinfo("Thông báo", "Xóa sinh viên thành công.")
                load_students()
                update_student_list()
            else:
                messagebox.showerror("Lỗi", "Xóa sinh viên thất bại.")
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để xóa")

# Hàm nhập điểm cho sinh viên
def enter_scores():
    selected_index = student_listbox.curselection()
    if selected_index:
        students = database.get_all_students()
        student = students[selected_index[0]]
        student_db_id = student['id']
        student_name = student['name']

        math_score = math_entry.get()
        literature_score = literature_entry.get()
        english_score = english_entry.get()

        # Kiểm tra xem điểm có hợp lệ không
        try:
            math_score = float(math_score)
            literature_score = float(literature_score)
            english_score = float(english_score)
        except ValueError:
            messagebox.showwarning("Thông báo", "Vui lòng nhập điểm hợp lệ.")
            return

        # Cập nhật điểm vào cơ sở dữ liệu
        success = database.update_scores(student_db_id, math_score, literature_score, english_score)
        if success:
            messagebox.showinfo("Thông báo", f"Điểm đã được nhập cho {student_name}!\nĐiểm: Toán: {math_score}, Văn: {literature_score}, Anh: {english_score}")
            update_student_list()
            math_entry.delete(0, END)
            literature_entry.delete(0, END)
            english_entry.delete(0, END)
        else:
            messagebox.showerror("Lỗi", "Cập nhật điểm thất bại.")
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để nhập điểm")

# Hàm sắp xếp sinh viên theo điểm cao nhất
def sort_by_scores():
    students = database.get_all_students()
    sorted_students = sorted(
        students, 
        key=lambda x: (x['math_score'] + x['literature_score'] + x['english_score']), 
        reverse=True
    )
    student_listbox.delete(0, END)
    for student in sorted_students:
        total_score = student['math_score'] + student['literature_score'] + student['english_score']
        student_listbox.insert(END, f"{student['name']} - Tổng điểm: {total_score} - Toán: {student['math_score']}, Văn: {student['literature_score']}, Anh: {student['english_score']}")

# Hàm lọc điểm cao nhất theo môn học
def highest_score_by_subject():
    students = database.get_all_students()
    highest_scores = {}
    for student in students:
        if student['math_score'] > highest_scores.get('Math', (None, -1))[1]:
            highest_scores['Math'] = (student['name'], student['math_score'])
        if student['literature_score'] > highest_scores.get('Literature', (None, -1))[1]:
            highest_scores['Literature'] = (student['name'], student['literature_score'])
        if student['english_score'] > highest_scores.get('English', (None, -1))[1]:
            highest_scores['English'] = (student['name'], student['english_score'])
    
    if highest_scores:
        message = "\n".join([
            f"Toán: {info[0]} với điểm {info[1]}" for subject, info in highest_scores.items()
        ])
        messagebox.showinfo("Điểm Cao Nhất Theo Môn", message)
    else:
        messagebox.showinfo("Thông báo", "Chưa có dữ liệu điểm.")

# Hàm xuất dữ liệu ra file txt
def export_data():
    students = database.get_all_students()
    scores = {student['name']: {
        'Math': student['math_score'],
        'Literature': student['literature_score'],
        'English': student['english_score']
    } for student in students}
    filename = "students_data.txt"  # Tên file xuất ra
    success = database.export_data_to_txt(students, scores, filename)
    if success:
        messagebox.showinfo("Thông báo", f"Xuất dữ liệu thành công vào file {filename}.")
    else:
        messagebox.showerror("Lỗi", "Xuất dữ liệu thất bại.")

# Tạo Label tiêu đề cho tab quản lý sinh viên
title_label = Label(main_tab, text="ỨNG DỤNG QUẢN LÝ SINH VIÊN", fg="red", font=("Helvetica", 16), width=30)
title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Tạo Listbox để hiển thị danh sách sinh viên
listbox = Listbox(main_tab, width=50, height=10)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
load_students()

# Tạo Entry để nhập tên sinh viên
name_label = Label(main_tab, text="Nhập tên Sinh Viên:")
name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

name_entry = Entry(main_tab, width=40)
name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Tạo Entry để nhập mã số sinh viên
id_label = Label(main_tab, text="Nhập mã số Sinh Viên:")
id_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

id_entry = Entry(main_tab, width=40)
id_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Tạo Entry để nhập năm sinh sinh viên
birth_year_label = Label(main_tab, text="Nhập năm sinh Sinh Viên:")
birth_year_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

birth_year_entry = Entry(main_tab, width=40)
birth_year_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Tạo các Button nằm ngang nhau trên cùng một dòng và có kích thước đồng đều
button_frame = Frame(main_tab)
button_frame.grid(row=5, column=0, columnspan=3, pady=10)

add_button = Button(button_frame, text="Thêm", command=add_student, width=10)
add_button.grid(row=0, column=0, padx=5)

edit_button = Button(button_frame, text="Sửa", command=edit_student, width=10)
edit_button.grid(row=0, column=1, padx=5)

delete_button = Button(button_frame, text="Xóa", command=delete_student, width=10)
delete_button.grid(row=0, column=2, padx=5)

# Cấu hình lưới để giãn nở Listbox
main_tab.grid_rowconfigure(1, weight=1)
main_tab.grid_columnconfigure(1, weight=1)

# Tab quản lý điểm
scores_title_label = Label(new_tab, text="QUẢN LÝ ĐIỂM SINH VIÊN", fg="blue", font=("Helvetica", 16), width=30)
scores_title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

student_listbox = Listbox(new_tab, width=60, height=10)
student_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
update_student_list()

# Tạo Label và Entry cho các môn học
math_label = Label(new_tab, text="Nhập điểm Toán:")
math_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

math_entry = Entry(new_tab, width=20)
math_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

literature_label = Label(new_tab, text="Nhập điểm Văn:")
literature_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

literature_entry = Entry(new_tab, width=20)
literature_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

english_label = Label(new_tab, text="Nhập điểm Anh:")
english_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

english_entry = Entry(new_tab, width=20)
english_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Tạo các Button nằm ngang nhau trên cùng một dòng và có kích thước đồng đều cho tab điểm
scores_button_frame = Frame(new_tab)
scores_button_frame.grid(row=5, column=0, columnspan=4, pady=10)

enter_scores_button = Button(scores_button_frame, text="Nhập Điểm", command=enter_scores, width=12)
enter_scores_button.grid(row=0, column=0, padx=5)

sort_scores_button = Button(scores_button_frame, text="Sắp Xếp Điểm", command=sort_by_scores, width=12)
sort_scores_button.grid(row=0, column=1, padx=5)

highest_score_button = Button(scores_button_frame, text="Điểm Cao Nhất", command=highest_score_by_subject, width=12)
highest_score_button.grid(row=0, column=2, padx=5)

export_button = Button(scores_button_frame, text="Xuất Dữ Liệu", command=export_data, width=15)
export_button.grid(row=0, column=3, padx=5)

# Cấu hình lưới để giãn nở Listbox
new_tab.grid_rowconfigure(1, weight=1)
new_tab.grid_columnconfigure(1, weight=1)

# Chạy ứng dụng
win.mainloop()
