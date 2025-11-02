from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Event, Order, db
from .forms import TicketForm

tickbp = Blueprint('ticket', __name__, url_prefix='/tickets')

@tickbp.route('/buy', methods=['GET', 'POST'])
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

        # Check how many tickets current user already bought for this event
        past_orders = Order.query.filter_by(user_id=current_user.id, event_id=event_id).all()
        user_tickets = sum([order.quantity for order in past_orders])

        # Max ticket amount for an event per person
        max_tickets = 10  
        # Check ticket purchase amount vs. available tickets left
        max_allowed = min(max_tickets - user_tickets, event.tickets_available)
        
        if max_allowed <= 0:
            flash("You cannot buy more tickets for this event", "error")
            return redirect(url_for('ticket.buy_ticket'))
        
        if requested_tickets > max_allowed: 
            flash(f"You can only purchase {max_allowed} more tickets", "error")
            return redirect(url_for('ticket.buy_ticket'))

        # Commit order with event's price
        new_order = Order(
            user_id=current_user.id, 
            event_id=event_id, 
            quantity=requested_tickets,
            price_per_ticket=event.price_per_ticket  # Use event's price
        )
        event.tickets_available -= requested_tickets
        
        db.session.add(new_order)
        db.session.commit()

        flash("Tickets purchased successfully!", "success")
        return redirect(url_for('ticket.history'))

    return render_template('buy_ticket.html', form=form)

@tickbp.route('/buy/<int:event_id>', methods=['GET', 'POST'])
@login_required
def buy_ticket_direct(event_id):
    # Get the specific event
    event = Event.query.get_or_404(event_id)
    
    # Create a simplified form for direct booking
    if request.method == 'POST':
        requested_tickets = int(request.form.get('quantity', 1))
        
        # Validate ticket availability
        if requested_tickets > event.tickets_available:
            flash(f"Only {event.tickets_available} tickets available", "error")
            return redirect(url_for('events.event_detail', event_id=event_id))
        
        if requested_tickets <= 0:
            flash("Please select a valid number of tickets", "error")
            return redirect(url_for('events.event_detail', event_id=event_id))
        
        # Check if user already bought tickets for this event
        past_orders = Order.query.filter_by(user_id=current_user.id, event_id=event_id).all()
        user_tickets = sum([order.quantity for order in past_orders])
        max_tickets = 10
        
        if user_tickets + requested_tickets > max_tickets:
            flash(f"You can only purchase {max_tickets - user_tickets} more tickets for this event", "error")
            return redirect(url_for('events.event_detail', event_id=event_id))
        
        # Create the order with event's price
        new_order = Order(
            user_id=current_user.id, 
            event_id=event_id, 
            quantity=requested_tickets,
            price_per_ticket=event.price_per_ticket  # Use event's price
        )
        
        # Update event availability
        event.tickets_available -= requested_tickets
        
        db.session.add(new_order)
        db.session.commit()
        
        flash(f"Successfully booked {requested_tickets} ticket(s) for {event.title}!", "success")
        return redirect(url_for('ticket.history'))
    
    # If GET request, redirect to event detail page (shouldn't happen with the form above)
    return redirect(url_for('events.event_detail', event_id=event_id))

@tickbp.route('/history')
@login_required 
def history():
   orders = Order.query.filter_by(user_id=current_user.id).all()
   return render_template('booking-history.html', orders=orders)