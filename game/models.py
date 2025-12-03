from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
import json

START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class User(AbstractUser):
    """Extended user model for MTU Chess Club"""
    
    DEPARTMENT_CHOICES = (
        ('CSC', 'Computer Science'),
        ('MCM', 'Mass Communication'),
        ('NUR', 'Nursing Science'),
        ('IT', 'Information Technology'),
        ('EEE', 'Electrical Engineering'),
        ('MCE', 'Mechanical Engineering'),
        ('CVE', 'Civil Engineering'),
        ('CHE', 'Chemical Engineering'),
        ('MTH', 'Mathematics'),
        ('PHY', 'Physics'),
        ('CHM', 'Chemistry'),
        ('BIO', 'Biology'),
        ('OTHER', 'Other'),
    )
    
    # Enhanced matric number validation for both regular and foundation students
    # Regular: 11 digits (e.g., 23010301040)
    # Foundation: 1 letter + 7 digits (e.g., F2301040)
    matric_validator = RegexValidator(
        regex=r'^(\d{11}|[A-Z]\d{7})$',
        message='Enter a valid matric number or Application Number'
    )
    
    matric_number = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[matric_validator],
        help_text='Enter your Matric Number or your Application Number'
    )
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    level = models.IntegerField(
        choices=((50, 'Foundation'),(100, '100 Level'), (200, '200 Level'), (300, '300 Level'), 
                 (400, '400 Level'), (500, '500 Level')),
        default=100
    )
    
    # Profile
    bio = models.TextField(blank=True, null=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Stats
    total_games = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    
    # Rating
    rating = models.IntegerField(
        default=None, 
        null=True, 
        blank=True,
        help_text='ELO rating - assigned after 5 games'
    )
    rating_assigned = models.BooleanField(
        default=False,
        help_text='True if rating has been calculated'
    )
    
    # Achievements & Streaks
    longest_win_streak = models.IntegerField(default=0)
    current_win_streak = models.IntegerField(default=0)
    achievements = models.JSONField(default=list, blank=True)
    
    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.matric_number})"
    
    @property 
    def win_rate(self):
        """Calculate win percentage"""
        if self.total_games == 0:
            return 0
        return round((self.wins / self.total_games) * 100, 1)
    
    @property
    def is_rated(self):
        """Check if user has been assigned a rating"""
        return self.rating is not None and self.rating_assigned
    
    @property
    def display_rating(self):
        """Get rating for display"""
        if self.rating is None:
            games_needed = max(0, 5 - self.total_games)
            return f"Unrated ({games_needed} games needed)"
        return self.rating
    
    def update_stats(self, result):
        """Update user statistics after a game"""
        self.total_games += 1
        
        if result == 'win':
            self.wins += 1
            self.current_win_streak += 1
            if self.current_win_streak > self.longest_win_streak:
                self.longest_win_streak = self.current_win_streak
            if self.rating is not None:
                self.rating += 10
        elif result == 'loss':
            self.losses += 1
            self.current_win_streak = 0
            if self.rating is not None:
                self.rating -= 10
        elif result == 'draw':
            self.draws += 1
            self.current_win_streak = 0
        
        # Assign initial rating after 5 games
        if self.total_games == 5 and not self.rating_assigned:
            self.assign_initial_rating()
        
        # Check for achievements
        self.check_achievements()
        
        self.save()
    
    def assign_initial_rating(self):
        """Calculate and assign initial rating based on first 5 games"""
        base_rating = 1000
        rating_adjustment = (self.wins * 20) + (self.losses * -15) + (self.draws * 5)
        self.rating = max(800, min(2000, base_rating + rating_adjustment))
        self.rating_assigned = True
    
    def check_achievements(self):
        """Check and award achievements"""
        achievements = self.achievements or []
        
        # First Win
        if self.wins == 1 and 'first_win' not in achievements:
            achievements.append('first_win')
        
        # 10 Games Milestone
        if self.total_games >= 10 and '10_games' not in achievements:
            achievements.append('10_games')
        
        # Winning Streak
        if self.current_win_streak >= 5 and 'win_streak_5' not in achievements:
            achievements.append('win_streak_5')
        
        # High Rating
        if self.rating and self.rating >= 1500 and 'rating_1500' not in achievements:
            achievements.append('rating_1500')
        
        self.achievements = achievements


