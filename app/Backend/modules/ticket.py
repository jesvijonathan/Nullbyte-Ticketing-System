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

# @jwt_required
@ticket.route('/list', methods=['GET'])
def get_all_tickets(*args, **kwargs):
    tickets = db_session.query(Ticket).order_by(Ticket.LastModified.desc()).limit(20).all()
    ticket_list = [ticket.serialize() for ticket in tickets]
    if not ticket_list:
        return make_response(jsonify({'message': 'No tickets found'}), 404)
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

    
def create_ticket(request):
    comments = []
    attachments = []
    # ticket_id = request.json.get('ticket_id')
    # if(ticket_id):
    #     ticket_no = int(str(ticket_id).split('-')[-1])
    # else :
    ticket_no = None
    print("@@@@@ INcomming Data")
    print(request.json)
    ticket = None
    ticket_id = None
    if ticket_id:
        ticket_no = str(ticket_id).split('-')[-1]
        ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_no).first()
        if not ticket:
            return error_response('Ticket not found', 404)

    # if 'comments' in request.json:
    #     comments = handle_comments(request.json['comments'], request.json.get('user'),ticket_no)

    # if 'logged_hrs' in request.json:
    #     handle_worklogs(request.json['logged_hrs'], request.json.get('user'))
    
    if 'attachments' in request.json:
        attachments = handle_attachments(request.json['attachments'], ticket_no)
        print("@@@@attachment")
        print(attachments)

    if ticket_id:
        # fetch new ticket data and serialize send
        ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_no).first()
        return jsonify(ticket.serialize())
    new_ticket_data = prepare_new_ticket_data(request.json, comments)

    new_ticket = Ticket(**new_ticket_data)
    try:
        validation_error = new_ticket.validate()
        if validation_error:
            return error_response(validation_error, 400)

        db_session.add(new_ticket)
        db_session.commit()
        ticket_id =str(new_ticket.Ticket_Id)
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return error_response(str(e), 500)

    folder_this = os.path.join(ticket_folder, ticket_id)
    os.makedirs(folder_this, exist_ok=True)

    print("@@@@chatfile")
    print(attachments)
    chat_file,chat_history = prepare_chat_history(request.json, ticket_id, [x.serialize() for x in attachments],[x.serialize() for x in comments])

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

def error_response(message, status_code):
    return make_response(jsonify({'error': message}), status_code)

def handle_comments(comments_data, user_email, ticket_no):
    comments = []
    comment_user = Customer().getIDfromUsername(user_email)
    print("came here")
    print(ticket_no)
    if ticket_no is not None:
        try:
            Comment().delete_comments(ticket_no)
        except Exception as e:
            logger.error(f"Error deleting comments: {e}")
            return error_response('Failed to delete existing comments', 500)
    for comment in comments_data:
        new_comment = Comment(Comment_user=comment_user, Comment=comment['text'])
        if ticket_no is not None:
            new_comment.Ticket_id = ticket_no
        comments.append(new_comment)
    if ticket_no is not None:
        try:
            db_session.add_all(comments)
            db_session.commit()
            comments = db_session.query(Comment).filter_by(Ticket_id=ticket_no).all()
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error adding comments: {e}")
            return error_response('Failed to add comments', 500)
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

def handle_attachments(attachments_data, ticket_no=None):
    attachments = []
    print(type(ticket_no))
    if ticket_no is not None:
        print("@@@@attachment ticket no")
        should_delete = bool(ticket_no)
        print(ticket_no)
        print(should_delete)
        try:
            db_session.query(Attachment).filter_by(Ticket_Id=ticket_no).delete()
        except Exception as e:
            logger.error(f"Error deleting attachments: {e}")
    for attachment in attachments_data:
        if attachment:
            b_file_data = base64.b64decode(attachment['data'])
            filePaththis = os.path.join(ticket_folder, ticket_no if ticket_no else "")
            filename, mime, file_path = parse_attachment(b_file_data, secure_filename(attachment['name']), filePaththis)
            file = Attachment(Name=filename, Url=file_path, Size=attachment['size'], Type=mime)
            if ticket_no is not None:
                file.Ticket_Id = ticket_no
            attachments.append(file)

    if ticket_no is not None:
        try:
            db_session.add_all(attachments)
            db_session.commit()
            attachments = db_session.query(Attachment).filter_by(Ticket_Id=ticket_no).all()
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error adding attachments: {e}")
            # return error_response('Failed to add attachments', 500)
    print("@@@@attachment")
    print(attachments)
    return attachments

def prepare_chat_history(request_data, ticket_id, attachments=[],comments=[]):
    chat_file = os.path.join(ticket_folder, ticket_id, "data.json")
    chat_history = {
        "chat_id": request_data.get('chat_id'),
        "ticket_id": ticket_id,
        "user": request_data.get('user'),
        "history": {},
        "medium": "portal",
        "comments": comments,
        "created": datetime.datetime.now().isoformat(),
        "updated": datetime.datetime.now().isoformat(),
        "logged_hrs": [],
        "attachments": attachments
    }
    # with open(chat_file, "w") as f:
        # json.dump(chat_history, f)
        # chat_attachment = Attachment(Name="data.json", chat_file, os.path.getsize(chat_file), "application/json")
        # attachments.append(chat_attachment.serialize())
        # chat_history['attachments']=attachments
    return chat_file,chat_history

