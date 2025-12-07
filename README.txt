================================================================================
                    MTU CHESS CLUB APP - WEB APPLICATION
================================================================================

Developer:      Ogidi Elijah
Student ID:     300 Level Computer Science Student
Institution:    Mountain Top University, Ibafo, Ogun State.
Year:           2025


================================================================================
                            PROJECT OVERVIEW
================================================================================

MTU Chess Club App is a comprehensive web-based chess platform designed 
specifically for students and staff of Mountain Top University (MTU). The application enables real-time multiplayer chess games 
over LAN, with features including user authentication, ELO rating system,
tournament and leaderboard management

================================================================================
                            KEY FEATURES
================================================================================

1. USER AUTHENTICATION
   - MTU-specific matric number validation (Format: 11 digit and an initial uppercase letter + 7 digits)
   - Department and level selection
   - Secure password authentication
   - User profiles with statistics

2. REAL-TIME CHESS GAMEPLAY
   - Live multiplayer chess over LAN
   - Multiple time controls (1min to 30min + unlimited)
   - Smooth countdown timer (no stuttering)
   - Move history tracking
   - Captured pieces display
   - Check/Checkmate/Stalemate detection
   - Pawn promotion with popup selection

3. GAME FEATURES
   - Drag-and-drop piece movement
   - Click-to-move alternative
   - Legal move highlighting
   - Turn-based validation
   - Resign and draw options

4. USER DASHBOARD
   - Personal statistics (wins, losses, draws)
   - ELO rating system
   - Recent game history
   - Live games to watch

5. TOURNAMENT SYSTEM
   - View all active and completed games
   - Filter by status (waiting, active, completed)
   - Real-time game tracking

6. LEADERBOARD
   - Top players by ELO rating
   - Win rate statistics

7. GUEST MODE
   - Watch-only access for non-registered users
   - Browse active games
   - Cannot create or join games

8. MTU CHESS CLUB BRANDING
   - MTU CHESS CLUB color scheme (Blue And Red)
   - MTU logo integration
   - Department-specific features

================================================================================
                        SYSTEM REQUIREMENTS
================================================================================

SERVER REQUIREMENTS:
- Python 3.8 or higher
- Django 5.0 or higher
- SQLite (included) or PostgreSQL (production)
- 2GB RAM minimum
- 1GB storage space

CLIENT REQUIREMENTS:
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Minimum 1024x768 screen resolution
- LAN network connection

OPERATING SYSTEMS:
- Windows 7/8/10/11
- macOS 10.12+
- Linux (Ubuntu 18.04+, Debian, CentOS)

================================================================================
                        INSTALLATION GUIDE
================================================================================

STEP 1: INSTALL PYTHON
-----------------------
Download and install Python 3.8+ from python.org
Verify installation: python --version

STEP 2: INSTALL DEPENDENCIES
-----------------------------
Navigate to project folder:
    cd lan_chess

Install required packages:
    pip install -r requirements.txt

Required packages:
    - Django>=5.0,<6.0
    - Pillow>=10.0.0
    - asgiref>=3.7.0
    - sqlparse>=0.4.4
    - tzdata>=2023.3
    - python-decouple>=3.8

STEP 3: DATABASE SETUP
-----------------------
Delete old database (if exists):
    rm db.sqlite3
    rm game/migrations/0*.py

Create new migrations:
    python manage.py makemigrations game
    python manage.py migrate

Create superuser account:
    python manage.py createsuperuser
    
    Enter:
    - Username: admin (or your choice)
    - Email: admin@mtu.edu.ng
    - Password: (minimum 8 characters)
    - Matric Number: MTU/CSC/20/0001
    - Department: CSC
    - Level: 300

STEP 4: STATIC FILES
--------------------
Ensure chess piece images are in:
    game/static/game/chess_pieces/
    
Required files:
    wK.png, wQ.png, wR.png, wB.png, wN.png, wP.png (white pieces)
    bK.png, bQ.png, bR.png, bB.png, bN.png, bP.png (black pieces)

STEP 5: RUN SERVER
------------------
Start development server:
    python manage.py runserver 0.0.0.0:8000

Server will run at:
    - Local: http://localhost:8000
    - LAN: http://YOUR-IP-ADDRESS:8000

To find your IP address:
    Windows: ipconfig
    Mac/Linux: ifconfig or ip addr show

STEP 6: ACCESS APPLICATION
---------------------------
Open browser and navigate to:
    http://localhost:8000 (on host machine)
    http://192.168.1.100:8000 (from other devices, use actual IP)

================================================================================
                        PROJECT STRUCTURE
================================================================================

