from flask import Blueprint
from flask import request, make_response, jsonify, render_template
from werkzeug.utils import secure_filename
from config import *
from .db.db_models import Ticket, Employee,Customer,Attachment,Comment,Worklog
from .auth.auth import jwt_required
from .db.database import db_session
from .log import *
from sqlalchemy import select

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

@ticket.route('/create', methods=['POST'])
@jwt_required
def create_ticket(payload):
    comments = []
    attachments= []
    ticket_id = None
    ticket = None
    # if id is there we are just updating the ticket with comments, attachments and worklog
    if 'id' in request.form:
        ticket_id = request.form.get('id')
        print(ticket_id)   
        try:
            ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
            print("ticket",end=": ")
            if not ticket:
                return make_response(jsonify({'error': 'Ticket not found'}), 404)
        except Exception as e:
            logger.error(f"Error fetching ticket: {e}")
            return make_response(jsonify({'error': 'Failed to fetch ticket? does ticket exist'}), 500)
    
    if 'comments' in request.form:
        for comment in request.form.getlist('comments'):
            Comment_user = Customer().getIDfromEmail(payload['upn'])
            Comment_text = comment
            new_comment = Comment(Comment_user=Comment_user, Comment=Comment_text)
            comments.append(new_comment)
    
    if 'worklog' in request.form:
        for worklog in request.form.getlist('worklog'):
            Worklog_user = Customer().getIDfromEmail(payload['upn'])
            Worklog_text = worklog
            Worklog_hours = request.form.get('worklog_hours', type=int)
            new_worklog = Worklog(
                Worklog_User=Worklog_user,
                Worklog=Worklog_text,
                Worklog_Hours=Worklog_hours
            )
            db_session.add(new_worklog)
            db_session.commit()

    files=request.files.getlist('files')
    if not all(file.filename == '' for file in files):
        try:
            ticket_folder = "./bucket/tickets"
            os.makedirs(ticket_folder, exist_ok=True)
            this_ticket_folder = os.path.join(ticket_folder, str(ticket_id))
            os.makedirs(this_ticket_folder, exist_ok=True)
            
            for file in files:
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    writefile = os.path.join(this_ticket_folder, filename)
                    file.save(writefile)
                    print(f"File saved to {this_ticket_folder}")
                    new_attachment = Attachment(url=writefile)
                    attachments.append(new_attachment)
        except Exception as e:
            logger.error(f"Error saving files: {e}")
            return make_response(jsonify({'error': 'File upload failed'}), 500)
    print(ticket_id)   
    if ticket_id and len(comments) == 0 and len(attachments) == 0:
        return make_response(jsonify({'error': 'Comments or attachments are required to update ticket if only id is provided'}), 400)
    elif ticket_id:
        try:
            print(ticket)
            print(comments)
            if ticket is not None and len(comments) > 0:
                print(comments)
                ticket.comments.extend(comments)
                db_session.commit()
                print("comments added")
            if ticket is not None and len(attachments) > 0:
                print(attachments)
                ticket.attachments.extend(attachments)
                db_session.commit()
                print("attachments added")
            return make_response(jsonify({'message': 'Data added successfully'}), 200)
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error updating ticket: {e}")
            return make_response(jsonify({'error': 'Failed to update ticket'}), 500)
    elif not ticket_id and request.form:
        new_ticket = Ticket(
            Subject=request.form.get("subject"),
            Summary=request.form.get("summary"),
            Analysis=request.form.get("analysis"),
            Type=request.form.get("type"),
            Description=request.form.get("description"),
            Status=request.form.get("status"),
            Priority=request.form.get("priority"),
            Issue_Type=request.form.get("issue_type"),
            Channel=request.form.get("channel"),
            Customer_ID=Customer().getIDfromEmail(payload['upn']),
            Product_ID=request.form.get("product_type"),
            Medium=request.form.get("medium"),
            Team=request.form.get("team"),
            Assignee_ID=request.form.get("assignee"),
            Resolution=request.form.get("Resolution"),
            Issue_Date=request.form.get("created"),
            First_Response_Time=request.form.get("First_Response_Time"),
            Time_to_Resolution=request.form.get("estimation"),
            Reopens=request.form.get("reopens"),
            Story_Points=request.form.get("story_points"),
            comments=comments,
            attachments=attachments
        )
        try:
            validation_error = new_ticket.validate()
            if validation_error:
                return make_response(jsonify({'error': validation_error}), 400)
            db_session.add(new_ticket)
            db_session.commit()
            return make_response(jsonify({'id': new_ticket.Ticket_Id}), 201)
        except Exception as e:
            db_session.rollback()
            logger.error(e)
            return make_response(jsonify({'error': str(e)}), 500)
    else:
        return make_response(jsonify({'error': 'Ticket ID is required to add comments. If creating a new ticket, do not include a ticket ID. To create new ticket pass form data without id'}), 400)

