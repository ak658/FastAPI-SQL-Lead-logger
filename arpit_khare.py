from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from fastapi.responses import HTMLResponse
app= FastAPI()
DB_URL = "sqlite:///my_first_database.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
with engine.connect() as connection:
    connection.execute(text(""" CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, message TEXT NOT NULL ) """))
    connection.commit()
class LeadStructure(BaseModel):
    name: str = Field(...,min_length=2,max_length=50)
    email: str
    phone: str = Field(...,min_length=10,max_length=15)
    message: str = None
@app.get("/", response_class=HTMLResponse)
def home():
      return """
      <h1>welcome to the lead management system</h1>"""
@app.post("/add-lead")
def add_new_lead(lead: LeadStructure):
     try:
          with engine.connect() as connection:
               query=text("INSERT INTO leads (name, email, phone,message) VALUES (:name,:email,:phone,:message)")
               connection.execute(query,{"name":lead.name,"email":lead.email,"phone":lead.phone,"message":lead.message})
               connection.commit()
               return {"status":"success","message":f"Lead for {lead.name} saved in SQL database!"}
     except Exception as e:
          raise HTTPException(status_code=500, detail=f"Database Issue:{str(e)}")
@app.get("/view-leads")
def view_all_leads():
     with engine.connect() as connection:
          result = connection.execute(text("SELECT*FROM leads;"))
          leads_list = [dict(row._mapping) for row in result]
          return {"total_leads":len(leads_list),"data":leads_list}



