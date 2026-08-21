# Luck2x Casino Games - Installation Guide

## Quick Start (5 minutes)

### 1. Extract Files
```bash
unzip mzizibet_feature_pack.zip
cd mzizibet_feature_pack
```

### 2. Copy Files to Your Mzizi Installation
```bash
# Copy models
cp app/models/games.py /path/to/your/mzizi/app/models/

# Copy routes
cp app/routes/games.py /path/to/your/mzizi/app/routes/

# Copy templates
cp -r app/templates/games/ /path/to/your/mzizi/app/templates/

# Copy config
cp config/games_config.py /path/to/your/mzizi/config/
```

### 3. Update Flask App (`app/__init__.py`)
```python
from app.routes.games import games_bp, set_db

def create_app():
    app = Flask(__name__)
    
    # ... existing config ...
    
    # Initialize database
    db.init_app(app)
    
    # Register game blueprint
    app.register_blueprint(games_bp)
    
    # Set database for games
    with app.app_context():
        set_db(db)
        db.create_all()
    
    return app
```

### 4. Install Dependencies
```bash
pip install -r requirements-games.txt
```

### 5. Configure Environment
```bash
# Copy and edit environment file
cp .env.games.example .env.games
nano .env.games
```

### 6. Run Database Migrations
```bash
flask db migrate -m "Add Luck2x Casino Games"
flask db upgrade
```

### 7. Add to Navigation
In `app/templates/base.html`, add:
```html
<a href="/games" class="nav-link">🎮 Play Games</a>
```

### 8. Test
```bash
python app.py
# Visit http://localhost:5000/games
```

---

## Detailed Installation

### Prerequisites
- Python 3.8+
- Flask 2.0+
- PostgreSQL 12+
- Redis (optional, for caching)

### Step-by-Step Setup

#### Step 1: Verify Mzizi Installation
```bash
cd /path/to/your/mzizi
ls -la app/
# Should show: models/, routes/, templates/, etc.
```

#### Step 2: Backup Existing Files
```bash
cp -r app app.backup
```

#### Step 3: Copy Game Module Files
```bash
# Copy all game files
cp -r path/to/extracted/app/* app/

# Verify copies
ls -la app/models/games.py
ls -la app/routes/games.py
ls -la app/templates/games/
```

#### Step 4: Update Application Configuration
Edit `config.py`:
```python
import os

class Config:
    # ... existing config ...
    
    # Games Configuration
    GAMES_MIN_BET = 1
    GAMES_MAX_BET = 10000
    GAMES_DATABASE_URI = os.getenv('GAMES_DB_URI', 'postgresql://user:pass@localhost/mzizi_games')
```

#### Step 5: Create .env File
```bash
cp .env.games.example .env.games
```

Edit `.env.games` with your values:
```
GAMES_DB_HOST=your_db_host
GAMES_DB_USER=your_db_user
GAMES_DB_PASSWORD=your_db_password
GAMES_DB_NAME=mzizi_games
```

#### Step 6: Install Dependencies
```bash
# Create virtual environment (if not already done)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements-games.txt
```

#### Step 7: Database Setup
```bash
# Create database (if not using Mzizi's existing DB)
createdb mzizi_games

# Run migrations
flask db init  # Skip if already initialized
flask db migrate -m "Add Luck2x Casino Games"
flask db upgrade

# Verify tables created
psql -U postgres -d mzizi_games -c "\dt"
# Should show dice_games, crash_games, hilo_games, etc.
```

#### Step 8: Update Flask App
Edit `app/__init__.py`:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes.games import games_bp, set_db
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(games_bp)
    
    # Database setup
    with app.app_context():
        set_db(db)
        db.create_all()
    
    return app
```

#### Step 9: Add Navigation Link
Edit `app/templates/base.html`:
```html
<nav class="navbar">
    <a href="/">Home</a>
    <a href="/games" class="nav-link">🎮 Games</a>
    <a href="/account">Account</a>