def delete_ticket(ticket_id):
    ticket_no = str(ticket_id).split('-')[-1]
    ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_no).first()
    if not ticket:
        return make_response(jsonify({'error': 'Ticket not found'+ticket_no}), 404)
    try:
        db_session.delete(ticket)
        db_session.commit()
        return make_response(jsonify({'message': 'Ticket deleted successfully'}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return make_response(jsonify({'error': str(e)}), 500)
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

# @ticket.route('/modify', methods=['POST'])
def modify_fields(request):
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
    ticket_no= str(ticket_id).split('-')[-1]
    print(ticket_no)
    ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_no).first()
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
        
        if 'comments' in request.json:
            comments = handle_comments(request.json['comments'], request.json.get('user'),ticket_no)

        if 'logged_hrs' in request.json:
            handle_worklogs(request.json['logged_hrs'], request.json.get('user'))
    
        if 'attachments' in request.json:
            attachments = handle_attachments(request.json['attachments'], ticket_no)
        print("@@@@attachment")
        print(attachments)


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

# @ticket.route('/get', methods=['GET'])
# @ticket.route('/get/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id=None):
    ticket = []
    # time.sleep(random.randint(2,4))
    if not ticket_id:
        ticket_id = request.args.get('ticket_id')
    print("@@@@ ticket_id")
    print(ticket_id)
    if ticket_id:
        if not ticket_id.isnumeric():
            ticket_id = ticket_id.split('-')[-1]
        db_session.expire_all()  # Ensure fresh data is fetched
        ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
        if ticket:
            ticket = ticket.serialize()
            ticket['ticket_id']=ticket['ticket_id']
    
    if not ticket_id:
        #assignee_id = Employee().getIDfromUsername("test@gmail.com")  # change later
        assignee_id=1
        if assignee_id:
            print("@@@@ id")
            print(assignee_id)
            tickets = db_session.execute(select(Ticket).where(Ticket.Assignee_ID == assignee_id).limit(10)).scalars().all()
            ticket = [t.serialize() for t in tickets]
            for x in ticket:
                x['ticket_id'] = f"{x['ticket_id']}"
            # print("@@@ id")
            # print(ticket)
    
    if not ticket:
        return jsonify({'error': 'Ticket not found'})
    # print("@@@ Final res")
    # print(ticket)
    print(ticket)
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
            print("@@@ Came here \n\n\n\n")
            print(ticket)
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
                Status="open"
            )
            try:
                validation_error = new_ticket.validate()
                if validation_error:
                    return {'error': validation_error}
                db_session.add(new_ticket)
                db_session.commit()
                print("@@@@ ticket created")
                return {'id': new_ticket.Ticket_Id}
            except Exception as e:
                db_session.rollback()
                logger.error(e)
                return {'error': str(e)}
        def setAssignee(self) -> int:
            # //logic to assign ticket to employee based on scoring mechanism
            return 1
        
        def create_ticket_dirmode(self, request):
                ticket_id = request.get('ticket_id')
                print("Ticket ID:", ticket_id)
                form_data = request
                print(json.dumps(form_data, indent=4))
                attachments = []  
                attachments_list = form_data.get('attachments', [])
                # ticket_id = form_data.get('ticket_id')
                print("Ticket ID:", ticket_id)
                folder_this = os.path.join(ticket_folder, ticket_id)
                print("Folder:", folder_this)
                if attachments_list:
                    attachment_count = 0
                    for attachment in attachments_list:
                        binary_file_data = attachment['data']
                        b_file_data = base64.b64decode(attachment['data'])
                        filename, mime = parse_attachment(b_file_data, secure_filename(attachment['name']), folder_this)
                        filename = filename
                        file_path = os.path.join(folder_this, filename)
                        attachments_list[attachment_count]['url'] = file_path
                        attachments_list[attachment_count].pop('data')
                        attachment_count += 1
                        # attachments.append(file_path)
                chat_file = os.path.join(folder_this, "data.json")
                os.makedirs(folder_this, exist_ok=True)
                chat_history={
                        "chat_id": form_data.get('chat_id'),
                        "ticket_id": ticket_id,
                        "user": form_data.get('user'),
                        "history": {},
                        "medium": "",
                        "comments": [],
                        "attachments": attachments_list,
                        "created": datetime.datetime.now().isoformat(),
                        "updated": datetime.datetime.now().isoformat(),
                        "logged_hrs": []
                    }
                chat_history = {**chat_history, **form_data}

                with open(chat_file, "w") as f:
                    json.dump(chat_history, f)
                if bucket_mode:
                    files_to_upload = [chat_file] + [attachment['url'] for attachment in attachments_list]
                    upload_individual_files(bucket_name, files_to_upload)

                    # Upload the chat file and attachments to the cloud
                    print("@@@@@@@@Chat histroy")
                    print(chat_history)
                return json.dumps(chat_history, indent=4) 
