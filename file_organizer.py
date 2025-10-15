import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import filedialog, simpledialog, messagebox
import os
import shutil
import subprocess
import sys
import datetime


class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("📁 Уютный Файловый Органайзер")
        self.geometry("800x700")
        self.storage_dir = "storage"
        os.makedirs(self.storage_dir, exist_ok=True)

        ctk.set_appearance_mode("Light")
        self.configure(fg_color="#F0F8FF")

        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground="#333333",
                        rowheight=50,
                        fieldbackground="#FFFFFF",
                        bordercolor="#CCCCCC",
                        borderwidth=1,
                        font=('Calibri', 24))

        style.configure("Treeview.Heading", font=('Calibri', 14, 'bold'))  # Стиль для заголовков тоже увеличим
        style.map('Treeview', background=[('selected', '#E6E6FA')])

        self.tree = ttk.Treeview(tree_frame, columns=('path', 'date'), displaycolumns=('date'))
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.heading("#0", text="Имя файла/папки", anchor='w')
        self.tree.column("#0", stretch=True, width=400)

        self.tree.heading('date', text='Дата изменения')
        self.tree.column('date', anchor='center', width=160)

        self.tree.column('path', width=0, stretch=False)

        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.on_double_click)

        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        button_color = "#E6E6FA"
        button_hover_color = "#DDA0DD"
        text_color = "#242424"

        self.btn_add_semester = ctk.CTkButton(control_frame, text="Добавить семестр", command=self.add_semester,
                                              fg_color=button_color, hover_color=button_hover_color,
                                              text_color=text_color)
        self.btn_add_semester.pack(pady=10, padx=10, fill="x")

        self.btn_add_subject = ctk.CTkButton(control_frame, text="Добавить предмет", command=self.add_subject,
                                             fg_color=button_color, hover_color=button_hover_color,
                                             text_color=text_color)
        self.btn_add_subject.pack(pady=10, padx=10, fill="x")

        self.btn_add_file = ctk.CTkButton(control_frame, text="Добавить файл", command=self.add_file,
                                          fg_color=button_color, hover_color=button_hover_color, text_color=text_color)
        self.btn_add_file.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(control_frame, text="").pack(pady=10)

        self.btn_open_file = ctk.CTkButton(control_frame, text="Открыть файл", command=self.open_selected_item,
                                           fg_color=button_color, hover_color=button_hover_color, text_color=text_color)
        self.btn_open_file.pack(pady=10, padx=10, fill="x")

        self.btn_delete = ctk.CTkButton(control_frame, text="Удалить выбранное", command=self.delete_item,
                                        fg_color="#FFB6C1", hover_color="#FF69B4", text_color=text_color)
        self.btn_delete.pack(pady=(30, 10), padx=10, fill="x")

    def populate_tree(self, parent="", path=""):
        if not parent:
            for i in self.tree.get_children():
                self.tree.delete(i)
            path = self.storage_dir

        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)

            try:
                mtime = os.path.getmtime(full_path)
                date_str = datetime.datetime.fromtimestamp(mtime).strftime('%d.%m.%Y %H:%M')
            except:
                date_str = ""

            if os.path.isdir(full_path):
                node = self.tree.insert(parent, "end", text=item, values=(full_path, ""))
                self.populate_tree(parent=node, path=full_path)
            else:
                node = self.tree.insert(parent, "end", text=item, values=(full_path, date_str))

    def add_semester(self):
        name = simpledialog.askstring("Новый семестр", "Введите название семестра (например, 'Семестр 1'):")
        if name:
            try:
                os.makedirs(os.path.join(self.storage_dir, name), exist_ok=True)
                self.populate_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать папку: {e}")

    def add_subject(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Сначала выберите семестр в дереве!")
            return
        item_path = self.tree.item(selected_item[0])['values'][0]
        if not os.path.isdir(item_path):
            messagebox.showwarning("Внимание", "Предмет можно добавить только в семестр (папку)!")
            return
        name = simpledialog.askstring("Новый предмет", "Введите название предмета (например, 'Математический анализ'):")
        if name:
            try:
                os.makedirs(os.path.join(item_path, name), exist_ok=True)
                self.populate_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать папку: {e}")

    def add_file(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Сначала выберите предмет в дереве!")
            return
        item_path = self.tree.item(selected_item[0])['values'][0]
        if not os.path.isdir(item_path):
            messagebox.showwarning("Внимание", "Файл можно добавить только в папку предмета!")
            return
        filepath = filedialog.askopenfilename(
            title="Выберите файл для добавления",
            filetypes=[
                ("Все поддерживаемые", "*.pdf *.docx *.doc *.xlsx *.xls *.pptx *.ppt *.txt *.exe"),
                ("PDF документы", "*.pdf"),
                ("Word документы", "*.docx *.doc"),
                ("Excel таблицы", "*.xlsx *.xls"),
                ("PowerPoint презентации", "*.pptx *.ppt"),
                ("Текстовые файлы", "*.txt"),
                ("Исполняемые файлы", "*.exe"),
                ("Все файлы", "*.*")
            ]
        )
        if filepath:
            try:
                shutil.copy(filepath, item_path)
                self.populate_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось скопировать файл: {e}")

    def on_double_click(self, event):
        self.open_selected_item()

    def open_selected_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Сначала выберите файл для открытия!")
            return
        item_path = self.tree.item(selected_item[0])['values'][0]
        if os.path.isfile(item_path):
            try:
                if sys.platform == "win32":
                    os.startfile(item_path)
                elif sys.platform == "darwin":
                    subprocess.call(["open", item_path])
                else:
                    subprocess.call(["xdg-open", item_path])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Сначала выберите элемент для удаления!")
            return
        item_path = self.tree.item(selected_item[0])['values'][0]
        item_name = self.tree.item(selected_item[0])['text']
        is_dir = os.path.isdir(item_path)
        item_type = "папку со всем содержимым" if is_dir else "файл"
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить {item_type} '{item_name}'?"):
            try:
                if is_dir:
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                self.populate_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить элемент: {e}")
if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()