from config import *
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import bcrypt
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
    Status = Column(Enum('open', 'progress', 'closed', 'reopened','waiting for information'), default='open')
    Priority = Column(Enum('critical', 'high', 'medium', 'low'), default='medium')
    Issue_Type = Column(Enum('bug', 'error', 'issue', 'story', 'others', 'feature', 'enhancement', 'support','task'), default='issue')
    Channel = Column(String(100))
    Customer_ID = Column(Integer, ForeignKey('customer.Id', ondelete='SET NULL'))
    Customer_Username = Column(String(255)) 
    Product_Type = Column(String(100))
    Medium = Column(String(100))
    Team = Column(String(50))
    Assignee_ID = Column(Integer, ForeignKey('employee.id', ondelete='SET NULL'))
    Assignee_Username = Column(String(255))
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
            'ticket_id': str(self.Ticket_Id),
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
            'user': self.Customer_Username,
            'product_type': self.Product_Type,
            'medium': self.Medium,
            'team': self.Team,
            'assignee': self.Assignee_Username,
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
        if self.Estimation == None or self.Estimation == '':
            self.Estimation = 0
            print(f"Estimation set to: {self.Estimation}")
        if self.Story_Points == None or self.Story_Points == '':
            self.Story_Points = 0
            print(f"Story Points set to: {self.Story_Points}")
        if self.Priority == None or self.Priority == '':
            self.Priority = 'low'
            print(f"Priority set to: {self.Priority}")
        if self.Issue_Type == None or self.Issue_Type == '':
            self.Issue_Type = 'issue'
            print(f"Issue Type set to: {self.Issue_Type}")
        if not self.Subject and not self.Description:
            print("Subject validation failed.")
            return "Subject or Description must be provided and less than 255 characters."
        if self.Status.lower() not in ["open", "progress", "closed", "reopened", "waiting for information"]:
            self.Status = 'open'
            print(f"Status set to: {self.Status}")
        if self.Priority.lower() not in ["critical", "high", "medium", "low", ""]:
            print(f"Invalid Priority: {self.Priority}")
            self.Priority = 'low'
            print(f"Priority set to: {self.Priority}")
        if self.Score is not None and (self.Score < 0 or self.Score > 100):
            print("Score validation failed.")
            return "Score must be between 0 and 100."

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
    def get_all_customers(self):
        customers = db_session.query(Customer).all()
        customers_dict = {}
        for customer in customers:
            customers_dict[customer.username] = {} 
            customers_dict[customer.username]['name'] = customer.name
            customers_dict[customer.username]['age'] = customer.age
            customers_dict[customer.username]['email'] = customer.email
            customers_dict[customer.username]['company'] = customer.company
            customers_dict[customer.username]['score'] = customer.score
            customers_dict[customer.username]['gender'] = customer.gender
            customers_dict[customer.username]['id'] = customer.Id
            customers_dict[customer.username]['phone'] = customer.phone
            customers_dict[customer.username]['role'] = customer.role
            customers_dict[customer.username]['password'] = customer.password
            customers_dict[customer.username]['type'] = 'customer'
        return customers_dict

    def getIDfromUsername(self, username):
        print("Customer Username: ", username)
        customer = db_session.query(Customer).filter_by(username=username).first()
        # print(customer.Id if customer else 1)
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
    closed_tickets = Column(Integer)
    open_tickets = Column(Integer)
    team = Column(String(50))
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
    def get_all_employees(self):
        employees = db_session.query(Employee).all()
        employees_dict = {}
        for employee in employees:
            emp_detail={}
            emp_detail['id'] = employee.id
            emp_detail['gcm'] = employee.gcm
            emp_detail['email'] = employee.email
            emp_detail['phone'] = employee.phone
            emp_detail['role'] = employee.role
            emp_detail['team'] = employee.team
            emp_detail['score'] = employee.score
            emp_detail['manager'] = employee.manager
            emp_detail['experience'] = employee.experience
            emp_detail['closed_tickets'] = employee.closed_tickets
            emp_detail['open_tickets'] = employee.open_tickets
            emp_detail['name'] = employee.name
            emp_detail['age'] = employee.age
            emp_detail["password"] = employee.password
            emp_detail["type"] = "employee"
            employees_dict[employee.username] = emp_detail
        return employees_dict
    

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
        
class AuthView(Base):
    __tablename__ = 'auth_view'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    phone = Column(String)
    role = Column(String)
    user_type = Column(String)

    def serialize(self, keys=None):
        data = {
            'user_id': self.user_id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'user_type': self.user_type
        }
        
        if keys:
            return {key: data[key] for key in keys if key in data}
        return data
    def validate_password(self,password):
        #convert password to bcrypt hash and check if it matches the stored hash
        # bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        bcrypt_hash = self.password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), bcrypt_hash)
        return self.password == password
    def get_user_type(self):
        return self.user_type
    def get_user(self, email):
        return db_session.query(AuthView).filter_by(email=email).first()
    def change_password(self, email, password):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            user = db_session.query(AuthView).filter_by(email=email).first()
            if user.user_type == 'employee':
                db_session.query(Employee).filter_by(email=email).update({'password': hashed_password})
            elif user.user_type == 'customer':
                db_session.query(Customer).filter_by(email=email).update({'password': hashed_password})
            
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error changing password: {e}")
            return False
        
def get_all_users():
    customers = Customer().get_all_customers()
    employees = Employee().get_all_employees()
    all_users = {**customers, **employees}
    print("\n\n\n", all_users)
    return all_users
