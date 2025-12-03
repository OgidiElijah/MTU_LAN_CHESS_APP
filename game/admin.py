from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Game, GameSession, Move

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with MTU fields"""
    list_display = ['username', 'matric_number', 'department', 'level', 'rating', 'total_games', 'wins']
    list_filter = ['department', 'level', 'date_joined']
    search_fields = ['username', 'matric_number', 'email', 'first_name', 'last_name']
    ordering = ['-rating']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('MTU Information', {
            'fields': ('matric_number', 'department', 'level', 'bio', 'avatar')
        }),
        ('Game Statistics', {
            'fields': ('total_games', 'wins', 'losses', 'draws', 'rating')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('MTU Information', {
            'fields': ('matric_number', 'department', 'level')
        }),
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Game administration"""
    list_display = ['code', 'status', 'get_white_name', 'get_black_name', 'time_control', 'winner', 'created_at']
    list_filter = ['status', 'time_control', 'is_rated', 'created_at']
    search_fields = ['code', 'white_player__username', 'black_player__username']
    readonly_fields = ['code', 'created_at', 'updated_at', 'started_at', 'completed_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Game Information', {
            'fields': ('code', 'status', 'fen', 'move_count')
        }),
        ('Players', {
            'fields': ('white_player', 'white_guest_name', 'black_player', 'black_guest_name')
        }),
        ('Settings', {
            'fields': ('time_control', 'is_rated', 'is_private')
        }),
        ('Timer', {
            'fields': ('white_time_remaining', 'black_time_remaining', 'last_move_time')
        }),
        ('Result', {
            'fields': ('winner', 'result_reason')
        }),
        ('Game Data', {
            'fields': ('move_history', 'captured_pieces'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_white_name(self, obj):
        return obj.get_white_display_name()
    get_white_name.short_description = 'White Player'
    
    def get_black_name(self, obj):
        return obj.get_black_display_name()
    get_black_name.short_description = 'Black Player'


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    """Game session tracking for reconnection"""
    list_display = ['user', 'game', 'color', 'last_seen', 'is_active']
    list_filter = ['color', 'last_seen']
    search_fields = ['user__username', 'game__code']
    readonly_fields = ['last_seen']
    
    def is_active(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        return obj.last_seen > timezone.now() - timedelta(minutes=5)
    is_active.boolean = True
    is_active.short_description = 'Active'


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    """Individual move tracking"""
    list_display = ['game', 'move_number', 'player_color', 'move_san', 'captured_piece', 'time_spent', 'timestamp']
    list_filter = ['player_color', 'timestamp']
    search_fields = ['game__code', 'move_san']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('game')