lan_chess/
├── lan_chess/                  # Main project folder
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
│
├── game/                       # Main application
│   ├── migrations/            # Database migrations
│   ├── static/game/           # Static files
│   │   ├── chess.js          # Chess engine
│   │   ├── chessboard.js     # Board renderer
│   │   ├── chessboard.css    # Board styling
│   │   └── chess_pieces/     # Piece images
│   ├── templates/game/        # HTML templates
│   │   ├── home.html         # Landing page
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration
│   │   ├── dashboard.html    # User dashboard
│   │   ├── play.html         # Game interface
│   │   ├── tournament.html   # Tournament view
│   │   ├── leaderboard.html  # Rankings
│   │   ├── guest.html        # Guest mode
│   │   ├── watch.html        # Spectator view
|   |   ├── recent.html       # User Recent games page
│   │   └── live.html         # active games page
|   | 
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Admin interface
│   └── tests.py               # Test cases
│
├── media/                      # User uploads
│   └── avatars/               # Profile pictures
│
├── manage.py                   # Django management
├── requirements.txt            # Python dependencies
└── README.txt                  # This file

================================================================================
                        USAGE INSTRUCTIONS
================================================================================

FOR NEW USERS:
--------------
1. Navigate to http://localhost:8000
2. Click "Register Now"
3. Fill in registration form:
   - First Name & Last Name
   - Username (unique)
   - Matric Number or Application Number
   - Department (from dropdown)
   - Level (100-500)
   - Email address
   - Password (minimum 8 characters)
4. Click "Create Account"
5. Automatically redirected to dashboard

FOR EXISTING USERS:
-------------------
1. Click "Login"
2. Enter username and password
3. Redirected to dashboard

TO HOST A GAME:
---------------
1. From dashboard, click "Play Now"
2. Select time control (1min - 30min or unlimited)
3. Click "Host New Game"
4. Share the 6-digit game code with opponent
5. Wait for opponent to join
6. Game starts automatically when opponent joins

TO JOIN A GAME:
---------------
1. Get game code from host
2. Navigate to Play page
3. Enter code in input field
4. Click "Join Game"
5. Game starts immediately

DURING GAMEPLAY:
----------------
- Drag pieces or click to move
- Timer counts down automatically
- Move history shows in right panel
- Captured pieces displayed
- Can resign or offer draw
- Game ends on checkmate, timeout, or resignation

GUEST MODE:
-----------
1. Click "Watch as Guest" on homepage
2. Browse active games
3. Click any game to spectate
4. Cannot play, only watch

================================================================================
                        ADMIN PANEL
================================================================================

ACCESS:
-------
Navigate to: http://localhost:8000/admin
Login with superuser credentials

FEATURES:
---------
- Manage users (view, edit, delete)
- Manage games (view status, results)
- View game sessions
- Track individual moves
- Monitor system activity
- Generate reports

================================================================================
                        TROUBLESHOOTING
================================================================================

PROBLEM: Server won't start
SOLUTION: 
    - Check if Python is installed: python --version
    - Check if Django is installed: pip show django
    - Check if port 8000 is free: netstat -an | find "8000"

PROBLEM: Can't access from other devices
SOLUTION:
    - Check firewall settings
    - Verify devices on same network
    - Use correct IP address (not localhost)
    - Ensure server running with 0.0.0.0:8000

PROBLEM: Database errors
SOLUTION:
    - Delete db.sqlite3
    - Delete migration files (keep __init__.py)
    - Run: python manage.py makemigrations
    - Run: python manage.py migrate

PROBLEM: Static files not loading
SOLUTION:
    - Run: python manage.py collectstatic
    - Check STATIC_ROOT in settings.py
    - Verify files in correct directories

PROBLEM: Timer stuttering/jumping
SOLUTION:
    - Clear browser cache
    - Ensure network connection stable

PROBLEM: Can't register with matric number
SOLUTION:
    - Use exact format: 11 digits or an initial uppercase letter with additional 7 digits
    - Example: 23010301040 or F2345678

PROBLEM: Game not syncing between players
SOLUTION:
    - Check internet/LAN connection
    - Refresh both browsers
    - Check browser console for errors
    - Verify both players using same game code

================================================================================
                        TECHNICAL SPECIFICATIONS
================================================================================

BACKEND:
--------
- Framework: Django 5.2
- Language: Python 3.8+
- Database: SQLite (development), PostgreSQL (production)
- Authentication: Django built-in with custom User model
- Session Management: Django sessions
- Timezone: Africa/Lagos (UTC+1)

FRONTEND:
---------
- HTML5, CSS3, JavaScript (ES6+)
- Chess Engine: chess.js library
- Board Rendering: Custom Chessboard.js
- No external frameworks (vanilla JS)
- Responsive design (mobile-friendly)

DATABASE MODELS:
----------------
1. User Model:
   - Extends AbstractUser
   - Fields: matric_number, department, level, rating, stats
   
2. Game Model:
   - Fields: code, fen, status, players, timer, moves
   
3. GameSession Model:
   - Tracks active sessions for reconnection
   
4. Move Model:
   - Individual move tracking for analysis

API ENDPOINTS:
--------------
POST /api/game/create/          - Create new game
GET  /api/game/<code>/state/    - Get game state
POST /api/game/<code>/move/     - Submit move
POST /api/game/<code>/join/     - Join game
POST /api/game/<code>/resign/   - Resign from game
POST /api/game/<code>/draw/     - Offer/accept draw
GET  /api/game/<code>/session/  - Check user session

