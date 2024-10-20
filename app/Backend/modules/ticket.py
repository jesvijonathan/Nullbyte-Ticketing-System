import mimetypes
import random
from flask import Blueprint
from flask import request, make_response, jsonify, render_template
from werkzeug.utils import secure_filename
from modules.bucket import upload_individual_files
from config import *
from .db.db_models import Ticket, Employee,Customer,Attachment,Comment,Worklog
from .auth.auth import jwt_required
from .db.database import db_session
from .log import *
from sqlalchemy import select
from datetime import datetime, timezone
from mimetypes import guess_extension
import base64
import datetime

ticket=Blueprint('ticket',__name__)

@ticket.route('/list', methods=['GET'])
@jwt_required
def get_all_tickets(*args, **kwargs):
    payload = kwargs.get('payload')
    assignee_id = request.args.get('Assignee_ID')

    if not assignee_id:
        username = payload.get('upn')        
        if not username:
            return make_response(jsonify({'error': 'User details not found in token'}), 400)
        user = db_session.query(Employee).filter_by(email=username).first()
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)
        assignee_id = user.id
        print(assignee_id)
    print(assignee_id)
    tickets = db_session.execute(select(Ticket).where(Ticket.Assignee_ID == assignee_id))
    ticket_list = [ticket[0].serialize() for ticket in tickets.all()]
    if not ticket_list:
        return make_response(jsonify({'message': 'No tickets found for the given Assignee_ID'}), 404)
    return make_response(jsonify(ticket_list), 200)

def parse_attachment(file_data, file_name, folder_this):
    """ Save attachment to bucket/chat_id folder and return base64 encoded content. """
    chat_folder = os.path.join(folder_this)
    os.makedirs(chat_folder, exist_ok=True)
    file_path = os.path.join(folder_this, file_name)

    # Write the file to disk
    with open(file_path, "wb") as f:
        f.write(file_data)

    # Convert file to base64
    with open(file_path, "rb") as f:
        file_ext = file_path.split('.')[-1]
        mime_type = guess_extension(file_ext) or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
    return file_name, mime_type,file_path

@ticket.route('/create', methods=['POST'])
def create_ticket():
    comments = []
    attachments = []
    ticket_id = request.json.get('ticket_id')
    print("@@@@@ INcomming Data")
    print(request.json)
    ticket = None
    if ticket_id:
        ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
        if not ticket:
            return error_response('Ticket not found', 404)

    if 'comments' in request.json:
        comments = handle_comments(request.json['comments'], request.json.get('user'))

    if 'logged_hrs' in request.json:
        handle_worklogs(request.json['logged_hrs'], request.json.get('user'))

    # Prepare new ticket data
    new_ticket_data = prepare_new_ticket_data(request.json, comments)

    # Create new ticket
    new_ticket = Ticket(**new_ticket_data)
    try:
        validation_error = new_ticket.validate()
        if validation_error:
            return error_response(validation_error, 400)

        db_session.add(new_ticket)
        db_session.commit()
        ticket_id ="SVC-"+str(new_ticket.Ticket_Id)
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return error_response(str(e), 500)

    folder_this = os.path.join(ticket_folder, ticket_id)
    os.makedirs(folder_this, exist_ok=True)
    attachments = handle_attachments(request.json.get('attachments', []), folder_this)

    chat_file,chat_history = prepare_chat_history(request.json, ticket_id, [x.serialize() for x in attachments])

    try:
        if attachments:
            print(attachments[0].serialize())
            ticket = db_session.query(Ticket).filter_by(Ticket_Id=new_ticket.Ticket_Id).first()
            print(ticket)
            ticket.attachments.extend(attachments)
            db_session.commit()  # Commit attachments
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error updating ticket with attachments: {e}")
        return error_response('Failed to update ticket with attachments', 500)
    print("@@@@chatfile mine")
    print(chat_history)
    print("@@@@chatfile mine")

    return json.dumps(chat_history, indent=4)
    return make_response(jsonify({chat_file}), 201)

