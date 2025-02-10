from functools import wraps
from flask import redirect, flash, url_for
from flask_login import current_user

def role_required(*roles):
    """Verifica se o usuário possui um dos papéis permitidos."""
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth_bp.login'))
            if current_user.role not in roles:
                flash('Acesso negado: Permissão insuficiente.', 'error')
                return redirect(url_for('main_bp.menu'))
            return func(*args, **kwargs)
        return decorated_view
    return decorator
