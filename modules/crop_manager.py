import json
import os

class CropManager:
    def __init__(self):
        self.crops = []
        self.data_file = "data/crops.json"
    
    def load_data(self):
        """Tải dữ liệu cây trồng từ file JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.crops = json.load(f)
            else:
                self.crops = []
        except Exception as e:
            self.crops = []
            raise e
    
    def save_data(self):
        """Lưu dữ liệu cây trồng vào file JSON"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.crops, f, ensure_ascii=False, indent=2)
    
    def add_crop(self, crop_data):
        """Thêm cây trồng mới"""
        self.crops.append(crop_data)
    
    def update_crop(self, crop_id, updated_data):
        """Cập nhật thông tin cây trồng"""
        for i, crop in enumerate(self.crops):
            if crop["id"] == crop_id:
                self.crops[i] = updated_data
                return True
        return False
    
    def delete_crop(self, crop_id):
        """Xóa cây trồng"""
        self.crops = [crop for crop in self.crops if crop["id"] != crop_id]
    
    def get_crop_by_id(self, crop_id):
        """Lấy thông tin cây trồng theo ID"""
        for crop in self.crops:
            if crop["id"] == crop_id:
                return crop
        return None