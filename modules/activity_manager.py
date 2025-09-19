import json
import os

class ActivityManager:
    def __init__(self):
        self.activities = []
        self.data_file = "data/activities.json"
    
    def load_data(self):
        """Tải dữ liệu hoạt động từ file JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.activities = json.load(f)
            else:
                self.activities = []
        except Exception as e:
            self.activities = []
            raise e
    
    def save_data(self):
        """Lưu dữ liệu hoạt động vào file JSON"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.activities, f, ensure_ascii=False, indent=2)
    
    def add_activity(self, activity_data):
        """Thêm hoạt động mới"""
        self.activities.append(activity_data)
    
    def update_activity(self, activity_id, updated_data):
        """Cập nhật thông tin hoạt động"""
        for i, activity in enumerate(self.activities):
            if activity["id"] == activity_id:
                self.activities[i] = updated_data
                return True
        return False
    
    def delete_activity(self, activity_id):
        """Xóa hoạt động"""
        self.activities = [activity for activity in self.activities if activity["id"] != activity_id]
    
    def get_activity_by_id(self, activity_id):
        """Lấy thông tin hoạt động theo ID"""
        for activity in self.activities:
            if activity["id"] == activity_id:
                return activity
        return None