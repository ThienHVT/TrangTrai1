import json
import os
from hashlib import sha256

class AuthManager:
    def __init__(self):
        self.users = []
        self.current_user = None
        self.users_file = "data/users.json"
    
    def load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, "r", encoding="utf-8") as f:
                    try:
                        self.users = json.load(f)
                        # Đảm bảo users là một list
                        if not isinstance(self.users, list):
                            self.users = []
                    except json.JSONDecodeError:
                        # Nếu file trống hoặc không hợp lệ, khởi tạo danh sách trống
                        self.users = []
            else:
                # Tạo thư mục data nếu chưa tồn tại
                os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
                # Tạo admin mặc định nếu file không tồn tại
                self.users = [
                    {
                        "username": "admin",
                        "password": self.hash_password("admin123"),
                        "type": "admin"
                    }
                ]
                self.save_users()
        except Exception as e:
            print(f"Error loading users: {str(e)}")
            self.users = []
    
    def save_users(self):
        """Lưu danh sách người dùng vào file JSON"""
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def hash_password(self, password):
        """Mã hóa mật khẩu"""
        #return sha256(password.encode("utf-8")).hexdigest()
        return password
    
    def register_user(self, username, password, user_type="user"):
        """Đăng ký người dùng mới"""
        # Kiểm tra username đã tồn tại chưa
        for user in self.users:
            if user["username"] == username:
                return {
                    "success": False,
                    "message": "Tên đăng nhập đã tồn tại"
                }
        
        # Thêm người dùng mới
        new_user = {
            "username": username,
            "password": self.hash_password(password),
            "type": user_type
        }
        self.users.append(new_user)
        self.save_users()
        
        return {
            "success": True,
            "message": "Đăng ký thành công"
        }
    
    def login(self, username, password):
        """Đăng nhập"""
        for user in self.users:
            if user["username"] == username and user["password"] == self.hash_password(password):
                self.current_user = user
                return {
                    "success": True,
                    "message": "Đăng nhập thành công",
                    "user": user
                }
        
        return {
            "success": False,
            "message": "Tên đăng nhập hoặc mật khẩu không đúng"
        }
    
    def change_password(self, username, current_password, new_password):
        """Đổi mật khẩu"""
        for user in self.users:
            if user["username"] == username and user["password"] == self.hash_password(current_password):
                user["password"] = self.hash_password(new_password)
                self.save_users()
                return {
                    "success": True,
                    "message": "Đổi mật khẩu thành công"
                }
        
        return {
            "success": False,
            "message": "Mật khẩu hiện tại không đúng"
        }