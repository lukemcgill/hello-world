-- ONLY FOR USE IN SHELL --
from datetime import date, time, timedelta
from website.models import db, User, Event

--- RESET (drop & recreate all tables) ---
db.drop_all()
db.create_all()

 --- Seed a basic owner user (so owner_id FK is valid) ---
owner = User(username="owner", email="owner@example.com", password_hash="dev")
db.session.add(owner)
db.session.commit()

today = date.today()

seed_events = [
    # Rock (Open)
    Event(
        owner_id=owner.id,
        title="Dz Deathrays Live",
        artist_name="Dz Deathrays",
        genre="Rock",
        capacity=100,
        venue_name="Greaser",
        location="Brisbane",
        event_date=today + timedelta(days=7),
        starts_at=time(19, 0),
        ends_at=time(22, 0),
        image_url="https://images.unsplash.com/photo-1638295415000-e692a6d44a6d?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHB1bmt8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&q=60&w=900",
        description=" Rock by the river.",
        tickets_total=100,
        tickets_available=100,
        cancelled=False,
    ),
    # Jazz (Sold Out)
    Event(
        owner_id=owner.id,
        title="Black Saint and the Sinner lady - Live",
        artist_name="Charles Mingus",
        genre="Jazz",
        capacity=80,
        venue_name="Old Parliment House",
        location="Brisbane",
        event_date=today + timedelta(days=10),
        starts_at=time(20, 0),
        ends_at=time(23, 0),
        image_url="https://images.unsplash.com/photo-1511192336575-5a79af67a629?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8amF6enxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&q=60&w=900",
        description="Smooth standards and grooves.",
        tickets_total=80,
        tickets_available=0,  
        cancelled=False,
    ),
    # Indie (Cancelled)
    Event(
        owner_id=owner.id,
        title="Forever howlong",
        artist_name="Black Country, New Road",
        genre="Indie",
        capacity=120,
        venue_name="Botanic Gardens",
        location="Brisbane",
        event_date=today + timedelta(days=14),
        starts_at=time(18, 0),
        ends_at=time(21, 0),
        image_url="https://images.unsplash.com/photo-1678984239375-53a221f58ad8?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y29hbCUyMHN0YXRpb258ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&q=60&w=900",
        description="Indie under the stars.",
        tickets_total=120,
        tickets_available=120,
        cancelled=True,         
    ),
    # Electronic (Inactive/past)
    Event(
        owner_id=owner.id,
        title="Fred again. Presents 10 cities 10 songs",
        artist_name="DJ Pulse",
        genre="Electronic",
        capacity=150,
        venue_name="Riverstage",
        location="Brisbane",
        event_date=today - timedelta(days=2),  # <- Past date
        starts_at=time(21, 0),
        ends_at=time(23, 30),
        image_url="https://images.unsplash.com/photo-1466907840060-8934465084e5?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fEhvdXNlJTIwTXVzaWN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&q=60&w=900",
        description="House bangers all night.",
        tickets_total=150,
        tickets_available=25,
        cancelled=False,
    ),
    # Hip Hop (Open)
    Event(
        owner_id=owner.id,
        title="GNX Tour",
        artist_name="Kendrick lamar",
        genre="Hip Hop",
        capacity=200,
        venue_name="South Bank Stage",
        location="Brisbane",
        event_date=today + timedelta(days=3),
        starts_at=time(17, 0),
        ends_at=time(20, 0),
        image_url="https://images.unsplash.com/photo-1543981281-3166a395e10c?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y29tcHRvbnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&q=60&w=900",
        description="From the Superbowl to southbank",
        tickets_total=200,
        tickets_available=180,
        cancelled=False,
    ),

Event(
    owner_id=owner.id,
    title="Getting killed (Live)",
    artist_name="Geese ",
    genre="Indie",
    capacity=90,
    venue_name="Burleigh Hotel",
    location="Gold Coast",
    event_date=today + timedelta(days=5),
    starts_at=time(18, 30),
    ends_at=time(21, 0),
    image_url="https://images.unsplash.com/photo-1484704324500-528d0ae4dc7d?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Z2Vlc2V8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&q=60&w=900",
    description="Rocks hottest new export",
    tickets_total=90,
    tickets_available=85,
    cancelled=False,
),

# Pop (Open)
Event(
    owner_id=owner.id,
    title="The BRAT tour",
    artist_name="Charli XCX",
    genre="Electronic",
    capacity=250,
    venue_name="Convention Centre",
    location="Sunshine Coast",
    event_date=today + timedelta(days=9),
    starts_at=time(19, 0),
    ends_at=time(22, 30),
    image_url="https://plus.unsplash.com/premium_photo-1674827393274-04d45d1026ac?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YWNpZCUyMGdyZWVufGVufDB8fDB8fHww&auto=format&fit=crop&q=60&w=900",
    description="Pop perfection live",
    tickets_total=250,
    tickets_available=200,
    cancelled=False,
),
]

db.session.add_all(seed_events)
db.session.commit()
