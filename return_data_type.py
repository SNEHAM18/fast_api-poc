from pydantic import BaseModel
from fastapi import FastAPI ,Body,Form,UploadFile,File
app=FastAPI()
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool

@app.post("/json/")
def create_item(item: Item):
   return {
   "type":"json",
   "json_list":[item],
   "name":item.name,
    "price":item.price,
    "in_stock":item.in_stock,
    "survey":"completed"
   }

# text data type



@app.post("/text")
def receive_text(content: str = Body(..., media_type="text/plain")):
    return {
        "type": "Plain Text",
        "content": content
    }


@app.post("/form")
def receive_form(name: str = Form(...),password: str = Form(...)):
    if not name:
        return {"error": "Name is required"}
    if not password:
        return {"error": "Password is required"}
    password_length = len(password)
    if password_length < 6:
        return {"error": "Password must be at least 6 characters long"}
    return {
        "type": "Form Data",
        "name": name,
        "password": password,
        "survey":"completed"
    }


@app.post("/file")
def receive_file(file: UploadFile = File(...)):
    return {
        "type": "File Upload",
        "filename": file.filename,
        "content_type": file.content_type,
        "survey":"completed"
    }
