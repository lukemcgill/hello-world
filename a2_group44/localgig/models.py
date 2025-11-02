from datetime import datetime, date, time
from flask_login import UserMixin
from . import db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Event(db.Model):
    __tablename__ = "event"

    event_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    title = db.Column(db.String(150), nullable=False) 
    artist_name = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False) 
    venue_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)

    event_date = db.Column(db.Date, nullable=False)
    starts_at = db.Column(db.Time, nullable=False)
    ends_at = db.Column(db.Time, nullable=False)

    image_url = db.Column(db.String(300))
    description = db.Column(db.Text, nullable=False)

    tickets_total = db.Column(db.Integer, nullable=False, default=0)
    tickets_available = db.Column(db.Integer, nullable=False, default=0)
    cancelled  = db.Column(db.Boolean, default=False, nullable=False)
    
    # Price per ticket
    price_per_ticket = db.Column(db.Float, nullable=False, default=25.00)

    # Relationships 
    comments = db.relationship("Comment", backref="event", lazy="dynamic", cascade="all, delete-orphan")
    orders = db.relationship("Order", backref="event", lazy="dynamic", cascade="all, delete-orphan")

    @hybrid_property
    def status(self) -> str:
        if self.cancelled:
            return "Cancelled"
        if self.capacity is not None:
            if self.tickets_available is not None and self.tickets_available <= 0:
                return "Sold Out"
        try:
            event_end = datetime.combine(self.event_date, self.ends_at)
            if event_end < datetime.now():
                return "Inactive"
        except Exception:
            pass
        return "Open"

    def __repr__(self):
        return f"<Event {self.title} | {self.status}>"

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.event_id"), nullable=False)

    user = db.relationship("User", backref="comments", lazy=True)

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    price_per_ticket = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def total_price(self):
        return self.quantity * self.price_per_ticket

    def __repr__(self):
        return f"<Order {self.id} | User {self.user_id} | Event {self.event_id}>"