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
    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")
    worklogs = relationship("Worklog", back_populates="ticket", cascade="all, delete-orphan")

    def serialize(self, keys=None):
        data = {
            'ticket_id': self.Ticket_Id,
            'chat_id': self.Chat_Id,
            'subject': self.Subject,
            'summary': self.Summary,
            'analysis': self.Analysis,
            'type': self.Type,
            'description': self.Description,
            'status': self.Status,
            'priority': self.Priority,
            'issue_type': self.Issue_Type,
            'channel': self.Channel,
            'customer_id': self.Customer_ID,
            'product_id': self.Product_ID,
            'medium': self.Medium,
            'team': self.Team,
            'assignee_id': self.Assignee_ID,
            'resolution': self.Resolution,
            'issue_date': self.Issue_Date.isoformat() if self.Issue_Date else None,
            'first_response_time': self.First_Response_Time.isoformat() if self.First_Response_Time else None,
            'time_to_resolution': self.Time_to_Resolution,
            'reopens': self.Reopens,
            'story_points': self.Story_Points,
            'score': self.Score,
            'attachments': list(set([attachment.serialize()["url"] for attachment in self.attachments])),
            'comments': [comment.serialize() for comment in self.comments],
            'worklogs': [worklog.serialize() for worklog in self.worklogs]
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
    def getIDfromEmail(self, email):
        print("Email: ", email)
        employee = db_session.query(Employee).filter_by(email=email).first()
        print(employee.id if employee else 1)
        return employee.id if employee else 1

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
class Comment(Base):
    __tablename__ = 'comments'
    Comment_id = Column(Integer, primary_key=True, autoincrement=True)
    Ticket_id = Column(Integer, ForeignKey('ticket.Ticket_Id', ondelete='CASCADE'), nullable=False)
    Timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    Comment_user = Column(Integer, nullable=False)
    Comment = Column(Text, nullable=False)

    # Define relationship to Ticket
    ticket = relationship("Ticket", back_populates="comments")

    def serialize(self, keys=None):
        data = {
            'comment_id': self.Comment_id,
            'ticket_id': self.Ticket_id,
            'timestamp': self.Timestamp.isoformat() if self.Timestamp else None,
            'comment_user': self.Comment_user,
            'comment': self.Comment
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data
    
class Worklog(Base):
        __tablename__ = 'worklog'
        Id = Column(Integer, primary_key=True, autoincrement=True)
        Ticket_Id = Column(Integer, ForeignKey('ticket.Ticket_Id', ondelete='CASCADE'), nullable=False)
        Worklog_User = Column(Integer, ForeignKey('employee.id', ondelete='SET NULL'), nullable=False)
        Worklog_Date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
        Worklog_Hours = Column(Integer, nullable=False)
        Worklog = Column(Text, nullable=False)

        ticket = relationship("Ticket", back_populates="worklogs")
        user = relationship("Employee")

        def serialize(self, keys=None):
            data = {
                'id': self.Id,
                'worklog_user': self.Worklog_User,
                'worklog_date': self.Worklog_Date.isoformat() if self.Worklog_Date else None,
                'worklog_hours': self.Worklog_Hours,
                'worklog': self.Worklog
            }
            
            if keys:
                return {key: data[key] for key in keys if key in data}
            return data