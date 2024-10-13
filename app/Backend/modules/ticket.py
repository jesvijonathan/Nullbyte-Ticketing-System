from flask import Blueprint
from flask import request, make_response, jsonify, render_template
from werkzeug.utils import secure_filename
from config import *
from .db.db_models import Ticket, Employee,Customer
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
def create_ticket(*args, **kwargs):
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)

    body = request.json
    new_ticket = Ticket(
        Subject=body.get("Subject"),
        Summary=body.get("Summary"),
        Analysis=body.get("Analysis"),
        Type=body.get("Type"),
        Description=body.get("Description"),
        Status=body.get("Status"),
        Priority=body.get("Priority"),
        Issue_Type=body.get("Issue_Type"),
        Channel=body.get("Channel"),
        Customer_ID=body.get("Customer_ID"),
        Product_ID=body.get("Product_ID"),
        Medium=body.get("Medium"),
        Team=body.get("Team"),
        Assignee_ID=body.get("Assignee_ID"),
        Resolution=body.get("Resolution"),
        Issue_Date=body.get("Issue_Date"),
        First_Response_Time=body.get("First_Response_Time"),
        Time_to_Resolution=body.get("Time_to_Resolution"),
        Reopens=body.get("Reopens"),
        Story_Points=body.get("Story_Points"),
        Score=body.get("Score")
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
    ticket_id='SVC-'+str(ticket_id)
    if 'file' not in request.files:
        return make_response(jsonify({'error': 'No file part'}), 400)
    
    file = request.files['file']
    if file.filename == '':
        return make_response(jsonify({'error': 'No selected file'}), 400)
    
    if file:
        try:
            filename = secure_filename(file.filename)
            ticket_folder = "./bucket/tickets"
            os.makedirs(ticket_folder, exist_ok=True)
            this_ticket_folder = os.path.join(ticket_folder, str(ticket_id))
            os.makedirs(this_ticket_folder, exist_ok=True)
            file.save(os.path.join(this_ticket_folder, filename))
            print(f"File saved to {this_ticket_folder}")
            return make_response(jsonify({'message': 'File uploaded successfully'}), 200)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
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
                # Attachments=ticket.get("attachments"),
                Customer_ID=Customer().getIDfromEmail(ticket.get("user")),
                Medium=ticket.get("medium"),
                Issue_Type=ticket.get("issue_type"),
                Channel=ticket.get("connection"),
                #Assignee_ID=1, //needed to be implemented based on scoring mechanism
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