from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db.models import Q, Count
import json

from .models import User, Game, GameSession, Move, START_FEN


# ============================================
# HOME & LANDING PAGES
# ============================================

def home(request):
    """Landing page for MTU Chess Club"""
    total_games = Game.objects.count()
    active_games = Game.objects.filter(status='active').count()
    total_users = User.objects.count()
    
    # Top players by rating
    top_players = User.objects.filter(rating__isnull=False).order_by('-rating')[:5]
    
    # Recent completed games
    recent_games = Game.objects.filter(status='completed').order_by('-completed_at')[:5]
    
    context = {
        'total_games': total_games,
        'active_games': active_games,
        'total_users': total_users,
        'top_players': top_players,
        'recent_games': recent_games,
    }
    return render(request, 'game/home.html', context)


# ============================================
# AUTHENTICATION VIEWS
# ============================================

def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        matric_number = request.POST.get('matric_number').upper()  # Uppercase for consistency
        department = request.POST.get('department')
        level = request.POST.get('level')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'game/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return render(request, 'game/register.html')
        
        if User.objects.filter(matric_number=matric_number).exists():
            messages.error(request, 'Matric number already registered!')
            return render(request, 'game/register.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                matric_number=matric_number,
                department=department,
                level=level,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
            )
            
            # Log user in
            login(request, user)
            messages.success(request, f'Welcome to MTU Chess Club, {username}!')
            return redirect('dashboard')
        
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'game/register.html')
    
    return render(request, 'game/register.html')


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'game/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    # messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    
    # Get user's recent games
    user_games = Game.objects.filter(
        Q(white_player=user) | Q(black_player=user)
    ).order_by('-created_at')[:5]
    
    # Get active games to watch
    active_games = Game.objects.filter(status='active').exclude(
        Q(white_player=user) | Q(black_player=user)
    ).order_by('-started_at')[:5]
    
    context = {
        'user': user,
        'user_games': user_games,
        'active_games': active_games,
        'win_rate': user.win_rate,
        'rating_progress': min(100, (user.total_games / 5) * 100),
    }
    return render(request, 'game/dashboard.html', context)


def guest_mode(request):
    """Guest mode - watch only"""
    active_games = Game.objects.filter(status='active').order_by('-started_at')[:20]
    
    context = {
        'active_games': active_games,
        'is_guest': True,
    }
    return render(request, 'game/guest.html', context)


# ============================================
# GAME VIEWS
# ============================================

@login_required
def play(request):
    """Play page for authenticated users"""
    return render(request, 'game/play.html')


def watch_game(request, code):
    """Watch a game (for guests)"""
    game = get_object_or_404(Game, code=code.upper())
    
    context = {
        'game': game,
        'is_spectator': True,
    }
    return render(request, 'game/watch.html', context)


def tournament(request):
    """Tournament dashboard"""
    games = Game.objects.all()[:50]
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        games = games.filter(status=status_filter)
    
    context = {
        'games': games,
        'status_filter': status_filter,
    }
    return render(request, 'game/tournament.html', context)


def leaderboard(request):
    """Leaderboard page"""
    players = User.objects.filter(rating__isnull=False).order_by('-rating')[:50]
    
    context = {
        'players': players,
    }
    return render(request, 'game/leaderboard.html', context)


# ============================================
# API ENDPOINTS
# ============================================

