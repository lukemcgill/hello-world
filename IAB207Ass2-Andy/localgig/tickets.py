from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import TicketForm, CommentForm
from . import db
from .models import User, Event, Comment, Order
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user, login_user

tickbp = Blueprint('ticket', __name__, url_prefix='/tickets')

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Event, Order, db
from .forms import TicketForm


tickbp = Blueprint('ticket', __name__, url_prefix='/tickets')


@tickbp.route('/buy', methods=['GET', 'POST'])
#user must be logged in to buy tickets
@login_required
def buy_ticket():
    form = TicketForm()
    
    if form.validate_on_submit():
        event_id = form.event.data
        requested_tickets = form.quantity.data
        
        event = Event.query.get(event_id)
        if not event:
            flash("Selected event does not exist.", "danger")
            return redirect(url_for('ticket.buy_ticket'))

        #search how many tickets that current user already bought for an event
        past_orders = Order.query.filter_by(user_id=current_user.id, event_id=event_id).all()
        user_tickets = sum([order.quantity for order in past_orders])

        #max ticket amount for an event per person
        max_tickets = 10  
        #check ticket purchase amount vs. available tickets left
        max_allowed = min(max_tickets - user_tickets, event.tickets_available)
        
        if max_allowed <= 0:
            flash("You cannot buy more tickets for this event")
            return redirect(url_for('ticket.buy_ticket'))
        
        if requested_tickets > max_allowed: 
            flash(f"You can only purchase {max_allowed} more tickets")
            return redirect(url_for('ticket.buy_ticket'))

        #commit order
        new_order = Order(user_id=current_user.id, event_id=event_id, quantity=requested_tickets)
        event.tickets_available -= requested_tickets
        
        db.session.add(new_order)
        db.session.commit()

        flash("Tickets purchased successfully!", "success")
        return redirect(url_for('ticket.history'))

    return render_template('buy_ticket.html', form=form)


@tickbp.route('/history')
#user must be logged in to view their history
@login_required 
def history():
   orders = Order.query.filter_by(user_id=current_user.id).all()
   return render_template('booking-history.html', orders=orders)
