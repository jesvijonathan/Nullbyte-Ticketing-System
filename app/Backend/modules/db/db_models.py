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
    Summary = Column(Text, nullable=False)
    Analysis = Column(Text)
    Type = Column(String(100))
    Description = Column(Text, nullable=False)
    Status = Column(Enum('open', 'progress', 'closed', 'reopened','waiting for information'), nullable=False, default='open')
    Priority = Column(Enum('critical', 'high', 'medium', 'low'), nullable=False, default='medium')
    Issue_Type = Column(Enum('bug', 'error', 'issue', 'story', 'others', 'feature', 'enhancement', 'support','task'), nullable=True, default='issue')
    Channel = Column(String(100))
    Customer_ID = Column(Integer, ForeignKey('customer.Id', ondelete='SET NULL'))
    Product_Type = Column(String(100))
    Medium = Column(String(100))
    Team = Column(String(50))
    Assignee_ID = Column(Integer, ForeignKey('employee.id', ondelete='SET NULL'))
    Resolution = Column(Text)
    Issue_Date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    Created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    LastModified = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    Estimation = Column(Integer,default=0)
    Reopens = Column(Integer, default=0)
    Story_Points = Column(Integer)
    Score = Column(Integer,default=0)
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
            'text': self.Description,
            'status': self.Status,
            'priority': self.Priority,
            'issue_type': self.Issue_Type,
            'channel': self.Channel,
            'user': Customer().getUserNamefromID(self.Customer_ID),
            'product_type': self.Product_Type,
            'medium': self.Medium,
            'team': self.Team,
            'assignee': Employee().getUserNamefromID(self.Assignee_ID),
            'resolution': self.Resolution,
            'created': self.Created.isoformat() if self.Created else None,
            'last_modified': self.LastModified.isoformat() if self.LastModified else None,
            'estimation': self.Estimation,
            'reopens': self.Reopens,
            'story_points': self.Story_Points,
            'score': self.Score,
            'attachments': list([attachment.serialize() for attachment in self.attachments]),
            'comments': [comment.serialize() for comment in self.comments],
            'worklogs': [worklog.serialize() for worklog in self.worklogs]
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data

    def validate(self):
        if self.Estimation ==None or self.Estimation=='':
            self.Estimation=0
        if self.Story_Points ==None or self.Story_Points=='':
            self.Story_Points=0
        if not self.Subject or len(self.Subject) > 255:
            return "Subject must be provided and less than 255 characters."
        if self.Status.lower()not in ["open", "progress", "closed", "reopened", "waiting for information"]:
            self.Status = 'open'
        if self.Priority.lower() not in ["critical", "high", "medium", "low", ""]:  
            print(self.Priority)
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
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
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
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'role': self.role,
            'score': self.score
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data

    def getIDfromUsername(self, username):
        print("Customer Username: ", username)
        customer = db_session.query(Customer).filter_by(username=username).first()
        print(customer.Id if customer else 1)
        return customer.Id if customer else 1
    def getUserNamefromID(self, id):
        print("ID: ", id)
        customer = db_session.query(Customer).filter_by(Id=id).first()
        return customer.username if customer else "unassigned"
    def getallUsers(self):
        customers = db_session.query(Customer).all()
        return [customer.username for customer in customers]

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
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
            'username': self.username,
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
    def getIDfromUsername(self, username):
        print("Employee Username: ", username)
        employee = db_session.query(Employee).filter_by(username=username).first()
        print(employee.id if employee else 1)
        return employee.id if employee else 1
    def getUserNamefromID(self, id):
        print("ID: ", id)
        employee = db_session.query(Employee).filter_by(id=id).first()
        return employee.username if employee else "unassigned"
    def getallUsers(self):
        employees = db_session.query(Employee).all()
        return [employee.username for employee in employees]

class Attachment(Base):
    __tablename__ = 'attachments'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Ticket_Id = Column(Integer, ForeignKey('ticket.Ticket_Id', ondelete='CASCADE'), nullable=False)
    Name = Column(String(100), nullable=False)
    Type = Column(String(50), nullable=True)
    Size = Column(String(10), nullable=True)
    Url = Column(Text, nullable=False)
    
    ticket = relationship('Ticket', back_populates='attachments')

    def serialize(self, keys=None):
        data = {
            'name': self.Name,
            'type': self.Type,
            'size': self.Size,
            'url': self.Url
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data
    def add_attachment(self, ticket_id, name, type, size, url):
        try:
            new_attachment = Attachment(
                Ticket_Id=ticket_id,
                Name=name,
                Type=type,
                Size=size,
                Url=url
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
            'date': self.Timestamp.isoformat() if self.Timestamp else None,
            'user': self.Comment_user,
            'text': self.Comment
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data
    def add_comment(self, ticket_id, user_id, comment):
        try:
            new_comment = Comment(
                Ticket_id=ticket_id,
                Comment_user=user_id,
                Comment=comment
            )
            db_session.add(new_comment)
            db_session.commit()
            return new_comment.Comment_id
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error adding comment: {e}")
            return {'error': str(e)}
    def edit_comment(self, comment_id, comment):
        try:
            db_session.query(Comment).filter_by(Comment_id=comment_id).update({'Comment': comment})
            db_session.commit()
            return comment_id
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error editing comment: {e}")
            return {'error': str(e)}
    def delete_comments(self, ticket_id):
        try:
            db_session.query(Comment).filter_by(Ticket_id=ticket_id).delete()
            db_session.commit()
            return ticket_id
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error deleting comments: {e}")
            return {'error': str(e)}
    
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