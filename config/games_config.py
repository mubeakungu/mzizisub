"""
Luck2x Casino Games Configuration
"""

class GamesConfig:
    """Games Configuration Settings"""

    # Game Limits
    MIN_BET = 1
    MAX_BET = 10000
    DEFAULT_BET = 100

    # RTP (Return to Player) Targets
    DICE_RTP = 0.96
    CRASH_RTP = 0.95
    HILO_RTP = 0.97
    MINES_RTP = 0.96
    TOWER_RTP = 0.95
    SLOTS_RTP = 0.94
    ROULETTE_RTP = 0.97

    # Multipliers
    DICE_MULTIPLIER = 5.0
    CRASH_MAX_MULTIPLIER = 10.0
    HILO_MULTIPLIER = 1.9
    MINES_MAX_MULTIPLIER = 10.0
    TOWER_MAX_MULTIPLIER = 6.0
    SLOTS_MAX_MULTIPLIER = 50.0
    ROULETTE_MAX_MULTIPLIER = 35.0

    # Game-Specific Settings
    MINES_GRID_SIZE = 25
    MINES_MIN_MINES = 1
    MINES_MAX_MINES = 24

    TOWER_LEVELS = 10
    TOWER_CHOICES = 3

    SLOTS_REELS = 5
    SLOTS_MIN_PAYLINES = 1
    SLOTS_MAX_PAYLINES = 25
    SLOTS_SYMBOLS = ['🍒', '🍋', '🍊', '🍉', '💎', '👑', '7️⃣']

    ROULETTE_NUMBERS = 37  # 0-36

    # Crash Game
    CRASH_MULTIPLIER_INCREMENT = 0.01
    CRASH_UPDATE_INTERVAL = 0.1  # seconds

    # User Limits
    DAILY_LOSS_LIMIT = 100000
    DAILY_BET_LIMIT = 500000
    MAX_CONCURRENT_GAMES = 5

    # Timeouts
    GAME_TIMEOUT = 3600  # 1 hour
    SESSION_TIMEOUT = 1800  # 30 minutes

    # Feature Flags
    ENABLE_DEMO_MODE = True
    ENABLE_LIVE_STATS = True
    ENABLE_LEADERBOARD = True

    # Analytics
    TRACK_GAME_EVENTS = True
    TRACK_PLAYER_BEHAVIOR = True

    # Currency
    PRIMARY_CURRENCY = 'KES'
    SECONDARY_CURRENCY = 'USD'
    KES_TO_USD_RATE = 0.0078  # Approximate rate

    # Notification Settings
    NOTIFY_ON_BIG_WIN = True
    BIG_WIN_THRESHOLD = 10000
    NOTIFY_ON_STREAK = True
    STREAK_LENGTH = 5

    # Database
    GAMES_TABLE_PREFIX = ''
    GAMES_DB_POOL_SIZE = 20
    GAMES_DB_POOL_RECYCLE = 3600

    # Cache Settings
    CACHE_STATS = True
    CACHE_TTL = 300  # 5 minutes
    CACHE_HISTORY = True

    # Security
    REQUIRE_2FA_FOR_LARGE_BETS = False
    LARGE_BET_THRESHOLD = 50000
    ANTI_CHEAT_ENABLED = True

    # Responsible Gaming
    ENABLE_SESSION_LIMITS = True
    DEFAULT_SESSION_LIMIT = 10800  # 3 hours
    ENABLE_LOSS_LIMITS = True
    DEFAULT_LOSS_LIMIT = 50000

    # Fraud Detection
    DETECT_SUSPICIOUS_PATTERNS = True
    PATTERN_CHECK_INTERVAL = 300  # 5 minutes
    ANOMALY_THRESHOLD = 0.95  # 95% deviation

    @classmethod
    def get_game_config(cls, game_type):
        """Get configuration for specific game"""
        configs = {
            'dice': {
                'min_bet': cls.MIN_BET,
                'max_bet': cls.MAX_BET,
                'multiplier': cls.DICE_MULTIPLIER,
                'rtp': cls.DICE_RTP,
                'options': list(range(1, 7))
            },
            'crash': {
                'min_bet': cls.MIN_BET,
                'max_bet': cls.MAX_BET,
                'max_multiplier': cls.CRASH_MAX_MULTIPLIER,
                'rtp': cls.CRASH_RTP,
                'increment': cls.CRASH_MULTIPLIER_INCREMENT
            },
            'hilo': {
                'min_bet': cls.MIN_BET,
                'max_bet': cls.MAX_BET,
                'multiplier': cls.HILO_MULTIPLIER,
                'rtp': cls.HILO_RTP,
                'options': ['high', 'low']
            },
            'mines': {
                'min_bet': cls.MIN_BET,
                'max_bet': cls.MAX_BET,
                'grid_size': cls.MINES_GRID_SIZE,
                'min_mines': cls.MINES_MIN_MINES,
                'max_mines': cls.MINES_MAX_MINES,
                'max_multiplier': cls.MINES_MAX_MULTIPLIER,
                'rtp': cls.MINES_RTP
            },
            'tower': {
                'min_bet': cls.MIN_BET,
                'max_bet': cls.MAX_BET,
                'levels': cls.TOWER_LEVELS,
                'choices': cls.TOWER_CHOICES,
                'max_multiplier': cls.TOWER_MAX_MULTIPLIER,
                'rtp': cls.TOWER_RTP,
                'difficulties': ['easy', 'medium', 'hard']
            },
            'slots': {
                'min_bet': cls.MIN_BET,
                'max_bet': cls.MAX_BET,
                'reels': cls.SLOTS_REELS,
                'min_paylines': cls.SLOTS_MIN_PAYLINES,
                'max_paylines': cls.SLOTS_MAX_PAYLINES,
                'max_multiplier': cls.SLOTS_MAX_MULTIPLIER,
                'rtp': cls.SLOTS_RTP,
                'symbols': cls.SLOTS_SYMBOLS
            },
            'roulette': {
                'min_bet': cls.MIN_BET,
                'max_bet': cls.MAX_BET,
                'numbers': cls.ROULETTE_NUMBERS,
                'max_multiplier': cls.ROULETTE_MAX_MULTIPLIER,
                'rtp': cls.ROULETTE_RTP,
                'bet_types': ['red', 'black', 'even', 'odd', 'number']
            }
        }
        return configs.get(game_type, {})

    @classmethod
    def is_valid_bet(cls, bet_amount):
        """Validate bet amount"""
        return cls.MIN_BET <= bet_amount <= cls.MAX_BET

    @classmethod
    def get_rtp_for_game(cls, game_type):
        """Get RTP percentage for game"""
        rtp_map = {
            'dice': cls.DICE_RTP,
            'crash': cls.CRASH_RTP,
            'hilo': cls.HILO_RTP,
            'mines': cls.MINES_RTP,
            'tower': cls.TOWER_RTP,
            'slots': cls.SLOTS_RTP,
            'roulette': cls.ROULETTE_RTP
        }
        return rtp_map.get(game_type, 0.95)
