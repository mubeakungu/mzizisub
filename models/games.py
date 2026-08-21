"""
Luck2x Games Integration Models
7 Core Games: Dice, Crash, Hilo, Mines, Tower, Slots, Roulette
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DiceGame(db.Model):
    """Dice Game Model"""
    __tablename__ = 'dice_games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    player_number = db.Column(db.Integer, nullable=False)  # 1-6
    dice_result = db.Column(db.Integer)
    multiplier = db.Column(db.Float)
    result = db.Column(db.String(20))  # win/loss
    payout = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DiceGame {self.id}>'


class CrashGame(db.Model):
    """Crash Game Model"""
    __tablename__ = 'crash_games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    multiplier = db.Column(db.Float, nullable=False)
    crash_point = db.Column(db.Float)
    cashout_at = db.Column(db.Float)
    result = db.Column(db.String(20))  # win/loss
    payout = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CrashGame {self.id}>'


class HiloGame(db.Model):
    """Hi-Lo Game Model"""
    __tablename__ = 'hilo_games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    current_card = db.Column(db.String(5))
    next_card = db.Column(db.String(5))
    prediction = db.Column(db.String(10))  # high/low
    result = db.Column(db.String(20))  # win/loss/push
    payout = db.Column(db.Float)
    streak = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HiloGame {self.id}>'


class MinesGame(db.Model):
    """Mines Game Model"""
    __tablename__ = 'mines_games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    mine_count = db.Column(db.Integer, default=3)  # 1-24
    revealed_tiles = db.Column(db.Integer, default=0)
    hit_mines = db.Column(db.Integer, default=0)
    grid_state = db.Column(db.JSON)  # Store grid configuration
    result = db.Column(db.String(20))  # win/loss
    payout = db.Column(db.Float)
    multiplier = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MinesGame {self.id}>'


class TowerGame(db.Model):
    """Tower Game Model"""
    __tablename__ = 'tower_games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.String(20))  # easy/medium/hard
    current_level = db.Column(db.Integer, default=1)
    max_level = db.Column(db.Integer, default=10)
    tower_sequence = db.Column(db.JSON)  # Store tower layout
    result = db.Column(db.String(20))  # win/loss
    payout = db.Column(db.Float)
    multiplier = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TowerGame {self.id}>'


class SlotsGame(db.Model):
    """Slots Game Model"""
    __tablename__ = 'slots_games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    lines = db.Column(db.Integer, default=25)
    reels = db.Column(db.JSON)  # Store reel positions
    win_lines = db.Column(db.JSON)  # Store winning lines
    result = db.Column(db.String(20))  # win/loss
    payout = db.Column(db.Float)
    multiplier = db.Column(db.Float)
    free_spins = db.Column(db.Integer, default=0)
    is_jackpot = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SlotsGame {self.id}>'


class RouletteGame(db.Model):
    """Roulette Game Model"""
    __tablename__ = 'roulette_games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bet_amount = db.Column(db.Float, nullable=False)
    bet_type = db.Column(db.String(50))  # red/black/even/odd/number/range
    bet_value = db.Column(db.String(50))  # specific value based on bet type
    wheel_spin = db.Column(db.Integer)  # 0-36
    result = db.Column(db.String(20))  # win/loss
    payout = db.Column(db.Float)
    multiplier = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RouletteGame {self.id}>'


class GameStats(db.Model):
    """Game Statistics Model"""
    __tablename__ = 'game_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_type = db.Column(db.String(50))  # dice, crash, hilo, etc.
    total_bets = db.Column(db.Float, default=0)
    total_wins = db.Column(db.Float, default=0)
    total_losses = db.Column(db.Float, default=0)
    total_payouts = db.Column(db.Float, default=0)
    games_played = db.Column(db.Integer, default=0)
    wins_count = db.Column(db.Integer, default=0)
    losses_count = db.Column(db.Integer, default=0)
    highest_win = db.Column(db.Float, default=0)
    highest_multiplier = db.Column(db.Float, default=0)
    rtp = db.Column(db.Float, default=0)  # Return to Player percentage
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<GameStats {self.game_type}>'