def error_response(message, status_code):
    return make_response(jsonify({'error': message}), status_code)

def handle_comments(comments_data, user_email):
    comments = []
    comment_user = Customer().getIDfromUsername(user_email)
    for comment in comments_data:
        if 'comment_id' in comment:
            existing_comment = db_session.query(Comment).filter_by(Comment_id=comment['comment_id']).first()
            if existing_comment:
                existing_comment.Comment = comment['comment']
                comments.append(existing_comment)
            else:
                new_comment = Comment(Comment_user=comment_user, Comment=comment['comment'])
                comments.append(new_comment)
        else:
            new_comment = Comment(Comment_user=comment_user, Comment=comment['comment'])
            comments.append(new_comment)
    return comments

def handle_worklogs(worklogs_data, user_email):
    worklog_user = Employee().getIDfromUsername(user_email)
    for worklog in worklogs_data:
        if 'id' in worklog:
            existing_worklog = db_session.query(Worklog).filter_by(Worklog_Id=worklog['id']).first()
            if existing_worklog:
                existing_worklog.Worklog = worklog['description']
                existing_worklog.Worklog_Hours = worklog.get('hours', 0)
            else:
                new_worklog = Worklog(
                    Worklog_User=worklog_user,
                    Worklog=worklog['description'],
                    Worklog_Hours=worklog.get('hours', 0)
                )
                db_session.add(new_worklog)
        else:
            new_worklog = Worklog(
                Worklog_User=worklog_user,
                Worklog=worklog['description'],
                Worklog_Hours=worklog.get('hours', 0)
            )
            db_session.add(new_worklog)
    db_session.commit()

def handle_attachments(attachments_data, folder_this):
    attachments = []
    existing_files = set()
    
    for attachment in attachments_data:
        if 'data' in attachment:
            b_file_data = base64.b64decode(attachment['data'])
            filename, mime, file_path = parse_attachment(b_file_data, secure_filename(attachment['name']), folder_this)
        else:
            filename = attachment['name']
            mime = attachment['type']
            file_path = attachment['url']
        
        if file_path in existing_files:
            continue  # Skip duplicate attachments
        
        existing_files.add(file_path)
        
        if 'id' in attachment:
            existing_attachment = db_session.query(Attachment).filter_by(Attachment_Id=attachment['id']).first()
            if existing_attachment:
                existing_attachment.name = filename
                existing_attachment.url = file_path
                existing_attachment.size = attachment['size']
                existing_attachment.type = mime
                attachments.append(existing_attachment)
            else:
                new_attachment = Attachment(filename, file_path, attachment['size'], mime)
                attachments.append(new_attachment)
        else:
            new_attachment = Attachment(filename, file_path, attachment['size'], mime)
            attachments.append(new_attachment)
        
        attachment['url'] = file_path
        if 'data' in attachment:
            attachment.pop('data')
    
    return attachments

def prepare_chat_history(request_data, ticket_id, attachments):
    chat_file = os.path.join(ticket_folder, ticket_id, "data.json")
    chat_history = {
        "chat_id": request_data.get('chat_id'),
        "ticket_id": ticket_id,
        "user": request_data.get('user'),
        "history": {},
        "medium": "portal",
        "comments": [],
        "created": datetime.datetime.now().isoformat(),
        "updated": datetime.datetime.now().isoformat(),
        "logged_hrs": []
    }
    with open(chat_file, "w") as f:
        json.dump(chat_history, f)
        chat_attachment = Attachment("data.json", chat_file, os.path.getsize(chat_file), "application/json")
        attachments.append(chat_attachment.serialize())
        chat_history['attachments']=attachments
    return chat_file,chat_history

