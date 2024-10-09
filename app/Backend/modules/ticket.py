from flask import Blueprint
from flask import request, make_response,jsonify
from config import *
from .db.db_models import Ticket
from .auth.auth import jwt_required
from .db.database import db_session
from .log import *

ticket=Blueprint('ticket',__name__)

# @ticket.route('/list',methods=['GET'])
# @jwt_required
# def get_all_tickets():
#     tickets = db_session.query(Ticket).all()
#     return make_response(jsonify([ticket.serialize() for ticket in tickets]), 200)

@ticket.route('/create',methods=['POST'])
@jwt_required
def create_ticket():
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)

    body = request.json
    new_ticket = Ticket(
        Subject=body.get("Subject"),
        Type=body.get("Type"),
        Description=body.get("Description"),
        Status=body.get("Status"),
        Priority=body.get("Priority"),
        Channel=body.get("Channel"),
        Customer_ID=body.get("Customer_ID"),
        Product_ID=body.get("Product_ID"),
        Assignee_ID=body.get("Assignee_ID"),
        Resolution=body.get("Resolution"),
        Reopens=body.get("Reopens"),
    )
    try:
        new_ticket.validate()
        db_session.add(new_ticket)
        db_session.commit()
        return make_response(jsonify({'id': new_ticket.Id}), 201)
    except Exception as e:
        db_session.rollback()
        logger.error(e) 
        return make_response(jsonify({'error': str(e)}), 500)

@ticket.route('/modify', methods=['PUT'])
@jwt_required
def modify_fields():
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)
    body = request.json
    ticket_id = body.get("Id")
    if not ticket_id:
        return make_response(jsonify({'error': 'Ticket ID is required'}), 400)
    ticket = db_session.query(Ticket).filter_by(Id=ticket_id).first()
    if not ticket:
        return make_response(jsonify({'error': 'Ticket not found'}), 404)
    try:
        if "Subject" in body:
            ticket.Subject = body["Subject"]
        if "Type" in body:
            ticket.Type = body["Type"]
        if "Description" in body:
            ticket.Description = body["Description"]
        if "Status" in body:
            ticket.Status = body["Status"]
        if "Priority" in body:
            ticket.Priority = body["Priority"]
        if "Channel" in body:
            ticket.Channel = body["Channel"]
        if "Customer_ID" in body:
            ticket.Customer_ID = body["Customer_ID"]
        if "Product_ID" in body:
            ticket.Product_ID = body["Product_ID"]
        if "Assignee_ID" in body:
            ticket.Assignee_ID = body["Assignee_ID"]
        if "Resolution" in body:
            ticket.Resolution = body["Resolution"]
        if "First_Response_Time" in body:
            ticket.First_Response_Time = body["First_Response_Time"]
        if "Time_to_Resolution" in body:
            ticket.Time_to_Resolution = body["Time_to_Resolution"]
        if "Reopens" in body:
            ticket.Reopens = body["Reopens"]
        if "Score" in body:
            ticket.Score = body["Score"]
        ticket.validate()
        db_session.commit()
        return make_response(jsonify({'message': 'Ticket updated successfully'}), 200)
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        return make_response(jsonify({'error': str(e)}), 500)