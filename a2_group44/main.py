from localgig import create_app, db
from werkzeug.security import generate_password_hash
from flask import render_template

app = create_app()

# Add error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Create tables and sample data
with app.app_context():
    db.create_all()
    
    # Import models inside app context
    from localgig.models import User, Event
    from datetime import date, time
    
    # Check if we need to create sample data
    if User.query.count() == 0:
        print("Creating default user...")
        
        # Create a default user for the sample events with all required fields
        default_user = User(
            first_name="Admin",
            surname="User", 
            username="admin",
            email="admin@localgig.com",
            contact_number="0412345678",
            street_address="123 Admin Street, City",
            password_hash=generate_password_hash("password123")
        )
        db.session.add(default_user)
        db.session.commit()
        print("Default user created with ID: 1")
    
    # Check if we need to create sample events
    if Event.query.count() == 0:
        print("Creating sample events with prices...")
        
        # Create sample events with the default user as owner and reasonable prices
        sample_events = [
            Event(
                owner_id=1,
                title="Summer Rock Festival",
                artist_name="The Local Band",
                genre="Rock",
                capacity=200,
                venue_name="Riverside Park",
                location="123 Park Avenue, City",
                event_date=date(2025, 12, 15),
                starts_at=time(19, 0),
                ends_at=time(23, 0),
                image_url="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                description="Annual summer rock festival featuring the best local bands. Food trucks and beverages available. Don't miss this incredible night of live music under the stars!",
                tickets_total=200,
                tickets_available=150,
                price_per_ticket=45.00
            ),
            Event(
                owner_id=1,
                title="Smooth Jazz Night",
                artist_name="Smooth Jazz Quartet", 
                genre="Jazz",
                capacity=100,
                venue_name="The Blue Note Club",
                location="456 Jazz Street, Downtown",
                event_date=date(2025, 11, 20),
                starts_at=time(20, 0),
                ends_at=time(23, 30),
                image_url="https://images.unsplash.com/photo-1529502669403-c073b74fcefb?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1470",
                description="An evening of smooth jazz with talented local musicians. Intimate setting, great acoustics, and a sophisticated atmosphere perfect for jazz enthusiasts.",
                tickets_total=100,
                tickets_available=25,
                price_per_ticket=35.00
            ),
            Event(
                owner_id=1,
                title="Indie Showcase",
                artist_name="Various Artists",
                genre="Indie",
                capacity=150,
                venue_name="The Underground",
                location="789 Music Lane, Arts District",
                event_date=date(2025, 11, 25),
                starts_at=time(18, 0),
                ends_at=time(22, 0),
                image_url="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                description="Showcase of emerging indie artists from the local scene. Discover new music and support up-and-coming talent in an intimate venue setting.",
                tickets_total=150,
                tickets_available=150,
                price_per_ticket=20.00
            ),
            Event(
                owner_id=1,
                title="Electronic Dance Night",
                artist_name="DJ Pulse & Friends",
                genre="Electronic",
                capacity=300,
                venue_name="Neon Club",
                location="321 Electric Avenue, Warehouse District",
                event_date=date(2025, 12, 5),
                starts_at=time(22, 0),
                ends_at=time(4, 0),
                image_url="https://images.unsplash.com/photo-1571330735066-03aaa9429d89?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80",
                description="High-energy electronic music night featuring local DJs. State-of-the-art sound system and light show. 18+ event with full bar service.",
                tickets_total=300,
                tickets_available=80,
                price_per_ticket=30.00
            ),
            Event(
                owner_id=1,
                title="Hip Hop Block Party",
                artist_name="Urban Flow Collective",
                genre="Hip Hop",
                capacity=250,
                venue_name="City Square",
                location="567 Main Street, City Center",
                event_date=date(2025, 11, 30),
                starts_at=time(16, 0),
                ends_at=time(21, 0),
                image_url="https://images.unsplash.com/photo-1621976360623-004223992275?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1428",
                description="Outdoor hip hop block party featuring local MCs, breakdancers, and graffiti artists. Free entry, food vendors, and community vibes.",
                tickets_total=250,
                tickets_available=250,
                price_per_ticket=15.00
            ),
            Event(
                owner_id=1,
                title="Acoustic Sessions",
                artist_name="Local Songwriters Circle",
                genre="Indie",
                capacity=80,
                venue_name="The Cozy Corner Cafe",
                location="890 Harmony Lane, West End",
                event_date=date(2025, 11, 18),
                starts_at=time(19, 30),
                ends_at=time(22, 0),
                image_url="https://plus.unsplash.com/premium_photo-1681492664700-27fa50f438ae?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1470",
                description="Intimate acoustic performances by local songwriters. Coffee, desserts, and heartfelt music in a cozy cafe setting. Perfect for a relaxed evening.",
                tickets_total=80,
                tickets_available=15,
                price_per_ticket=25.00
            )
        ]
        
        for event in sample_events:
            db.session.add(event)
        
        db.session.commit()
        print(f"✅ {len(sample_events)} sample events created successfully!")
    
    # Count events for verification
    event_count = Event.query.count()
    user_count = User.query.count()
    print(f"📊 Database ready with {user_count} users and {event_count} events")

if __name__ == "__main__":
    app.run(debug=True)