</nav>
```

#### Step 10: Test Installation
```bash
# Start Flask app
python app.py

# In another terminal, test API
curl -X GET http://localhost:5000/games \
  -H "User-ID: test_user"

# Should return games hub HTML
```

---

## Troubleshooting

### Issue: ImportError for games module
```
Solution: Ensure app/models/games.py exists
Check: ls -la app/models/games.py
```

### Issue: Database tables not created
```
Solution: Run migrations
Command: flask db upgrade
Check: psql -d mzizi_games -c "\dt" | grep games
```

### Issue: 404 on /games route
```
Solution: Blueprint not registered
Check: In app/__init__.py, verify set_db(db) is called
```

### Issue: User-ID header required error
```
Solution: Add User-ID header to requests
Example: curl -H "User-ID: 123" http://localhost:5000/api/games/stats
```

### Issue: Database connection refused
```
Solution: Check PostgreSQL is running and credentials are correct
Command: psql -U postgres -c "SELECT 1"
```

---

## Post-Installation Configuration

### 1. Configure Game Settings
Edit `config/games_config.py`:
```python
class GamesConfig:
    MIN_BET = 1          # Minimum bet in base currency
    MAX_BET = 10000      # Maximum bet
    DICE_MULTIPLIER = 5.0
    # ... adjust other settings as needed
```

### 2. Set Up M-Pesa Integration (Optional)
If using M-Pesa:
```bash
# Update .env.games with M-Pesa credentials
MPESA_API_KEY=your_key
MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
```

### 3. Configure Redis Cache (Optional)
```bash
# Start Redis
redis-server

# Update .env.games
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 4. Set Up Email Notifications (Optional)
```bash
# Update .env.games with email credentials
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

---

## Testing the Installation

### 1. Test Games Hub
```
Navigate to: http://localhost:5000/games
Should show: 7 game cards (Dice, Crash, Hilo, Mines, Tower, Slots, Roulette)
```

### 2. Test API Endpoint
```bash
curl -X POST http://localhost:5000/api/games/dice/play \
  -H "User-ID: test_user" \
  -H "Content-Type: application/json" \
  -d '{"bet_amount": 100, "number": 4}'

# Should return game result JSON
```

### 3. Test Database
```bash
psql -U postgres -d mzizi_games -c "SELECT COUNT(*) FROM dice_games;"
# Should show: count
#        0
```

### 4. Run Unit Tests (if included)
```bash
pytest tests/test_games.py -v
```

---

## Verification Checklist

- [ ] All files copied to correct directories
- [ ] `app/__init__.py` updated with blueprint registration
- [ ] Database migrations run successfully
- [ ] Environment file created and configured
- [ ] Dependencies installed
- [ ] Navigation link added to base template
- [ ] `/games` URL loads successfully
- [ ] API endpoints respond correctly
- [ ] Database tables created
- [ ] No errors in Flask logs

---

## Next Steps

1. **Customize Game Settings**
   - Adjust bet limits in `config/games_config.py`
   - Configure RTP targets
   - Set house edge

2. **Enable Features**
   - Configure M-Pesa integration
   - Set up email notifications
   - Enable analytics tracking

3. **Deploy to Production**
   - Update `.env.games` with production values
   - Use production database
   - Enable security settings
   - Set DEBUG = False

4. **Monitor and Maintain**
   - Check error logs regularly
   - Monitor game statistics
   - Backup database daily
   - Review player activity

---

## Support

For issues:
1. Check GAMES_README.md
2. Review GAMES_INTEGRATION.md
3. Check Flask error logs
4. Verify database connectivity
5. Ensure all files are in correct locations

**Enjoy your new casino platform! 🎮**

---

**Version**: 1.0  
**Last Updated**: August 20, 2024  
**Compatibility**: Python 3.8+, Flask 2.0+, PostgreSQL 12+
