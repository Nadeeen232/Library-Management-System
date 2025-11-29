from abc import ABC, abstractmethod

class LibraryItem(ABC):
   
    
    def __init__(self, item_id, title, subject):
        self._item_id = item_id          # Protected attribute
        self._title = title
        self._subject = subject
        self._is_checked_out = False     

    # --- Getters  ---
    @property
    def item_id(self):
        return self._item_id

    @property
    def title(self):
        return self._title

    @property
    def subject(self):
        return self._subject

    @property
    def is_checked_out(self):
        return self._is_checked_out

    # --- Methods ---
    def check_out(self):
        """تغيير الحالة إلى مستعار"""
        if self._is_checked_out:
            raise ValueError(f"Item '{self._title}' is already checked out.")
        self._is_checked_out = True

    def return_item(self):
        """تغيير الحالة إلى متاح"""
        self._is_checked_out = False

    def to_dict(self):
        """تحويل الكائن لقاموس لحفظه في ملفات البيانات"""
        return {
            "item_id": self._item_id,
            "title": self._title,
            "subject": self._subject,
            "is_checked_out": self._is_checked_out,
            "type": self.__class__.__name__ # لحفظ نوع الكلاس (Book/Magazine)
        }

    # دالة مجردة: تجبر المطورين الآخرين على كتابة تفاصيل كل مادة
    @abstractmethod
    def get_details(self):
        pass