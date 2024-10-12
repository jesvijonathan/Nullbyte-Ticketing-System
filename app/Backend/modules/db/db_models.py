from config import *
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base, db_session
from modules.log import *

class Ticket(Base):
    __tablename__ = 'ticket'
    Ticket_Id = Column(Integer, primary_key=True, autoincrement=True)
    Chat_Id = Column(String(50))
    Subject = Column(String(255), nullable=False)
    Summary = Column(Text, nullable=False)  # Changed to Text
    Analysis = Column(Text)
    Type = Column(String(100))
    Description = Column(Text, nullable=False)
    Status = Column(Enum('open', 'progress', 'closed', 'reopened', ''), nullable=False)  # Added empty string
    Priority = Column(Enum('critical', 'high', 'medium', 'low', ''), nullable=False)  # Added empty string
    Issue_Type = Column(Enum('bug', 'error', 'issue', 'story', 'others', 'feature', 'enhancement', 'support', ''), nullable=True)  # Added empty string
    Channel = Column(String(100))
    Customer_ID = Column(Integer, ForeignKey('customer.Id', ondelete='SET NULL'))  # Changed to SET NULL
    Product_ID = Column(String(100))
    Medium = Column(String(100))
    Team = Column(String(50))
    Assignee_ID = Column(Integer, ForeignKey('employee.id', ondelete='SET NULL'))
    Resolution = Column(Text)
    Issue_Date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    First_Response_Time = Column(DateTime)
    Time_to_Resolution = Column(Integer)
    Reopens = Column(Integer, default=0)
    Story_Points = Column(Integer)
    Score = Column(Integer)
    attachments = relationship("Attachment", back_populates="ticket")
    customer = relationship("Customer", back_populates="tickets")
    assignee = relationship("Employee", back_populates="assigned_tickets")

    def serialize(self, keys=None):
        data = {
            'Ticket_Id': self.Ticket_Id,
            'Chat_Id': self.Chat_Id,
            'Subject': self.Subject,
            'Summary': self.Summary,
            'Analysis': self.Analysis,
            'Type': self.Type,
            'Description': self.Description,
            'Status': self.Status,
            'Priority': self.Priority,
            'Issue_Type': self.Issue_Type,
            'Channel': self.Channel,
            'Customer_ID': self.Customer_ID,
            'Product_ID': self.Product_ID,
            'Medium': self.Medium,
            'Team': self.Team,
            'Assignee_ID': self.Assignee_ID,
            'Resolution': self.Resolution,
            'Issue_Date': self.Issue_Date.isoformat() if self.Issue_Date else None,
            'First_Response_Time': self.First_Response_Time.isoformat() if self.First_Response_Time else None,
            'Time_to_Resolution': self.Time_to_Resolution,
            'Reopens': self.Reopens,
            'Story_Points': self.Story_Points,
            'Score': self.Score,
            'attachments': [attachment.serialize()["url"] for attachment in self.attachments]
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data

    def validate(self):
        if not self.Subject or len(self.Subject) > 255:
            return "Subject must be provided and less than 255 characters."
        if self.Status not in ['open', 'progress', 'closed', 'reopened', '']:
            self.Status = 'open'
        if self.Priority not in ['critical', 'high', 'medium', 'low', '']:
            self.Priority = 'low'
        if self.Score is not None and (self.Score < 0 or self.Score > 100):
            return "Score must be between 0 and 100."
        if self.Reopens and not isinstance(self.Reopens, int):
            return "Reopens must be an integer."
        return None

class Customer(Base):
    __tablename__ = 'customer'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(Enum('Male', 'Female'))
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15))
    company = Column(String(255))
    role = Column(String(100))
    score = Column(Integer)

    tickets = relationship("Ticket", back_populates="customer")

    def serialize(self, keys=None):
        data = {
            'Id': self.Id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'role': self.role,
            'score': self.score
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data

    def getIDfromEmail(self, email):
        print("Email: ", email)
        customer = db_session.query(Customer).filter_by(email=email).first()
        print(customer.Id if customer else 1)
        return customer.Id if customer else 1

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(Enum('Male', 'Female'), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15))
    role = Column(String(100))
    score = Column(Integer)
    manager = Column(Integer, ForeignKey('employee.id', ondelete='SET NULL'))
    gcm = Column(Integer)
    experience = Column(Integer)

    assigned_tickets = relationship("Ticket", back_populates="assignee")
    manager_relationship = relationship("Employee", remote_side=[id])

    def serialize(self, keys=None):
        data = {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'score': self.score,
            'manager': self.manager,
            'gcm': self.gcm,
            'experience': self.experience
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data

class Attachment(Base):
    __tablename__ = 'attachments'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Ticket_Id = Column(Integer, ForeignKey('ticket.Ticket_Id', ondelete='CASCADE'), nullable=False)
    url = Column(Text, nullable=False)
    ticket = relationship('Ticket', back_populates='attachments')

    def serialize(self, keys=None):
        data = {
            'Id': self.Id,
            'Ticket_Id': self.Ticket_Id,
            'url': self.url
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data

    def addAttachment(self, ticket_id, url):
        try:
            new_attachment = Attachment(
                Ticket_Id=ticket_id,
                url=url
            )
            db_session.add(new_attachment)
            db_session.commit()
            return new_attachment.Id
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error adding attachment: {e}")
            return {'error': str(e)}