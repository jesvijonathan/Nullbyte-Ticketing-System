from config import *
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import validator_collection
from database import Base

class Ticket(Base):
    __tablename__ = 'ticket'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Subject = Column(String(255), nullable=False)
    Type = Column(String(100))
    Description = Column(Text, nullable=False)
    Status = Column(Enum('Open', 'In Progress', 'Closed', 'Reopened'), nullable=False)
    Priority = Column(Enum('Low', 'Medium', 'High'), nullable=False)
    Channel = Column(String(100))
    Customer_ID = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'))
    Product_ID = Column(Integer)
    Assignee_ID = Column(Integer, ForeignKey('employee.id', ondelete='SET NULL'))
    Resolution = Column(Text)
    Issue_Date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    First_Response_Time = Column(DateTime)
    Time_to_Resolution = Column(Integer)
    Reopens = Column(Integer, default=0)
    Score = Column(Integer)

    customer = relationship("Customer", back_populates="tickets")
    assignee = relationship("Employee", back_populates="assigned_tickets")

    def validate(self):
        if not self.Subject or len(self.Subject) > 255:
            return "Subject must be provided and less than 255 characters."
        if not self.Description:
            return "Description must be provided."
        if self.Status not in ['Open', 'In Progress', 'Closed', 'Reopened']:
            return "Status must be one of 'Open', 'In Progress', 'Closed', 'Reopened'."
        if self.Priority not in ['Low', 'Medium', 'High']:
            return "Priority must be one of 'Low', 'Medium', 'High'."
        if self.Customer_ID is None:
            return "Customer_ID must be provided."
        if self.Assignee_ID is None:
            return "Assignee_ID must be provided."
        if self.Score is not None and (self.Score < 0 or self.Score > 100):
            return "Score must be between 0 and 100."
        if self.First_Response_Time and not isinstance(self.First_Response_Time, datetime):
            return "First_Response_Time must be a datetime object."
        if self.Time_to_Resolution and not isinstance(self.Time_to_Resolution, int):
            return "Time_to_Resolution must be an integer."

        if self.Reopens and not isinstance(self.Reopens, int):
            return "Reopens must be an integer."

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    company = Column(String(255))
    role = Column(String(100))
    score = Column(Integer)

    tickets = relationship("Ticket", back_populates="customer")

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    role = Column(String(100))
    score = Column(Integer)
    Manager = Column(Integer, ForeignKey('employee.id', ondelete='SET NULL'))
    GCM = Column(String(100))
    Experience = Column(Integer)

    assigned_tickets = relationship("Ticket", back_populates="assignee")
    manager = relationship("Employee", remote_side=[id])
