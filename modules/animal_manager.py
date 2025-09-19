import json
import os

class AnimalManager:
    def __init__(self):
        self.animals = []
        self.data_file = "data/animals.json"
    
    def load_data(self):
        """Tải dữ liệu vật nuôi từ file JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.animals = json.load(f)
            else:
                self.animals = []
        except Exception as e:
            self.animals = []
            raise e
    
    def save_data(self):
        """Lưu dữ liệu vật nuôi vào file JSON"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.animals, f, ensure_ascii=False, indent=2)
    
    def add_animal(self, animal_data):
        """Thêm vật nuôi mới"""
        self.animals.append(animal_data)
    
    def update_animal(self, animal_id, updated_data):
        """Cập nhật thông tin vật nuôi"""
        for i, animal in enumerate(self.animals):
            if animal["id"] == animal_id:
                self.animals[i] = updated_data
                return True
        return False
    
    def delete_animal(self, animal_id):
        """Xóa vật nuôi"""
        self.animals = [animal for animal in self.animals if animal["id"] != animal_id]
    
    def get_animal_by_id(self, animal_id):
        """Lấy thông tin vật nuôi theo ID"""
        for animal in self.animals:
            if animal["id"] == animal_id:
                return animal
        return None