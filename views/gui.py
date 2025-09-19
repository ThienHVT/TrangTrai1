import tkinter as tk
from tkinter import ttk, messagebox
from modules.auth import AuthManager
from modules.crop_manager import CropManager
from modules.animal_manager import AnimalManager
from modules.activity_manager import ActivityManager
import json
import os
import pandas as pd
from tkinter.filedialog import asksaveasfilename
from modules.report_generator import ReportGenerator

class FarmManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Trang Trại")
        self.root.geometry("1000x600")
        
        # Khởi tạo các module
        self.auth_manager = AuthManager()
        self.crop_manager = CropManager()
        self.animal_manager = AnimalManager()
        self.activity_manager = ActivityManager()
        
        # Tạo thư mục data nếu chưa tồn tại
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Tải dữ liệu
        self.load_data()
        
        # Giao diện đăng nhập
        self.show_login_screen()
    
    def load_data(self):
        """Tải tất cả dữ liệu từ file JSON"""
        try:
            self.crop_manager.load_data()
            self.animal_manager.load_data()
            self.activity_manager.load_data()
            self.auth_manager.load_users()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
    
    def save_data(self):
        """Lưu tất cả dữ liệu vào file JSON"""
        try:
            self.crop_manager.save_data()
            self.animal_manager.save_data()
            self.activity_manager.save_data()
            self.auth_manager.save_users()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")
    
    def show_login_screen(self):
        """Hiển thị màn hình đăng nhập"""
        self.clear_window()
        
        login_frame = ttk.Frame(self.root, padding="30 15 30 15")
        login_frame.pack(expand=True)
        
        ttk.Label(login_frame, text="ĐĂNG NHẬP HỆ THỐNG", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(login_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(login_frame, text="Mật khẩu:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Button(login_frame, text="Đăng nhập", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Thêm nút đăng ký cho người dùng mới
        ttk.Button(login_frame, text="Đăng ký tài khoản mới", command=self.show_register_screen).grid(row=4, column=0, columnspan=2, pady=5)
    
    def show_register_screen(self):
        """Hiển thị màn hình đăng ký"""
        self.clear_window()
        
        register_frame = ttk.Frame(self.root, padding="30 15 30 15")
        register_frame.pack(expand=True)
        
        ttk.Label(register_frame, text="ĐĂNG KÝ TÀI KHOẢN MỚI", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(register_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_username = ttk.Entry(register_frame)
        self.reg_username.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(register_frame, text="Mật khẩu:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_password = ttk.Entry(register_frame, show="*")
        self.reg_password.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(register_frame, text="Xác nhận mật khẩu:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_confirm = ttk.Entry(register_frame, show="*")
        self.reg_confirm.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(register_frame, text="Loại tài khoản:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.user_type = tk.StringVar(value="user")
        ttk.Radiobutton(register_frame, text="Người dùng thường", variable=self.user_type, value="user").grid(row=4, column=1, sticky=tk.W)
        ttk.Radiobutton(register_frame, text="Quản trị viên", variable=self.user_type, value="admin").grid(row=5, column=1, sticky=tk.W)
        
        ttk.Button(register_frame, text="Đăng ký", command=self.handle_register).grid(row=6, column=0, columnspan=2, pady=15)
        ttk.Button(register_frame, text="Quay lại đăng nhập", command=self.show_login_screen).grid(row=7, column=0, columnspan=2, pady=5)
    
    def handle_register(self):
        """Xử lý đăng ký tài khoản mới"""
        username = self.reg_username.get()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        user_type = self.user_type.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Tên đăng nhập và mật khẩu không được để trống")
            return
        
        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return
        
        result = self.auth_manager.register_user(username, password, user_type)
        if result["success"]:
            messagebox.showinfo("Thành công", result["message"])
            self.show_login_screen()
        else:
            messagebox.showerror("Lỗi", result["message"])
    
    def handle_login(self):
        """Xử lý đăng nhập"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu")
            return
        
        result = self.auth_manager.login(username, password)
        if result["success"]:
            self.current_user = result["user"]
            self.show_main_menu()
        else:
            messagebox.showerror("Lỗi", result["message"])
    
    def show_main_menu(self):
        """Hiển thị menu chính sau khi đăng nhập thành công"""
        self.clear_window()
        
        # Tạo thanh menu
        menubar = tk.Menu(self.root)
        
        # Menu hệ thống
        system_menu = tk.Menu(menubar, tearoff=0)
        system_menu.add_command(label="Đổi mật khẩu", command=self.show_change_password)
        system_menu.add_separator()
        system_menu.add_command(label="Đăng xuất", command=self.logout)
        system_menu.add_command(label="Thoát", command=self.exit_app)
        menubar.add_cascade(label="Hệ thống", menu=system_menu)
        
        # Menu quản lý
        management_menu = tk.Menu(menubar, tearoff=0)
        management_menu.add_command(label="Quản lý cây trồng", command=self.show_crop_management)
        management_menu.add_command(label="Quản lý vật nuôi", command=self.show_animal_management)
        management_menu.add_command(label="Quản lý hoạt động", command=self.show_activity_management)
        menubar.add_cascade(label="Quản lý", menu=management_menu)
        
        # Menu báo cáo (chỉ admin)
        if self.current_user["type"] == "admin":
            report_menu = tk.Menu(menubar, tearoff=0)
            report_menu.add_command(label="Xuất báo cáo Excel", command=self.export_excel)
            menubar.add_cascade(label="Báo cáo", menu=report_menu)
        
        self.root.config(menu=menubar)
        
        # Hiển thị trang chủ
        home_frame = ttk.Frame(self.root, padding="20")
        home_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(home_frame, text=f"CHÀO MỪNG ĐẾN VỚI HỆ THỐNG QUẢN LÝ TRANG TRẠI", 
                 font=('Arial', 16)).pack(pady=20)
        
        ttk.Label(home_frame, text=f"Xin chào, {self.current_user['username']} ({'Quản trị viên' if self.current_user['type'] == 'admin' else 'Người dùng'})", 
                 font=('Arial', 12)).pack(pady=10)
        
        # Hiển thị thống kê nhanh
        stats_frame = ttk.LabelFrame(home_frame, text="Thống kê nhanh", padding="10")
        stats_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(stats_frame, text=f"Số loại cây trồng: {len(self.crop_manager.crops)}").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Label(stats_frame, text=f"Số loại vật nuôi: {len(self.animal_manager.animals)}").grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        ttk.Label(stats_frame, text=f"Số hoạt động gần đây: {len(self.activity_manager.activities)}").grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
    
    def show_change_password(self):
        """Hiển thị form đổi mật khẩu"""
        change_pass_window = tk.Toplevel(self.root)
        change_pass_window.title("Đổi mật khẩu")
        change_pass_window.geometry("400x250")
        
        ttk.Label(change_pass_window, text="ĐỔI MẬT KHẨU", font=('Arial', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(change_pass_window, padding="10")
        form_frame.pack(expand=True)
        
        ttk.Label(form_frame, text="Mật khẩu hiện tại:").grid(row=0, column=0, sticky=tk.W, pady=5)
        current_pass = ttk.Entry(form_frame, show="*")
        current_pass.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Mật khẩu mới:").grid(row=1, column=0, sticky=tk.W, pady=5)
        new_pass = ttk.Entry(form_frame, show="*")
        new_pass.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Xác nhận mật khẩu mới:").grid(row=2, column=0, sticky=tk.W, pady=5)
        confirm_pass = ttk.Entry(form_frame, show="*")
        confirm_pass.grid(row=2, column=1, pady=5, padx=5)
        
        def handle_change():
            current = current_pass.get()
            new = new_pass.get()
            confirm = confirm_pass.get()
            
            if not current or not new or not confirm:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
                return
            
            if new != confirm:
                messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận không khớp")
                return
            
            result = self.auth_manager.change_password(
                self.current_user["username"],
                current,
                new
            )
            
            if result["success"]:
                messagebox.showinfo("Thành công", result["message"])
                change_pass_window.destroy()
            else:
                messagebox.showerror("Lỗi", result["message"])
        
        ttk.Button(form_frame, text="Đổi mật khẩu", command=handle_change).grid(row=3, column=0, columnspan=2, pady=15)
    
    def show_crop_management(self):
        """Hiển thị màn hình quản lý cây trồng"""
        self.clear_window()
        
        # Tạo frame chứa các control
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Nút thêm mới
        ttk.Button(control_frame, text="Thêm cây trồng", command=self.show_add_crop_form).pack(side=tk.LEFT, padx=5)
        
        # Ô tìm kiếm
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.crop_search_entry = ttk.Entry(search_frame, width=30)
        self.crop_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm", command=self.search_crops).pack(side=tk.LEFT)
        
        # Tạo Treeview để hiển thị dữ liệu
        self.crop_tree = ttk.Treeview(self.root, columns=("ID", "Tên", "Loại", "Ngày trồng", "Diện tích", "Trạng thái"), show="headings")
        
        # Đặt tên cho các cột
        self.crop_tree.heading("ID", text="ID")
        self.crop_tree.heading("Tên", text="Tên")
        self.crop_tree.heading("Loại", text="Loại")
        self.crop_tree.heading("Ngày trồng", text="Ngày trồng")
        self.crop_tree.heading("Diện tích", text="Diện tích (ha)")
        self.crop_tree.heading("Trạng thái", text="Trạng thái")
        
        # Đặt độ rộng các cột
        self.crop_tree.column("ID", width=50, anchor=tk.CENTER)
        self.crop_tree.column("Tên", width=150)
        self.crop_tree.column("Loại", width=100)
        self.crop_tree.column("Ngày trồng", width=100, anchor=tk.CENTER)
        self.crop_tree.column("Diện tích", width=100, anchor=tk.CENTER)
        self.crop_tree.column("Trạng thái", width=100)
        
        self.crop_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.crop_tree, orient=tk.VERTICAL, command=self.crop_tree.yview)
        self.crop_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nút sửa và xóa
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Sửa", command=self.edit_crop).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Xóa", command=self.delete_crop).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Quay lại", command=self.show_main_menu).pack(side=tk.RIGHT)
        
        # Hiển thị dữ liệu
        self.display_crops()
    
    def display_crops(self, crops=None):
        """Hiển thị danh sách cây trồng trên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.crop_tree.get_children():
            self.crop_tree.delete(item)
        
        # Hiển thị dữ liệu mới
        crops_to_display = crops if crops else self.crop_manager.crops
        for crop in crops_to_display:
            self.crop_tree.insert("", tk.END, values=(
                crop["id"],
                crop["name"],
                crop["type"],
                crop["planting_date"],
                crop["area"],
                crop["status"]
            ))
    
    def search_crops(self):
        """Tìm kiếm cây trồng"""
        keyword = self.crop_search_entry.get().lower()
        if not keyword:
            self.display_crops()
            return
        
        filtered_crops = [
            crop for crop in self.crop_manager.crops
            if (keyword in crop["name"].lower() or 
                keyword in crop["type"].lower() or 
                keyword in crop["status"].lower())
        ]
        self.display_crops(filtered_crops)
    
    def show_add_crop_form(self):
        """Hiển thị form thêm cây trồng mới"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm cây trồng mới")
        add_window.geometry("500x400")
        
        ttk.Label(add_window, text="THÊM CÂY TRỒNG MỚI", font=('Arial', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Các trường thông tin
        ttk.Label(form_frame, text="Tên cây:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Loại cây:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_entry = ttk.Entry(form_frame)
        type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ngày trồng:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Diện tích (ha):").grid(row=3, column=0, sticky=tk.W, pady=5)
        area_entry = ttk.Entry(form_frame)
        area_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        status_entry = ttk.Entry(form_frame)
        status_entry.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        notes_entry = tk.Text(form_frame, height=5, width=30)
        notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def save_crop():
            new_crop = {
                "id": len(self.crop_manager.crops) + 1,
                "name": name_entry.get(),
                "type": type_entry.get(),
                "planting_date": date_entry.get(),
                "area": area_entry.get(),
                "status": status_entry.get(),
                "notes": notes_entry.get("1.0", tk.END).strip()
            }
            
            if not new_crop["name"] or not new_crop["type"]:
                messagebox.showerror("Lỗi", "Tên và loại cây không được để trống")
                return
            
            self.crop_manager.add_crop(new_crop)
            self.crop_manager.save_data()
            self.display_crops()
            add_window.destroy()
            messagebox.showinfo("Thành công", "Đã thêm cây trồng mới")
        
        ttk.Button(form_frame, text="Lưu", command=save_crop).grid(row=6, column=0, columnspan=2, pady=15)
    
    def edit_crop(self):
        """Sửa thông tin cây trồng"""
        selected_item = self.crop_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cây trồng cần sửa")
            return
        
        item_data = self.crop_tree.item(selected_item[0], "values")
        crop_id = int(item_data[0])
        
        # Tìm cây trồng cần sửa
        crop_to_edit = None
        for crop in self.crop_manager.crops:
            if crop["id"] == crop_id:
                crop_to_edit = crop
                break
        
        if not crop_to_edit:
            messagebox.showerror("Lỗi", "Không tìm thấy cây trồng cần sửa")
            return
        
        # Hiển thị form sửa
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa thông tin cây trồng")
        edit_window.geometry("500x400")
        
        ttk.Label(edit_window, text="SỬA THÔNG TIN CÂY TRỒNG", font=('Arial', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Các trường thông tin
        ttk.Label(form_frame, text="Tên cây:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, crop_to_edit["name"])
        name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Loại cây:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_entry = ttk.Entry(form_frame)
        type_entry.insert(0, crop_to_edit["type"])
        type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ngày trồng:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.insert(0, crop_to_edit["planting_date"])
        date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Diện tích (ha):").grid(row=3, column=0, sticky=tk.W, pady=5)
        area_entry = ttk.Entry(form_frame)
        area_entry.insert(0, crop_to_edit["area"])
        area_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        status_entry = ttk.Entry(form_frame)
        status_entry.insert(0, crop_to_edit["status"])
        status_entry.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        notes_entry = tk.Text(form_frame, height=5, width=30)
        notes_entry.insert("1.0", crop_to_edit.get("notes", ""))
        notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_crop():
            updated_crop = {
                "id": crop_id,
                "name": name_entry.get(),
                "type": type_entry.get(),
                "planting_date": date_entry.get(),
                "area": area_entry.get(),
                "status": status_entry.get(),
                "notes": notes_entry.get("1.0", tk.END).strip()
            }
            
            if not updated_crop["name"] or not updated_crop["type"]:
                messagebox.showerror("Lỗi", "Tên và loại cây không được để trống")
                return
            
            self.crop_manager.update_crop(crop_id, updated_crop)
            self.crop_manager.save_data()
            self.display_crops()
            edit_window.destroy()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin cây trồng")
        
        ttk.Button(form_frame, text="Cập nhật", command=update_crop).grid(row=6, column=0, columnspan=2, pady=15)
    
    def delete_crop(self):
        """Xóa cây trồng"""
        selected_item = self.crop_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cây trồng cần xóa")
            return
        
        item_data = self.crop_tree.item(selected_item[0], "values")
        crop_id = int(item_data[0])
        
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa cây trồng này?")
        if confirm:
            self.crop_manager.delete_crop(crop_id)
            self.crop_manager.save_data()
            self.display_crops()
            messagebox.showinfo("Thành công", "Đã xóa cây trồng")
    
    def show_animal_management(self):
        """Hiển thị màn hình quản lý vật nuôi"""
        self.clear_window()
        
        # Tạo frame chứa các control
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Nút thêm mới
        ttk.Button(control_frame, text="Thêm vật nuôi", command=self.show_add_animal_form).pack(side=tk.LEFT, padx=5)
        
        # Ô tìm kiếm
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.animal_search_entry = ttk.Entry(search_frame, width=30)
        self.animal_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm", command=self.search_animals).pack(side=tk.LEFT)
        
        # Tạo Treeview để hiển thị dữ liệu
        self.animal_tree = ttk.Treeview(self.root, columns=("ID", "Tên", "Loại", "Ngày nhập", "Số lượng", "Trạng thái"), show="headings")
        
        # Đặt tên cho các cột
        self.animal_tree.heading("ID", text="ID")
        self.animal_tree.heading("Tên", text="Tên")
        self.animal_tree.heading("Loại", text="Loại")
        self.animal_tree.heading("Ngày nhập", text="Ngày nhập")
        self.animal_tree.heading("Số lượng", text="Số lượng")
        self.animal_tree.heading("Trạng thái", text="Trạng thái")
        
        # Đặt độ rộng các cột
        self.animal_tree.column("ID", width=50, anchor=tk.CENTER)
        self.animal_tree.column("Tên", width=150)
        self.animal_tree.column("Loại", width=100)
        self.animal_tree.column("Ngày nhập", width=100, anchor=tk.CENTER)
        self.animal_tree.column("Số lượng", width=80, anchor=tk.CENTER)
        self.animal_tree.column("Trạng thái", width=100)
        
        self.animal_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.animal_tree, orient=tk.VERTICAL, command=self.animal_tree.yview)
        self.animal_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nút sửa và xóa
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Sửa", command=self.edit_animal).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Xóa", command=self.delete_animal).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Quay lại", command=self.show_main_menu).pack(side=tk.RIGHT)
        
        # Hiển thị dữ liệu
        self.display_animals()
    
    def display_animals(self, animals=None):
        """Hiển thị danh sách vật nuôi trên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.animal_tree.get_children():
            self.animal_tree.delete(item)
        
        # Hiển thị dữ liệu mới
        animals_to_display = animals if animals else self.animal_manager.animals
        for animal in animals_to_display:
            self.animal_tree.insert("", tk.END, values=(
                animal["id"],
                animal["name"],
                animal["type"],
                animal["entry_date"],
                animal["quantity"],
                animal["status"]
            ))
    
    def search_animals(self):
        """Tìm kiếm vật nuôi"""
        keyword = self.animal_search_entry.get().lower()
        if not keyword:
            self.display_animals()
            return
        
        filtered_animals = [
            animal for animal in self.animal_manager.animals
            if (keyword in animal["name"].lower() or 
                keyword in animal["type"].lower() or 
                keyword in animal["status"].lower())
        ]
        self.display_animals(filtered_animals)
    
    def show_add_animal_form(self):
        """Hiển thị form thêm vật nuôi mới"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm vật nuôi mới")
        add_window.geometry("500x400")
        
        ttk.Label(add_window, text="THÊM VẬT NUÔI MỚI", font=('Arial', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Các trường thông tin
        ttk.Label(form_frame, text="Tên vật nuôi:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Loại vật nuôi:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_entry = ttk.Entry(form_frame)
        type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ngày nhập:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Số lượng:").grid(row=3, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(form_frame)
        quantity_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        status_entry = ttk.Entry(form_frame)
        status_entry.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        notes_entry = tk.Text(form_frame, height=5, width=30)
        notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def save_animal():
            try:
                new_animal = {
                    "id": len(self.animal_manager.animals) + 1,
                    "name": name_entry.get(),
                    "type": type_entry.get(),
                    "entry_date": date_entry.get(),
                    "quantity": int(quantity_entry.get()),
                    "status": status_entry.get(),
                    "notes": notes_entry.get("1.0", tk.END).strip()
                }
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên")
                return
            
            if not new_animal["name"] or not new_animal["type"]:
                messagebox.showerror("Lỗi", "Tên và loại vật nuôi không được để trống")
                return
            
            self.animal_manager.add_animal(new_animal)
            self.animal_manager.save_data()
            self.display_animals()
            add_window.destroy()
            messagebox.showinfo("Thành công", "Đã thêm vật nuôi mới")
        
        ttk.Button(form_frame, text="Lưu", command=save_animal).grid(row=6, column=0, columnspan=2, pady=15)
    
    def edit_animal(self):
        """Sửa thông tin vật nuôi"""
        selected_item = self.animal_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn vật nuôi cần sửa")
            return
        
        item_data = self.animal_tree.item(selected_item[0], "values")
        animal_id = int(item_data[0])
        
        # Tìm vật nuôi cần sửa
        animal_to_edit = None
        for animal in self.animal_manager.animals:
            if animal["id"] == animal_id:
                animal_to_edit = animal
                break
        
        if not animal_to_edit:
            messagebox.showerror("Lỗi", "Không tìm thấy vật nuôi cần sửa")
            return
        
        # Hiển thị form sửa
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa thông tin vật nuôi")
        edit_window.geometry("500x400")
        
        ttk.Label(edit_window, text="SỬA THÔNG TIN VẬT NUÔI", font=('Arial', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Các trường thông tin
        ttk.Label(form_frame, text="Tên vật nuôi:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, animal_to_edit["name"])
        name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Loại vật nuôi:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_entry = ttk.Entry(form_frame)
        type_entry.insert(0, animal_to_edit["type"])
        type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ngày nhập:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.insert(0, animal_to_edit["entry_date"])
        date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Số lượng:").grid(row=3, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(form_frame)
        quantity_entry.insert(0, str(animal_to_edit["quantity"]))
        quantity_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        status_entry = ttk.Entry(form_frame)
        status_entry.insert(0, animal_to_edit["status"])
        status_entry.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        notes_entry = tk.Text(form_frame, height=5, width=30)
        notes_entry.insert("1.0", animal_to_edit.get("notes", ""))
        notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_animal():
            try:
                updated_animal = {
                    "id": animal_id,
                    "name": name_entry.get(),
                    "type": type_entry.get(),
                    "entry_date": date_entry.get(),
                    "quantity": int(quantity_entry.get()),
                    "status": status_entry.get(),
                    "notes": notes_entry.get("1.0", tk.END).strip()
                }
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên")
                return
            
            if not updated_animal["name"] or not updated_animal["type"]:
                messagebox.showerror("Lỗi", "Tên và loại vật nuôi không được để trống")
                return
            
            self.animal_manager.update_animal(animal_id, updated_animal)
            self.animal_manager.save_data()
            self.display_animals()
            edit_window.destroy()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin vật nuôi")
        
        ttk.Button(form_frame, text="Cập nhật", command=update_animal).grid(row=6, column=0, columnspan=2, pady=15)
    
    def delete_animal(self):
        """Xóa vật nuôi"""
        selected_item = self.animal_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn vật nuôi cần xóa")
            return
        
        item_data = self.animal_tree.item(selected_item[0], "values")
        animal_id = int(item_data[0])
        
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa vật nuôi này?")
        if confirm:
            self.animal_manager.delete_animal(animal_id)
            self.animal_manager.save_data()
            self.display_animals()
            messagebox.showinfo("Thành công", "Đã xóa vật nuôi")
    
    def show_activity_management(self):
        """Hiển thị màn hình quản lý hoạt động"""
        self.clear_window()
        
        # Tạo frame chứa các control
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Nút thêm mới
        ttk.Button(control_frame, text="Thêm hoạt động", command=self.show_add_activity_form).pack(side=tk.LEFT, padx=5)
        
        # Ô tìm kiếm
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.activity_search_entry = ttk.Entry(search_frame, width=30)
        self.activity_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm", command=self.search_activities).pack(side=tk.LEFT)
        
        # Tạo Treeview để hiển thị dữ liệu
        self.activity_tree = ttk.Treeview(self.root, columns=("ID", "Tên", "Loại", "Ngày", "Người phụ trách", "Trạng thái"), show="headings")
        
        # Đặt tên cho các cột
        self.activity_tree.heading("ID", text="ID")
        self.activity_tree.heading("Tên", text="Tên hoạt động")
        self.activity_tree.heading("Loại", text="Loại hoạt động")
        self.activity_tree.heading("Ngày", text="Ngày thực hiện")
        self.activity_tree.heading("Người phụ trách", text="Người phụ trách")
        self.activity_tree.heading("Trạng thái", text="Trạng thái")
        
        # Đặt độ rộng các cột
        self.activity_tree.column("ID", width=50, anchor=tk.CENTER)
        self.activity_tree.column("Tên", width=200)
        self.activity_tree.column("Loại", width=120)
        self.activity_tree.column("Ngày", width=100, anchor=tk.CENTER)
        self.activity_tree.column("Người phụ trách", width=150)
        self.activity_tree.column("Trạng thái", width=100)
        
        self.activity_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.activity_tree, orient=tk.VERTICAL, command=self.activity_tree.yview)
        self.activity_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Nút sửa và xóa
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Sửa", command=self.edit_activity).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Xóa", command=self.delete_activity).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Quay lại", command=self.show_main_menu).pack(side=tk.RIGHT)
        
        # Hiển thị dữ liệu
        self.display_activities()
    
    def display_activities(self, activities=None):
        """Hiển thị danh sách hoạt động trên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        # Hiển thị dữ liệu mới
        activities_to_display = activities if activities else self.activity_manager.activities
        for activity in activities_to_display:
            self.activity_tree.insert("", tk.END, values=(
                activity["id"],
                activity["name"],
                activity["type"],
                activity["date"],
                activity["responsible"],
                activity["status"]
            ))
    
    def search_activities(self):
        """Tìm kiếm hoạt động"""
        keyword = self.activity_search_entry.get().lower()
        if not keyword:
            self.display_activities()
            return
        
        filtered_activities = [
            activity for activity in self.activity_manager.activities
            if (keyword in activity["name"].lower() or 
                keyword in activity["type"].lower() or 
                keyword in activity["responsible"].lower() or
                keyword in activity["status"].lower())
        ]
        self.display_activities(filtered_activities)
    
    def show_add_activity_form(self):
        """Hiển thị form thêm hoạt động mới"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm hoạt động mới")
        add_window.geometry("500x400")
        
        ttk.Label(add_window, text="THÊM HOẠT ĐỘNG MỚI", font=('Arial', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Các trường thông tin
        ttk.Label(form_frame, text="Tên hoạt động:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Loại hoạt động:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_entry = ttk.Entry(form_frame)
        type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ngày thực hiện:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Người phụ trách:").grid(row=3, column=0, sticky=tk.W, pady=5)
        responsible_entry = ttk.Entry(form_frame)
        responsible_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        status_entry = ttk.Entry(form_frame)
        status_entry.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Mô tả:").grid(row=5, column=0, sticky=tk.W, pady=5)
        description_entry = tk.Text(form_frame, height=5, width=30)
        description_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def save_activity():
            new_activity = {
                "id": len(self.activity_manager.activities) + 1,
                "name": name_entry.get(),
                "type": type_entry.get(),
                "date": date_entry.get(),
                "responsible": responsible_entry.get(),
                "status": status_entry.get(),
                "description": description_entry.get("1.0", tk.END).strip()
            }
            
            if not new_activity["name"] or not new_activity["type"]:
                messagebox.showerror("Lỗi", "Tên và loại hoạt động không được để trống")
                return
            
            self.activity_manager.add_activity(new_activity)
            self.activity_manager.save_data()
            self.display_activities()
            add_window.destroy()
            messagebox.showinfo("Thành công", "Đã thêm hoạt động mới")
        
        ttk.Button(form_frame, text="Lưu", command=save_activity).grid(row=6, column=0, columnspan=2, pady=15)
    
    def edit_activity(self):
        """Sửa thông tin hoạt động"""
        selected_item = self.activity_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hoạt động cần sửa")
            return
        
        item_data = self.activity_tree.item(selected_item[0], "values")
        activity_id = int(item_data[0])
        
        # Tìm hoạt động cần sửa
        activity_to_edit = None
        for activity in self.activity_manager.activities:
            if activity["id"] == activity_id:
                activity_to_edit = activity
                break
        
        if not activity_to_edit:
            messagebox.showerror("Lỗi", "Không tìm thấy hoạt động cần sửa")
            return
        
        # Hiển thị form sửa
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa thông tin hoạt động")
        edit_window.geometry("500x400")
        
        ttk.Label(edit_window, text="SỬA THÔNG TIN HOẠT ĐỘNG", font=('Arial', 14)).pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Các trường thông tin
        ttk.Label(form_frame, text="Tên hoạt động:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.insert(0, activity_to_edit["name"])
        name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Loại hoạt động:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_entry = ttk.Entry(form_frame)
        type_entry.insert(0, activity_to_edit["type"])
        type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ngày thực hiện:").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.insert(0, activity_to_edit["date"])
        date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Người phụ trách:").grid(row=3, column=0, sticky=tk.W, pady=5)
        responsible_entry = ttk.Entry(form_frame)
        responsible_entry.insert(0, activity_to_edit["responsible"])
        responsible_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        status_entry = ttk.Entry(form_frame)
        status_entry.insert(0, activity_to_edit["status"])
        status_entry.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Mô tả:").grid(row=5, column=0, sticky=tk.W, pady=5)
        description_entry = tk.Text(form_frame, height=5, width=30)
        description_entry.insert("1.0", activity_to_edit.get("description", ""))
        description_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_activity():
            updated_activity = {
                "id": activity_id,
                "name": name_entry.get(),
                "type": type_entry.get(),
                "date": date_entry.get(),
                "responsible": responsible_entry.get(),
                "status": status_entry.get(),
                "description": description_entry.get("1.0", tk.END).strip()
            }
            
            if not updated_activity["name"] or not updated_activity["type"]:
                messagebox.showerror("Lỗi", "Tên và loại hoạt động không được để trống")
                return
            
            self.activity_manager.update_activity(activity_id, updated_activity)
            self.activity_manager.save_data()
            self.display_activities()
            edit_window.destroy()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin hoạt động")
        
        ttk.Button(form_frame, text="Cập nhật", command=update_activity).grid(row=6, column=0, columnspan=2, pady=15)
    
    def delete_activity(self):
        """Xóa hoạt động"""
        selected_item = self.activity_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hoạt động cần xóa")
            return
        
        item_data = self.activity_tree.item(selected_item[0], "values")
        activity_id = int(item_data[0])
        
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa hoạt động này?")
        if confirm:
            self.activity_manager.delete_activity(activity_id)
            self.activity_manager.save_data()
            self.display_activities()
            messagebox.showinfo("Thành công", "Đã xóa hoạt động")
    
    def export_excel(self):
        """Xuất báo cáo Excel"""
        if self.current_user["type"] != "admin":
            messagebox.showerror("Lỗi", "Chỉ quản trị viên mới có quyền xuất báo cáo")
            return

        # Hiển thị hộp thoại chọn loại báo cáo
        report_type = tk.StringVar(value="crops")
        dialog = tk.Toplevel(self.root)
        dialog.title("Chọn loại báo cáo")
        dialog.geometry("300x200")

        ttk.Label(dialog, text="Chọn loại báo cáo:", font=("Arial", 12)).pack(pady=10)
        ttk.Radiobutton(dialog, text="Cây trồng", variable=report_type, value="crops").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Vật nuôi", variable=report_type, value="animals").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Hoạt động", variable=report_type, value="activities").pack(anchor=tk.W, padx=20)

        def generate_report():
            selected_type = report_type.get()
            if selected_type == "crops":
                data = self.crop_manager.crops
            elif selected_type == "animals":
                data = self.animal_manager.animals
            elif selected_type == "activities":
                data = self.activity_manager.activities
            else:
                messagebox.showerror("Lỗi", "Loại báo cáo không hợp lệ")
                return

            try:
                filepath = ReportGenerator.generate_excel_report(data, selected_type)
                messagebox.showinfo("Thành công", f"Báo cáo đã được lưu tại: {filepath}")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo báo cáo: {str(e)}")

        ttk.Button(dialog, text="Xuất báo cáo", command=generate_report).pack(pady=20)
        ttk.Button(dialog, text="Hủy", command=dialog.destroy).pack()

        
    def logout(self):
        """Đăng xuất"""
        self.save_data()
        self.current_user = None
        self.show_login_screen()
    
    def exit_app(self):
        """Thoát ứng dụng"""
        self.save_data()
        self.root.quit()
    
    def clear_window(self):
        """Xóa tất cả widget trên cửa sổ chính"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Xóa thanh menu nếu có
        try:
            self.root.config(menu=tk.Menu(self.root))
        except:
            pass