@csrf_exempt
@require_http_methods(["POST"])
def api_create_game(request):
    """Create a new game"""
    try:
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        
        # Generate unique code
        code = get_random_string(6).upper()
        while Game.objects.filter(code=code).exists():
            code = get_random_string(6).upper()
        
        # Get time control
        time_control = data.get('time_control', 'blitz_5')
        is_rated = data.get('is_rated', True)
        
        # Create game
        game = Game.objects.create(
            code=code,
            fen=START_FEN,
            status='waiting',
            time_control=time_control,
            is_rated=is_rated,
        )
        
        # Set initial time
        initial_time = game.get_time_control_seconds()
        game.white_time_remaining = initial_time
        game.black_time_remaining = initial_time
        
        # Assign player
        if request.user.is_authenticated:
            game.white_player = request.user
        else:
            game.white_guest_name = data.get('player_name', 'Guest')
        
        game.save()
        
        # Create session
        if request.user.is_authenticated:
            GameSession.objects.create(
                user=request.user,
                game=game,
                session_key=request.session.session_key or 'guest',
                color='white'
            )
        
        return JsonResponse({
            'success': True,
            'code': game.code,
            'fen': game.fen,
            'status': game.status,
            'white_time': game.white_time_remaining,
            'black_time': game.black_time_remaining,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def api_game_state(request, code):
    """
    CRITICAL FIX: Get current game state WITHOUT modifying database
    This prevents timer from resetting on every poll
    """
    try:
        game = Game.objects.get(code=code.upper())
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    # Get timer state WITHOUT saving to database
    timer_state = game.get_timer_state()
    
    return JsonResponse({
        'code': game.code,
        'fen': game.fen,
        'status': game.status,
        'white_player': game.get_white_display_name(),
        'black_player': game.get_black_display_name(),
        'white_time': timer_state['white_time'],
        'black_time': timer_state['black_time'],
        'winner': game.winner,
        'result_reason': game.result_reason,
        'move_history': game.move_history,
        'move_count': game.move_count,
        'captured_pieces': game.captured_pieces,
        'updated_at': game.updated_at.isoformat(),
        'timer_last_updated': timer_state.get('last_updated'),
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_game_move(request, code):
    """Submit a move"""
    try:
        game = Game.objects.get(code=code.upper())
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    fen = data.get('fen')
    if not fen:
        return JsonResponse({'error': 'fen is required'}, status=400)
    
    # Update game state
    game.fen = fen
    game.move_count += 1
    
    # Update move history
    move_san = data.get('move_san')
    if move_san:
        try:
            history = json.loads(game.move_history) if game.move_history else []
            history.append(move_san)
            game.move_history = json.dumps(history)
        except:
            pass
    
    # Handle captured piece
    captured = data.get('captured')
    if captured:
        captured_color = captured.get('color')
        captured_piece = captured.get('piece')
        if captured_color and captured_piece:
            game.add_captured_piece(captured_piece, captured_color)
    
    # CRITICAL FIX: Update timer only when move is made
    game.update_timer_on_move()
    
    # Check for game end
    game_over = data.get('game_over', False)
    if game_over:
        winner = data.get('winner')
        reason = data.get('reason')
        game.mark_completed(winner=winner, reason=reason)
    
    game.save()
    
    # Return updated timer state
    timer_state = game.get_timer_state()
    
    return JsonResponse({
        'success': True,
        'white_time': timer_state['white_time'],
        'black_time': timer_state['black_time'],
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_join_game(request, code):
    """Join an existing game"""
    try:
        game = Game.objects.get(code=code.upper())
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    if game.status != 'waiting':
        return JsonResponse({'error': 'Game already has two players'}, status=400)
    
    try:
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
        
        # Assign player
        if request.user.is_authenticated:
            game.black_player = request.user
        else:
            game.black_guest_name = data.get('player_name', 'Guest')
        
        game.mark_started()
        
        # Create session
        if request.user.is_authenticated:
            GameSession.objects.create(
                user=request.user,
                game=game,
                session_key=request.session.session_key or 'guest',
                color='black'
            )
        
        return JsonResponse({
            'success': True,
            'code': game.code,
            'fen': game.fen,
            'status': game.status,
            'white_player': game.get_white_display_name(),
            'black_player': game.get_black_display_name(),
            'white_time': game.white_time_remaining,
            'black_time': game.black_time_remaining,
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_resign(request, code):
    """Resign from a game"""
    try:
        game = Game.objects.get(code=code.upper())
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    data = json.loads(request.body.decode('utf-8'))
    color = data.get('color')
    
    if color == 'white':
        game.mark_completed(winner='black', reason='resignation')
    else:
        game.mark_completed(winner='white', reason='resignation')
    
    return JsonResponse({'success': True})


@csrf_exempt
@require_http_methods(["POST"])
def api_offer_draw(request, code):
    """Offer or accept a draw"""
    try:
        game = Game.objects.get(code=code.upper())
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    data = json.loads(request.body.decode('utf-8'))
    action = data.get('action')
    
    if action == 'accept':
        game.mark_completed(winner='draw', reason='agreement')
        return JsonResponse({'success': True, 'draw_accepted': True})
    
    return JsonResponse({'success': True, 'draw_offered': True})


@require_http_methods(["GET"])
def api_check_session(request, code):
    """Check if user has an active session in this game"""
    try:
        game = Game.objects.get(code=code.upper())
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    
    if not request.user.is_authenticated:
        return JsonResponse({'has_session': False})
    
    try:
        session = GameSession.objects.get(user=request.user, game=game)
        return JsonResponse({
            'has_session': True,
            'color': session.color,
        })
    except GameSession.DoesNotExist:
        return JsonResponse({'has_session': False})