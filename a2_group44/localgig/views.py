from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .models import db, Event, Comment, Order
from .forms import EventForm, CommentForm

main_bp = Blueprint("main", __name__)
events_bp = Blueprint("events", __name__, url_prefix="/events")

# --- Dynamic Homepage ---
@main_bp.route("/", methods=["GET"])
def index():
    genre_filter = request.args.get("genre")
    search_query = request.args.get("q", "").strip()

    events_query = Event.query.order_by(Event.event_date.asc())

    if genre_filter:
        events_query = events_query.filter_by(genre=genre_filter)

    if search_query:
        events_query = events_query.filter(Event.title.ilike(f"%{search_query}%"))

    events = events_query.all()
    genres = ["Rock", "Jazz", "Indie", "Electronic", "Hip Hop"]

    return render_template(
        "index.html",
        events=events,
        genres=genres,
        selected_genre=genre_filter
    )

# --- Event Creation ---
@events_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        
        if form.ends_at.data <= form.starts_at.data:
            flash("End time must be after start time.", "warning")
            return render_template("create-event.html", form=form)
        
        ev = Event(
            owner_id=current_user.id,
            title=form.title.data,
            artist_name=form.artist_name.data,
            genre=form.genre.data,
            capacity=form.capacity.data,
            venue_name=form.venue_name.data,
            location=form.location.data,
            event_date=form.event_date.data,
            starts_at=form.starts_at.data,
            ends_at=form.ends_at.data,
            image_url=form.image_url.data or None,
            description=form.description.data,
            tickets_total=form.capacity.data,
            tickets_available=form.capacity.data,
            price_per_ticket=form.price_per_ticket.data
        )
        
        db.session.add(ev)
        db.session.commit()
        
        flash("Event created.", "success")
        return redirect(url_for("events.event_detail", event_id=ev.event_id))
    
    return render_template("create-event.html", form=form)

# --- Event Editing ---
@events_bp.route("/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if user owns the event
    if current_user.id != event.owner_id:
        flash("You don't have permission to edit this event.", "warning")
        return redirect(url_for("events.event_detail", event_id=event_id))
    
    form = EventForm()
    
    # Pre-populate form with current event data
    if request.method == 'GET':
        form.title.data = event.title
        form.artist_name.data = event.artist_name
        form.genre.data = event.genre
        form.capacity.data = event.capacity
        form.venue_name.data = event.venue_name
        form.location.data = event.location
        form.event_date.data = event.event_date
        form.starts_at.data = event.starts_at
        form.ends_at.data = event.ends_at
        form.image_url.data = event.image_url
        form.description.data = event.description
        form.price_per_ticket.data = event.price_per_ticket
    
    if form.validate_on_submit():
        if form.ends_at.data <= form.starts_at.data:
            flash("End time must be after start time.", "warning")
            return render_template("edit-event.html", form=form, event=event)
        
        # Update event with new data (don't update status-related fields)
        event.title = form.title.data
        event.artist_name = form.artist_name.data
        event.genre = form.genre.data
        event.venue_name = form.venue_name.data
        event.location = form.location.data
        event.event_date = form.event_date.data
        event.starts_at = form.starts_at.data
        event.ends_at = form.ends_at.data
        event.image_url = form.image_url.data or None
        event.description = form.description.data
        event.price_per_ticket = form.price_per_ticket.data
        
        # Note: We don't update capacity/tickets_available to avoid breaking bookings
        # Note: We don't update cancelled status - that's handled by cancel_event
        
        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect(url_for("events.event_detail", event_id=event.event_id))
    
    return render_template("edit-event.html", form=form, event=event)

# --- Event Details ---
@events_bp.route("/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comments = event.comments.order_by(Comment.created_at.desc()).all()
    form = CommentForm()
    return render_template(
        "event-detail.html",
        event=event,
        comments=comments,
        comment_form=form,
        is_logged_in=current_user.is_authenticated
    )

# --- Cancel Event ---
@events_bp.route("/<int:event_id>/cancel", methods=["POST"])
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.id == event.owner_id:
        if not event.cancelled:
            event.cancelled = True
            db.session.commit()
            flash("Event cancelled.", "success")
        else:
            flash("Event already cancelled.", "info")
    else:
        flash("You don't have permission to cancel this event.", "warning")
    return redirect(url_for("events.event_detail", event_id=event.event_id))

# --- Post Comment ---
@events_bp.route("/<int:event_id>/comment", methods=["POST"])
@login_required
def post_comment(event_id):
    event = Event.query.get_or_404(event_id)
    form = CommentForm()
    if form.validate_on_submit():
        c = Comment(
            body=form.body.data, 
            user_id=current_user.id,
            event_id=event.event_id
        )
        db.session.add(c)
        db.session.commit()
        flash("Comment posted.", "success")
    else:
        flash("Could not post comment. Please check your input.", "warning")
    return redirect(url_for("events.event_detail", event_id=event.event_id))

# --- My Bookings Placeholder ---
@main_bp.route("/my-bookings")
@login_required
def my_bookings():
    # This is just a placeholder - the actual booking history is in tickets.py
    flash('Booking history is available in "My Bookings" section', 'info')
    return redirect(url_for('main.index'))