@ticket.route('/logwork', methods=['POST'])
@jwt_required
def log_work(payload):
    Worklog_User = Employee().getIDfromEmail(payload['upn'])
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

@ticket.route('/modify', methods=['PUT'])
@jwt_required
def modify_fields(*args, **kwargs):
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)
    body = request.json
    ticket_id = body.get("Id")
    if not ticket_id:
        return make_response(jsonify({'error': 'Ticket ID is required'}), 400)
    ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
    if not ticket:
        return make_response(jsonify({'error': 'Ticket not found'}), 404)
    try:
        if "Subject" in body:
            ticket.Subject = body["Subject"]
        if "Summary" in body:
            ticket.Summary = body["Summary"]
        if "Analysis" in body:
            ticket.Analysis = body["Analysis"]
        if "Attachments" in body:
            ticket.Attachments = body["Attachments"]
        if "Type" in body:
            ticket.Type = body["Type"]
        if "Description" in body:
            ticket.Description = body["Description"]
        if "Status" in body:
            ticket.Status = body["Status"]
        if "Priority" in body:
            ticket.Priority = body["Priority"]
        if "Issue_Type" in body:
            ticket.Issue_Type = body["Issue_Type"]
        if "Channel" in body:
            ticket.Channel = body["Channel"]
        if "Customer_ID" in body:
            ticket.Customer_ID = body["Customer_ID"]
        if "Product_ID" in body:
            ticket.Product_ID = body["Product_ID"]
        if "Medium" in body:
            ticket.Medium = body["Medium"]
        if "Team" in body:
            ticket.Team = body["Team"]
        if "Assignee_ID" in body:
            ticket.Assignee_ID = body["Assignee_ID"]
        if "Resolution" in body:
            ticket.Resolution = body["Resolution"]
        if "Issue_Date" in body:
            ticket.Issue_Date = body["Issue_Date"]
        if "First_Response_Time" in body:
            ticket.First_Response_Time = body["First_Response_Time"]
        if "Time_to_Resolution" in body:
            ticket.Time_to_Resolution = body["Time_to_Resolution"]
        if "Reopens" in body:
            ticket.Reopens = body["Reopens"]
        if "Story_Points" in body:
            ticket.Story_Points = body["Story_Points"]
        if "Score" in body:
            ticket.Score = body["Score"]
        
        validation_error = ticket.validate()
        if validation_error:
            return make_response(jsonify({'error': validation_error}), 400)
        
        db_session.commit()
        return make_response(jsonify({'message': 'Ticket updated successfully'}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return make_response(jsonify({'error': str(e)}), 500)
    
@ticket.route('/', methods=['GET'])
@jwt_required
def get_ticket(*args, **kwargs):
    ticket_id = request.args.get('id')
    if ticket_id:
        if ticket_id.isnumeric():
            ticket_id = int(ticket_id)
        else:
            ticket_id = ticket_id.split('-')[-1]
    if not ticket_id:
        return make_response(jsonify({'error': 'Ticket ID is required'}), 400)
    db_session.expire_all()  # Expire all instances to ensure fresh data is fetched
    ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
    if not ticket:
        return make_response(jsonify({'error': 'Ticket not found'}), 404)
    return make_response(jsonify(ticket.serialize()), 200)

@ticket.route('/attachments/add', methods=['POST'])
@jwt_required
def addattachment():
    ticket_id = request.form.get('ticket_id')
    if not ticket_id:
        return make_response(jsonify({'error': 'Ticket ID is required'}), 400)
    
    ticket = db_session.query(Ticket).filter_by(Ticket_Id=ticket_id).first()
    if not ticket:
        return make_response(jsonify({'error': 'Ticket not found'}), 404)
    full_ticket_id = 'SVC-' + str(ticket_id)
    
    if 'files' not in request.files:
        return make_response(jsonify({'error': 'No files part'}), 400)
    
    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        return make_response(jsonify({'error': 'No selected files'}), 400)
    
    try:
        ticket_folder = "./bucket/tickets"
        os.makedirs(ticket_folder, exist_ok=True)
        this_ticket_folder = os.path.join(ticket_folder, str(full_ticket_id))
        os.makedirs(this_ticket_folder, exist_ok=True)
        
        for file in files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                writefile = os.path.join(this_ticket_folder, filename)
                file.save(writefile)
                print(f"File saved to {this_ticket_folder}")
                Attachment().addAttachment(ticket_id, writefile)
        
        return make_response(jsonify({'message': 'Files uploaded successfully'}), 200)
    except Exception as e:
        logger.error(f"Error saving files: {e}")
        return make_response(jsonify({'error': 'File upload failed'}), 500)
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
                Customer_ID=Customer().getIDfromEmail(ticket.get("user")),
                Medium=ticket.get("medium"),
                Issue_Type=ticket.get("issue_type"),
                Channel=ticket.get("connection"),
                Assignee_ID=self.setAssignee(),#, //needed to be implemented based on scoring mechanism
                Product_ID=ticket.get("product_id"),  
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