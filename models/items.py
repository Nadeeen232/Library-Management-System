from models.library_items import LibraryItem
class Book(LibraryItem):
    def __init__(self,item_id,title,subject,author,isbn,pages):
        super().__init__(item_id,title,subject)
        self.author = author
        self.isbn = isbn
        self.pages = pages

    def to_dict(self):
        super().to_dict()
        data= super().to_dict()
        data["author"] = self.author
        data["isbn"] = self.isbn
        data["pages"] = self.pages
        return data

    def edit_item(self,new_author,new_isbn,new_pages):
        self.author = new_author
        self.isbn = new_isbn
        self.pages = new_pages

    def get_details(self):
        return {"author" : self.author, "isbn": self.isbn, "pages": self.pages}




class Magazine(LibraryItem):
    def __init__(self,item_id,title,subject,issue_number,publisher):
        super().__init__(item_id,title,subject)
        self.issue_number = issue_number
        self.publisher= publisher
    def get_details(self):
        return {"issue_number" : self.issue_number, "publisher": self.publisher}






class DVD(LibraryItem):
    def __init__(self,item_id,title,subject,duration,region_code):
        super().__init__(item_id,title,subject)
        self.duration = duration
        self.region_code= region_code
    def get_details(self):
        return {"duration" : self.duration, "region_code": self.region_code}