def prepare_new_ticket_data(request_data, comments):
    return {
        "Chat_Id": request_data.get("chat_id"),
        "Subject": request_data.get("subject"),
        "Summary": request_data.get("summary"),
        "Analysis": request_data.get("analysis"),
        "Description": request_data.get("text"),
        "Status": request_data.get("status"),
        "Priority": request_data.get("priority", "").lower(),
        "Issue_Type": request_data.get("issue_type"),
        "Channel": request_data.get("medium"),
        "Customer_ID": Customer().getIDfromUsername(request_data.get("user")),
        "Product_Type": request_data.get("product_type"),
        "Assignee_ID": Employee().getIDfromUsername(request_data.get('assingee')),
        "LastModified": datetime.datetime.now().isoformat(),
        "Estimation": request_data.get("estimation"),
        "Story_Points": request_data.get("story_points"),
        "comments": comments,
    }

@ticket.route('/logwork', methods=['POST'])
@jwt_required
def log_work(payload):
    Worklog_User = Employee().getIDfromUsername(payload['upn'])
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)

    body = request.json
    ticket_id = body.get("ticket_id")
    worklog = body.get("worklog")
    worklog_hours = body.get("worklog_hours")
    worklog_date = body.get("worklog_date")
    ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
    if not ticket:
        return make_response(jsonify({'error': 'Ticket not found'}), 404)
    print(ticket)
    db_session.add(Worklog(Ticket_Id=ticket_id, Worklog_User=Worklog_User, Worklog=worklog, Worklog_Hours=worklog_hours, Worklog_Date=worklog_date))
    try:
        db_session.commit()
        return make_response(jsonify({'message': 'Worklog added successfully'}), 201)
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return make_response(jsonify({'error': str(e)}), 500)

@ticket.route('/modify', methods=['POST'])
def modify_fields(*args, **kwargs):
    print("\n\n\n\@@@  modify value")
    print(request.json)
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)
    
    body = request.json
    ticket_id = body.get("ticket_id")  # Adjusted to match the new key
    ticket_id = str(ticket_id).split('-')[-1]
    print(ticket_id)
    if not ticket_id:
        return make_response(jsonify({'error': 'Ticket ID is required'}), 400)
    ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
    if not ticket:
        return make_response(jsonify({'error': 'Ticket not found'}), 404)
    
    try:
        if "subject" in body:
            ticket.Subject = body["subject"]
        if "summary" in body:
            ticket.Summary = body["summary"]
        if "analysis" in body:
            ticket.Analysis = body["analysis"]
        if "type" in body:
            ticket.Type = body["type"]
        if "text" in body:
            ticket.Description = body["text"]
        if "status" in body:
            ticket.Status = body["status"]
        if "priority" in body:
            ticket.Priority = body["priority"]
        if "issue_type" in body:
            ticket.Issue_Type = body["issue_type"]
        if "channel" in body:
            ticket.Channel = body["channel"]
        if "user" in body:
            ticket.Customer_ID = Customer().getIDfromUsername(body["user"])
        if "product_type" in body:
            ticket.Product_Type = body["product_type"]
        if "medium" in body:
            ticket.Medium = body["medium"]
        if "team" in body:
            ticket.Team = body["team"]
        if "assignee" in body:
            ticket.Assignee_ID = Employee().getIDfromUsername(body["assignee"])
        if "resolution" in body:
            ticket.Resolution = body["resolution"]
        if "issue_date" in body:
            ticket.Issue_Date = body["issue_date"]
        if "estimation" in body:
            ticket.Estimation = body["estimation"]
        if "reopens" in body:
            ticket.Reopens = body["reopens"]
        if "story_points" in body:
            ticket.Story_Points = body["story_points"]
        if "score" in body:
            ticket.Score = body["score"]

        ticket.LastModified = datetime.datetime.now().isoformat()
        print("workey")
        validation_error = ticket.validate()
        if validation_error:
            return make_response(jsonify({'error': validation_error}), 400)

        db_session.commit()
        return make_response(jsonify({'message': 'Ticket updated successfully'}), 200)

    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return make_response(jsonify({'error': str(e)}), 500)

