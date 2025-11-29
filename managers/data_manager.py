import json
import os

class DataManager:
    """
    مسؤول عن حفظ واسترجاع البيانات من ملفات JSON.
    """
    
    @staticmethod
    def save_data(data, filename):
        """
        يحفظ قائمة من القواميس في ملف JSON داخل مجلد data
        """
        # التأكد من وجود مجلد data
        if not os.path.exists('data'):
            os.makedirs('data')

        file_path = os.path.join('data', filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"✔ Data saved successfully to {filename}")
        except Exception as e:
            print(f"✖ Error saving data: {e}")

    @staticmethod
    def load_data(filename):
        """
        يقرأ البيانات من ملف JSON ويعيدها كقائمة
        """
        file_path = os.path.join('data', filename)
        
        # لو الملف مش موجود، نرجع قائمة فاضية بدل ما البرنامج يضرب
        if not os.path.exists(file_path):
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"✖ Error loading data: {e}")
            return []
        