class Game(models.Model):
    """Chess game model with enhanced timer tracking"""
    
    GAME_STATUS = (
        ('waiting', 'Waiting for opponent'),
        ('active', 'Game in progress'),
        ('completed', 'Game completed'),
        ('abandoned', 'Game abandoned'),
    )
    
    TIME_CONTROL_CHOICES = (
        ('bullet_1', '1 min (Bullet)'),
        ('bullet_2', '2 min (Bullet)'),
        ('blitz_3', '3 min (Blitz)'),
        ('blitz_5', '5 min (Blitz)'),
        ('rapid_10', '10 min (Rapid)'),
        ('rapid_15', '15 min (Rapid)'),
        ('classical_30', '30 min (Classical)'),
        ('unlimited', 'Unlimited'),
    )
    
    code = models.CharField(max_length=8, unique=True, db_index=True)
    fen = models.CharField(max_length=100, default=START_FEN)
    status = models.CharField(max_length=20, choices=GAME_STATUS, default='waiting')
    
    # Players
    white_player = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='games_as_white'
    )
    black_player = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='games_as_black'
    )
    
    # Guest player names
    white_guest_name = models.CharField(max_length=50, blank=True, null=True)
    black_guest_name = models.CharField(max_length=50, blank=True, null=True)
    
    # Game settings
    time_control = models.CharField(
        max_length=20, 
        choices=TIME_CONTROL_CHOICES, 
        default='blitz_5'
    )
    is_rated = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    
    # timer tracking
    white_time_remaining = models.IntegerField(default=300)
    black_time_remaining = models.IntegerField(default=300)
    last_move_time = models.DateTimeField(null=True, blank=True)
    
    # NEW: Track when timer was last updated to prevent double-counting
    timer_last_updated = models.DateTimeField(null=True, blank=True)
    
    # Game result
    winner = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        choices=(('white', 'White'), ('black', 'Black'), ('draw', 'Draw'))
    )
    result_reason = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        choices=(
            ('checkmate', 'Checkmate'),
            ('resignation', 'Resignation'),
            ('timeout', 'Time out'),
            ('stalemate', 'Stalemate'),
            ('insufficient', 'Insufficient material'),
            ('agreement', 'Draw by agreement'),
            ('repetition', 'Threefold repetition'),
            ('fifty_move', 'Fifty-move rule'),
            ('abandoned', 'Abandoned'),
        )
    )
    
    # Move history
    move_history = models.TextField(blank=True, default='[]')
    move_count = models.IntegerField(default=0)
    
    # Captured pieces
    captured_pieces = models.TextField(blank=True, default='{"white": [], "black": []}')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['white_player', 'created_at']),
            models.Index(fields=['black_player', 'created_at']),
        ]

    def __str__(self):
        return f"Game {self.code} - {self.status}"
    
    def get_white_display_name(self):
        """Get display name for white player"""
        if self.white_player:
            return self.white_player.username
        return self.white_guest_name or 'Guest'
    
    def get_black_display_name(self):
        """Get display name for black player"""
        if self.black_player:
            return self.black_player.username
        return self.black_guest_name or 'Waiting...'
    
    def mark_started(self):
        """Mark game as started when second player joins"""
        if not self.started_at:
            self.started_at = timezone.now()
            self.last_move_time = timezone.now()
            self.timer_last_updated = timezone.now()
            self.status = 'active'
            self.save()
    
    def mark_completed(self, winner=None, reason=None):
        """Mark game as completed and update player stats"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.winner = winner
        self.result_reason = reason
        self.save()
        
        # Update player statistics if not guest game
        if self.white_player and self.black_player and self.is_rated:
            if winner == 'white':
                self.white_player.update_stats('win')
                self.black_player.update_stats('loss')
            elif winner == 'black':
                self.white_player.update_stats('loss')
                self.black_player.update_stats('win')
            elif winner == 'draw':
                self.white_player.update_stats('draw')
                self.black_player.update_stats('draw')
    
    def get_timer_state(self):
        """
        Get accurate timer state without modifying the database
        This prevents timer from resetting on every poll
        """
        if self.status != 'active' or not self.last_move_time:
            return {
                'white_time': self.white_time_remaining,
                'black_time': self.black_time_remaining,
                'last_updated': self.timer_last_updated.isoformat() if self.timer_last_updated else None
            }
        
        # Calculate elapsed time since last move
        now = timezone.now()
        elapsed = (now - self.last_move_time).total_seconds()
        
        # Determine whose turn it is based on FEN
        current_turn = 'white' if 'w' in self.fen.split()[1] else 'black'
        
        # Calculate current time without saving to database
        white_time = self.white_time_remaining
        black_time = self.black_time_remaining
        
        if current_turn == 'white':
            white_time = max(0, self.white_time_remaining - int(elapsed))
        else:
            black_time = max(0, self.black_time_remaining - int(elapsed))
        
        return {
            'white_time': white_time,
            'black_time': black_time,
            'current_turn': current_turn,
            'last_updated': now.isoformat()
        }
    
    def update_timer_on_move(self):
        """
        Update timer when a move is made (not on every poll)
        This is called only when a move is actually made
        """
        if not self.last_move_time or self.status != 'active':
            self.last_move_time = timezone.now()
            self.timer_last_updated = timezone.now()
            self.save()
            return
        
        now = timezone.now()
        elapsed = (now - self.last_move_time).total_seconds()
        
        # Determine who just moved (opposite of current turn in FEN)
        current_turn_in_fen = 'white' if 'w' in self.fen.split()[1] else 'black'
        player_who_moved = 'black' if current_turn_in_fen == 'white' else 'white'
        
        # Deduct time from player who just moved
        if player_who_moved == 'white':
            self.white_time_remaining = max(0, self.white_time_remaining - int(elapsed))
            if self.white_time_remaining == 0:
                self.mark_completed(winner='black', reason='timeout')
        else:
            self.black_time_remaining = max(0, self.black_time_remaining - int(elapsed))
            if self.black_time_remaining == 0:
                self.mark_completed(winner='white', reason='timeout')
        
        self.last_move_time = now
        self.timer_last_updated = now
        self.save()
    
    def get_time_control_seconds(self):
        """Get initial time in seconds based on time control"""
        time_map = {
            'bullet_1': 60,
            'bullet_2': 120,
            'blitz_3': 180,
            'blitz_5': 300,
            'rapid_10': 600,
            'rapid_15': 900,
            'classical_30': 1800,
            'classical_2_60': 3600,
            'unlimited': 999999,           
        }
        return time_map.get(self.time_control, 300)
    
    def add_captured_piece(self, piece, color):
        """Add a captured piece to the list"""
        try:
            captured = json.loads(self.captured_pieces)
        except:
            captured = {"white": [], "black": []}
        
        captured[color].append(piece)
        self.captured_pieces = json.dumps(captured)
        self.save()


class GameSession(models.Model):
    """Track active game sessions for reconnection"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    color = models.CharField(max_length=5, choices=(('white', 'White'), ('black', 'Black')))
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['user', 'game'], ['session_key', 'game']]
    
    def __str__(self):
        return f"{self.user or 'Guest'} in {self.game.code}"


class Move(models.Model):
    """Store individual moves for analysis and replay"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
    move_number = models.IntegerField()
    player_color = models.CharField(max_length=5)
    move_san = models.CharField(max_length=10)
    move_from = models.CharField(max_length=2)
    move_to = models.CharField(max_length=2)
    captured_piece = models.CharField(max_length=1, blank=True, null=True)
    fen_after = models.CharField(max_length=100)
    time_spent = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['move_number']
    
    def __str__(self):
        return f"{self.game.code} - Move {self.move_number}: {self.move_san}"