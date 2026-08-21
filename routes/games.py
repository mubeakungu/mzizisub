"""
Luck2x Games Routes
Endpoints for: Dice, Crash, Hilo, Mines, Tower, Slots, Roulette
"""
import random
import math
import json
from datetime import datetime
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy

games_bp = Blueprint('games', __name__, url_prefix='/api/games')

# Database will be injected
db = None


def set_db(database):
    """Set database instance"""
    global db
    db = database


def login_required(f):
    """Login required decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get('User-ID')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# DICE GAME
# ============================================================================
@games_bp.route('/dice/play', methods=['POST'])
@login_required
def play_dice():
    """Play Dice Game"""
    try:
        from app.models.games import DiceGame
        
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        bet_amount = float(data.get('bet_amount', 0))
        player_number = int(data.get('number', 0))
        
        if bet_amount <= 0 or not (1 <= player_number <= 6):
            return jsonify({'error': 'Invalid bet or number'}), 400
        
        # Simulate dice roll
        dice_result = random.randint(1, 6)
        result = 'win' if dice_result == player_number else 'loss'
        
        # Calculate payout (5x multiplier on win)
        multiplier = 5.0 if result == 'win' else 0.0
        payout = bet_amount * multiplier if result == 'win' else 0
        
        # Save game
        game = DiceGame(
            user_id=user_id,
            bet_amount=bet_amount,
            player_number=player_number,
            dice_result=dice_result,
            multiplier=multiplier,
            result=result,
            payout=payout
        )
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'player_number': player_number,
            'dice_result': dice_result,
            'result': result,
            'multiplier': multiplier,
            'payout': payout,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# CRASH GAME
# ============================================================================
@games_bp.route('/crash/start', methods=['POST'])
@login_required
def start_crash():
    """Start Crash Game"""
    try:
        from app.models.games import CrashGame
        
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        bet_amount = float(data.get('bet_amount', 0))
        
        if bet_amount <= 0:
            return jsonify({'error': 'Invalid bet amount'}), 400
        
        # Generate crash point (1.01 to 10.00)
        crash_point = round(random.uniform(1.01, 10.00), 2)
        
        # Save game
        game = CrashGame(
            user_id=user_id,
            bet_amount=bet_amount,
            multiplier=1.00,
            crash_point=crash_point
        )
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'bet_amount': bet_amount,
            'current_multiplier': 1.00,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@games_bp.route('/crash/cashout/<int:game_id>', methods=['POST'])
@login_required
def cashout_crash(game_id):
    """Cashout Crash Game"""
    try:
        from app.models.games import CrashGame
        
        user_id = request.headers.get('User-ID')
        game = CrashGame.query.filter_by(id=game_id, user_id=user_id).first()
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        # Calculate current multiplier (0.01 increments every 100ms approximately)
        elapsed = (datetime.utcnow() - game.created_at).total_seconds()
        current_multiplier = 1.00 + (elapsed * 0.01)
        
        result = 'win' if current_multiplier < game.crash_point else 'loss'
        payout = (game.bet_amount * current_multiplier) if result == 'win' else 0
        
        game.cashout_at = current_multiplier
        game.result = result
        game.payout = payout
        game.multiplier = current_multiplier
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'crashed_at': game.crash_point,
            'cashed_out_at': current_multiplier,
            'result': result,
            'payout': payout,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# HILO GAME
# ============================================================================
@games_bp.route('/hilo/play', methods=['POST'])
@login_required
def play_hilo():
    """Play Hi-Lo Game"""
    try:
        from app.models.games import HiloGame
        
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        bet_amount = float(data.get('bet_amount', 0))
        prediction = data.get('prediction')  # 'high' or 'low'
        
        if bet_amount <= 0 or prediction not in ['high', 'low']:
            return jsonify({'error': 'Invalid bet or prediction'}), 400
        
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        current_card = random.choice(cards)
        next_card = random.choice(cards)
        
        current_value = cards.index(current_card)
        next_value = cards.index(next_card)
        
        if prediction == 'high':
            result = 'win' if next_value > current_value else ('loss' if next_value < current_value else 'push')
        else:
            result = 'win' if next_value < current_value else ('loss' if next_value > current_value else 'push')
        
        multiplier = 1.9 if result == 'win' else 0.0
        payout = bet_amount * multiplier if result == 'win' else 0
        
        game = HiloGame(
            user_id=user_id,
            bet_amount=bet_amount,
            current_card=current_card,
            next_card=next_card,
            prediction=prediction,
            result=result,
            payout=payout
        )
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'current_card': current_card,
            'next_card': next_card,
            'prediction': prediction,
            'result': result,
            'payout': payout,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# MINES GAME
# ============================================================================
@games_bp.route('/mines/start', methods=['POST'])
@login_required
def start_mines():
    """Start Mines Game"""
    try:
        from app.models.games import MinesGame
        
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        bet_amount = float(data.get('bet_amount', 0))
        mine_count = int(data.get('mine_count', 3))
        
        if bet_amount <= 0 or not (1 <= mine_count <= 24):
            return jsonify({'error': 'Invalid bet or mine count'}), 400
        
        # Generate grid with mines
        grid = [0] * (25 - mine_count) + [1] * mine_count
        random.shuffle(grid)
        
        game = MinesGame(
            user_id=user_id,
            bet_amount=bet_amount,
            mine_count=mine_count,
            grid_state=grid
        )
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'bet_amount': bet_amount,
            'mine_count': mine_count,
            'grid_size': 25,
            'multiplier': 1.00,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@games_bp.route('/mines/reveal/<int:game_id>', methods=['POST'])
@login_required
def reveal_mines(game_id):
    """Reveal tile in Mines Game"""
    try:
        from app.models.games import MinesGame
        
        user_id = request.headers.get('User-ID')
        data = request.get_json()
        tile_index = int(data.get('tile_index', 0))
        
        game = MinesGame.query.filter_by(id=game_id, user_id=user_id).first()
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        grid = game.grid_state
        is_mine = grid[tile_index] == 1
        
        if is_mine:
            game.result = 'loss'
            game.payout = 0
            game.hit_mines += 1
        else:
            game.revealed_tiles += 1
            # Calculate multiplier based on revealed tiles
            safe_tiles = 25 - game.mine_count
            if game.revealed_tiles == safe_tiles:
                game.result = 'win'
                game.multiplier = 10.0  # All tiles revealed
                game.payout = game.bet_amount * game.multiplier
            else:
                game.multiplier = 1.0 + (game.revealed_tiles * 0.1)
        
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'tile_index': tile_index,
            'is_mine': is_mine,
            'revealed_tiles': game.revealed_tiles,
            'multiplier': game.multiplier,
            'result': game.result,
            'payout': game.payout if game.result else None,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# TOWER GAME
# ============================================================================
@games_bp.route('/tower/start', methods=['POST'])
@login_required
def start_tower():
    """Start Tower Game"""
    try:
        from app.models.games import TowerGame
        
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        bet_amount = float(data.get('bet_amount', 0))
        difficulty = data.get('difficulty', 'medium')  # easy/medium/hard
        
        if bet_amount <= 0:
            return jsonify({'error': 'Invalid bet amount'}), 400
        
        # Generate tower sequence
        tower_height = 10
        tower = [random.randint(0, 2) for _ in range(tower_height)]
        
        game = TowerGame(
            user_id=user_id,
            bet_amount=bet_amount,
            difficulty=difficulty,
            tower_sequence=tower,
            max_level=tower_height
        )
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'bet_amount': bet_amount,
            'difficulty': difficulty,
            'max_level': tower_height,
            'multiplier': 1.00,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@games_bp.route('/tower/play/<int:game_id>', methods=['POST'])
@login_required
def play_tower(game_id):
    """Play Tower level"""
    try:
        from app.models.games import TowerGame
        
        user_id = request.headers.get('User-ID')
        data = request.get_json()
        choice = int(data.get('choice', 0))  # 0, 1, or 2
        
        game = TowerGame.query.filter_by(id=game_id, user_id=user_id).first()
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        current_level = game.current_level
        if current_level > game.max_level:
            return jsonify({'error': 'Game already finished'}), 400
        
        tower = game.tower_sequence
        level_challenge = tower[current_level - 1]
        
        if choice == level_challenge:
            game.current_level += 1
            game.multiplier = 1.0 + (game.current_level * 0.5)
            
            if game.current_level > game.max_level:
                game.result = 'win'
                game.payout = game.bet_amount * game.multiplier
        else:
            game.result = 'loss'
            game.payout = 0
        
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'level': game.current_level,
            'choice': choice,
            'correct': choice == level_challenge,
            'result': game.result,
            'multiplier': game.multiplier,
            'payout': game.payout if game.result else None,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# SLOTS GAME
# ============================================================================
@games_bp.route('/slots/spin', methods=['POST'])
@login_required
def spin_slots():
    """Spin Slots"""
    try:
        from app.models.games import SlotsGame
        
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        bet_amount = float(data.get('bet_amount', 0))
        lines = int(data.get('lines', 25))
        
        if bet_amount <= 0 or not (1 <= lines <= 25):
            return jsonify({'error': 'Invalid bet or lines'}), 400
        
        # Generate reel spin
        symbols = ['🍒', '🍋', '🍊', '🍉', '💎', '👑', '7️⃣']
        reels = [random.choice(symbols) for _ in range(5)]
        
        # Check for wins (3+ matching symbols)
        win_lines = []
        result = 'loss'
        multiplier = 0.0
        payout = 0
        
        # Simple 3-in-a-row check
        if reels[0] == reels[1] == reels[2]:
            result = 'win'
            multiplier = 5.0
            win_lines.append({'line': 1, 'symbols': reels[0]})
        elif reels[2] == reels[3] == reels[4]:
            result = 'win'
            multiplier = 3.0
            win_lines.append({'line': 2, 'symbols': reels[2]})
        
        if result == 'win':
            payout = bet_amount * multiplier * (lines / 25)
        
        game = SlotsGame(
            user_id=user_id,
            bet_amount=bet_amount,
            lines=lines,
            reels=reels,
            win_lines=win_lines,
            result=result,
            multiplier=multiplier,
            payout=payout
        )
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'reels': reels,
            'lines': lines,
            'win_lines': win_lines,
            'result': result,
            'multiplier': multiplier,
            'payout': payout,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROULETTE GAME
# ============================================================================
@games_bp.route('/roulette/spin', methods=['POST'])
@login_required
def spin_roulette():
    """Spin Roulette"""
    try:
        from app.models.games import RouletteGame
        
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        bet_amount = float(data.get('bet_amount', 0))
        bet_type = data.get('bet_type')  # red, black, even, odd, number
        bet_value = data.get('bet_value')  # specific value
        
        if bet_amount <= 0 or not bet_type:
            return jsonify({'error': 'Invalid bet'}), 400
        
        # Spin the wheel (0-36, 0 and 00 are green)
        wheel_spin = random.randint(0, 36)
        
        # Determine colors and properties
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        is_red = wheel_spin in red_numbers
        is_black = wheel_spin not in red_numbers and wheel_spin != 0
        is_even = wheel_spin % 2 == 0 and wheel_spin != 0
        is_odd = wheel_spin % 2 == 1
        
        result = 'loss'
        multiplier = 0.0
        
        # Check win conditions
        if bet_type == 'red' and is_red:
            result = 'win'
            multiplier = 1.9
        elif bet_type == 'black' and is_black:
            result = 'win'
            multiplier = 1.9
        elif bet_type == 'even' and is_even:
            result = 'win'
            multiplier = 1.9
        elif bet_type == 'odd' and is_odd:
            result = 'win'
            multiplier = 1.9
        elif bet_type == 'number' and str(bet_value) == str(wheel_spin):
            result = 'win'
            multiplier = 35.0
        
        payout = bet_amount * multiplier if result == 'win' else 0
        
        game = RouletteGame(
            user_id=user_id,
            bet_amount=bet_amount,
            bet_type=bet_type,
            bet_value=bet_value,
            wheel_spin=wheel_spin,
            result=result,
            multiplier=multiplier,
            payout=payout
        )
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'game_id': game.id,
            'bet_type': bet_type,
            'bet_value': bet_value,
            'wheel_spin': wheel_spin,
            'result': result,
            'multiplier': multiplier,
            'payout': payout,
            'timestamp': game.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# GAME HISTORY & STATS
# ============================================================================
@games_bp.route('/history/<game_type>', methods=['GET'])
@login_required
def get_game_history(game_type):
    """Get game history"""
    try:
        user_id = request.headers.get('User-ID')
        limit = request.args.get('limit', 20, type=int)
        
        game_models = {
            'dice': 'DiceGame',
            'crash': 'CrashGame',
            'hilo': 'HiloGame',
            'mines': 'MinesGame',
            'tower': 'TowerGame',
            'slots': 'SlotsGame',
            'roulette': 'RouletteGame'
        }
        
        if game_type not in game_models:
            return jsonify({'error': 'Invalid game type'}), 400
        
        # Dynamically import model
        from app.models import games as games_module
        model = getattr(games_module, game_models[game_type])
        
        games = model.query.filter_by(user_id=user_id).order_by(
            model.created_at.desc()
        ).limit(limit).all()
        
        history = []
        for game in games:
            history.append({
                'id': game.id,
                'bet_amount': game.bet_amount,
                'result': game.result,
                'payout': game.payout,
                'multiplier': getattr(game, 'multiplier', None),
                'timestamp': game.created_at.isoformat()
            })
        
        return jsonify({'games': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@games_bp.route('/stats', methods=['GET'])
@login_required
def get_game_stats():
    """Get overall game statistics"""
    try:
        from app.models.games import GameStats
        
        user_id = request.headers.get('User-ID')
        
        stats = GameStats.query.filter_by(user_id=user_id).all()
        
        result = []
        for stat in stats:
            result.append({
                'game_type': stat.game_type,
                'total_bets': stat.total_bets,
                'total_wins': stat.total_wins,
                'total_losses': stat.total_losses,
                'games_played': stat.games_played,
                'win_rate': (stat.wins_count / stat.games_played * 100) if stat.games_played > 0 else 0,
                'rtp': stat.rtp,
                'highest_win': stat.highest_win,
                'highest_multiplier': stat.highest_multiplier
            })
        
        return jsonify({'stats': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
