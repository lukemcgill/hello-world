from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required

from .models import db, Event
from .forms import EventForm, CommentForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template('index.html')

events_bp = Blueprint("events", __name__, url_prefix="/events")

@events_bp.route("/create", methods=["GET", "POST"])
#Creat Event method
def create_event():
    form = EventForm()
    #checks for end time before start time
    if form.validate_on_submit():
        if form.ends_at.data <= form.starts_at.data:
            flash("End time must be after start time.", "warning")
            return render_template("create-event.html", form=form)
        ev = Event(
            owner_id=1,  # placeholder until user is implemented
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
        )
        db.session.add(ev)
        db.session.commit()
        flash("Event created.") #Validation mesage
        return redirect(url_for("events.event_detail", event_id=ev.event_id)) #Brings user to the created event page
    return render_template("create-event.html", form=form)


@events_bp.route("/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comments = event.comments.order_by(
        Event.comments.prop.mapper.class_.created_at.desc()
    ).all()
    form = CommentForm()
    #Render event detail page with comments and comment form from event id
    return render_template(
        "event-detail.html",
        event=event,
        comments=comments,
        comment_form=form,
    )

#Cancel event button route
@events_bp.route("/<int:event_id>/cancel", methods=["POST"])
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)

    # Get current or placeholder user
    user_id = current_user.id if getattr(current_user, "is_authenticated", False) else 1

    if user_id == event.owner_id:
        if not event.cancelled:
            event.cancelled = True
            db.session.commit()
            flash("Event cancelled.", "success")
        else:
            flash("Event already cancelled.", "info")
    else:
        flash("You don't have permission to cancel this event.", "warning")

    return redirect(url_for("events.event_detail", event_id=event.event_id))


@events_bp.route("/<int:event_id>/comment", methods=["POST"])
@login_required
def post_comment(event_id):
    event = Event.query.get_or_404(event_id)
    form = CommentForm()
    #Commits comment to db, with user and event id
    if form.validate_on_submit():
        from .models import Comment
        c = Comment(body=form.body.data, user_id=1, event_id=event.event_id)
        db.session.add(c)
        db.session.commit()
        flash("Comment posted.", "success")
    else:
        flash("Could not post comment. Please check your input.", "warning")
    return redirect(url_for("events.event_detail", event_id=event.event_id))