@ticket.route('/get', methods=['GET'])
@ticket.route('/get/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id=None):
    ticket = []
    # time.sleep(random.randint(2,4))
    if not ticket_id:
        ticket_id = request.args.get('id')

    if ticket_id:
        if not ticket_id.isnumeric():
            ticket_id = ticket_id.split('-')[-1]
        db_session.expire_all()  # Ensure fresh data is fetched
        ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
        if ticket:
            ticket = ticket.serialize()
            ticket['ticket_id']=f"SVC-{ticket['ticket_id']}"
    
    if not ticket_id:
        #assignee_id = Employee().getIDfromUsername("test@gmail.com")  # change later
        assignee_id=1
        if assignee_id:
            print("@@@@ id")
            print(assignee_id)
            tickets = db_session.execute(select(Ticket).where(Ticket.Assignee_ID == assignee_id)).scalars().all()
            ticket = [t.serialize() for t in tickets]
            for x in ticket:
                x['ticket_id'] = f"SVC-{x['ticket_id']}"
            # print("@@@ id")
            # print(ticket)
    
    if not ticket:
        return jsonify({'error': 'Ticket not found'})
    # print("@@@ Final res")
    # print(ticket)

    return jsonify(ticket)

@ticket.route('/attachment/add', methods=['POST'])
def attachment():
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)
    body = request.json
    ticket_id = body.get('ticket_id')
    if not ticket_id:
        return make_response(jsonify({'error': 'Ticket ID is required'}), 400)
    ticket_no = str(ticket_id).split('-')[-1]
    attachments = body.get('attachments')
    for attachment in attachments:
        if attachment:
            b_file_data = base64.b64decode(attachment['data'])
            filePaththis = os.path.join(ticket_folder, ticket_id)
            filename, mime, file_path = parse_attachment(b_file_data, secure_filename(attachment['name']), filePaththis)
            file=Attachment(filename, file_path, attachment['size'], mime,ticket_no)
            try:
                db_session.add(file)
                db_session.commit()
                return make_response(jsonify({'message': 'Attachment added successfully'}), 201)
            except Exception as e:
                db_session.rollback()
                logger.error(e)
                return make_response(jsonify({'error': str(e)}), 500)
    return make_response(jsonify({'error': 'Attachment data not found'}), 400)

@ticket.route('/attachment/delete', methods=['DELETE'])
def delete_attachment():
    attachment_id = request.args.get('id')
    if not attachment_id:
        return make_response(jsonify({'error': 'Attachment ID is required'}), 400)
    attachment = db_session.query(Attachment).filter_by(Id=attachment_id).first()
    if not attachment:
        return make_response(jsonify({'error': 'Attachment not found'}), 404)
    try:
        db_session.delete(attachment)
        db_session.commit()
        return make_response(jsonify({'message': 'Attachment deleted successfully'}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return make_response(jsonify({'error': str(e)}), 500)

class BotAdmin:
        def create_ticket(self,ticket):
            description = ticket.get("description")
            analysis = ticket.get("analysis")
            
            if analysis and description=="":
                description = analysis
                analysis = ""

            new_ticket = Ticket(
                Chat_Id=ticket.get("chat_id"),
                Subject=ticket.get("subject"),
                Summary=ticket.get("summary"),
                Analysis=analysis,
                Description=description,
                Customer_ID=Customer().getIDfromUsername(ticket.get("user")),
                Medium=ticket.get("medium"),
                Issue_Type=ticket.get("issue_type"),
                Channel=ticket.get("connection"),
                Assignee_ID=self.setAssignee(),
                Product_Type=ticket.get("product_type"),  
                Priority=ticket.get("priority"),
                Story_Points=ticket.get("story_points"),
                Status="Open"
            )
            try:
                validation_error = new_ticket.validate()
                if validation_error:
                    return {'error': validation_error}
                db_session.add(new_ticket)
                db_session.commit()
                return {'id': new_ticket.Ticket_Id}
            except Exception as e:
                db_session.rollback()
                logger.error(e)
                return {'error': str(e)}
        def setAssignee(self) -> int:
            # //logic to assign ticket to employee based on scoring mechanism
            return 1