================================================================================
                        SECURITY NOTES
================================================================================

DEVELOPMENT MODE:
-----------------
- DEBUG = True (shows detailed errors)
- SECRET_KEY exposed (change for production)
- ALLOWED_HOSTS = ['*'] (accepts all connections)
- SQLite database (not suitable for production)

PRODUCTION DEPLOYMENT:
----------------------
Must change the following in settings.py:

1. Set DEBUG = False
2. Change SECRET_KEY to new random value
3. Set ALLOWED_HOSTS = ['your-domain.com', 'your-ip']
4. Use PostgreSQL instead of SQLite
5. Enable HTTPS:
   - SECURE_SSL_REDIRECT = True
   - SESSION_COOKIE_SECURE = True
   - CSRF_COOKIE_SECURE = True
6. Configure proper STATIC_ROOT and MEDIA_ROOT
7. Use environment variables for secrets
8. Set up proper backup system
9. Configure rate limiting
10. Enable Django security middleware

CSRF Protection:
----------------
Currently using @csrf_exempt on API endpoints for development.
For production, implement proper CSRF token handling.

================================================================================
                        KNOWN LIMITATIONS
================================================================================

1. POLLING vs WEBSOCKETS
   - Current: HTTP polling (1-second intervals)
   - Future: WebSocket for true real-time
   - Impact: Slight delay in move updates

2. NO AI OPPONENT
   - Only human vs human games
   - Future: Integrate Stockfish or similar

3. BASIC TOURNAMENT
   - Manual tournament management
   - No bracket system yet
   - Future: Automatic pairing, Swiss system

4. NO CHAT FEATURE
   - Players can't communicate in-app
   - Future: Add chat, emojis, quick messages

5. NO MOBILE APP
   - Web-only (responsive design)
   - Future: React Native or Flutter app

6. NO GAME ANALYSIS
   - No post-game move analysis
   - Future: Engine evaluation, mistakes highlight

================================================================================
                        FUTURE ENHANCEMENTS
================================================================================

VERSION 2.0 ROADMAP:
--------------------
- WebSocket integration for instant updates
- AI opponent (Stockfish integration)
- Video chat during games (WebRTC)
- Advanced tournament system (brackets, Swiss)
- Game replay and analysis
- Puzzle section (daily chess puzzles)
- Interactive lessons
- Social features (friends, chat, clubs)
- Achievement system (badges, rewards)
- Mobile native apps (iOS/Android)
- Email notifications
- Game export (PGN format)
- Opening book integration
- Time increment (Fischer timing)
- Rated vs unrated games toggle
- Private games with passwords
- Spectator chat
- Live streaming support

================================================================================
                        CREDITS & ACKNOWLEDGMENTS
================================================================================

Developer:              Ogidi Elijah
Institution:            Mountain Top University, Ibafo, Ogun State.
Department:             Computer Science
Level:                  300 Level
Year:                   2025


Technologies Used:
    - Django (Python Web Framework)
    - chess.js (Chess Engine)
    - SQLite (Database)
    - HTML5/CSS3/JavaScript

External Libraries:
    - chess.js by Jeff Hlywa (MIT License)
    - Chess piece images from Wikimedia Commons (Public Domain)

Special Thanks:
    - Shola
    - Ajayi Emmanuel
    - Maxwel


================================================================================
                        LICENSE & COPYRIGHT
================================================================================

Copyright (c) 2025 Ogidi Elijah
All rights reserved.

This project is developed for educational and non-commercial use only.
Commercial use requires explicit permission from the developer.

================================================================================
                        CONTACT INFORMATION
================================================================================

Developer:      Ogidi Elijah
Email:          elijahogidi@mtu.edu.ng
Institution:    Mountain Top University, Ibafo, Ogun State
Department:     Computer Science
Level:          300 Level
Project Duration: 2025-11-00*   -  2025-12-07
Project GitHub: 


For support, bug reports, or feature requests:
Contact via email or submit issue on GitHub

================================================================================
                        VERSION HISTORY
================================================================================

Version 1.0.0 (2025-12-07)
--------------------------
- Initial release
- User authentication with MTU matric validation
- Real-time multiplayer chess
- Timer system with multiple controls
- Dashboard and statistics
- Tournament management
- Leaderboard system
- Guest mode
- Session reconnection
- MTU CHESS CLUB branding and design



================================================================================
                        FINAL NOTES
================================================================================

This chess application demonstrates practical application of web development skills,
database management, real-time systems, and user-centered design.

The platform is designed to promote chess culture at MTU, provide a learning
tool for students, and serve as a foundation for campus-wide chess tournaments.

All code is original and written specifically for this project, with proper
attribution to external libraries used.

Thank you for taking the time to review this project!

Ogidi Elijah
300 Level Computer Science Student
Mountain Top University, Ibafo, Ogun State
2025

================================================================================
                        END OF README
================================================================================