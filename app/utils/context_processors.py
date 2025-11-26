from datetime import datetime
from flask import current_app, g, request, session
from flask_login import current_user
from babel.dates import format_date, format_datetime, format_time
from babel.numbers import format_currency, format_decimal, format_percent
import pytz

def inject_now():
    """Inject current datetime into all templates."""
    return {'now': datetime.utcnow()}

def inject_user():
    """Inject user-related variables into all templates."""
    return {
        'current_user': current_user,
        'user_avatar': get_user_avatar_url(),
        'user_timezone': get_user_timezone(),
        'user_currency': get_user_currency(),
    }

def format_currency(amount, currency=None, format=None, locale=None):
    """
    Format a number as a currency.
    
    Args:
        amount: The amount to format
        currency: ISO 4217 currency code (defaults to user's preferred currency)
        format: Custom format string
        locale: Locale to use for formatting (defaults to user's preferred locale)
    
    """

    
    
    
    if amount is None:
        return ''
        
    if currency is None:
        currency = getattr(g, 'currency', 'USD')
        
    if locale is None:
        locale = get_locale()
    
    try:
        return format_currency(amount, currency, format=format, locale=locale)
    except Exception as e:
        current_app.logger.error(f"Error formatting currency: {e}")
        return f"{currency} {amount:.2f}"  # Fallback format

def format_date_filter(date, format='medium', locale=None):
    """Format a date using Babel."""
    
    
    if date is None:
        return ''
    if locale is None:
        locale = get_locale()
    return format_date(date, format=format, locale=locale)

def format_datetime_filter(datetime_obj, format='medium', timezone=None, locale=None):

    """Format a datetime using Babel."""



    if datetime_obj is None:
        return ''
        
    if timezone is None:
        timezone = get_user_timezone()
    
    if locale is None:
        locale = get_locale()
    
    # Convert naive datetime to timezone-aware if needed
    if datetime_obj.tzinfo is None:
        datetime_obj = pytz.utc.localize(datetime_obj)
    
    # Convert to user's timezone
    datetime_obj = datetime_obj.astimezone(timezone)
    
    return format_datetime(datetime_obj, format=format, locale=locale)

def format_time_filter(time_obj, format='short', timezone=None, locale=None):
    """Format a time using Babel."""
    if time_obj is None:
        return ''
        
    if timezone is None:
        timezone = get_user_timezone()
    
    if locale is None:
        locale = get_locale()
    
    # Handle both time and datetime objects
    if hasattr(time_obj, 'tzinfo') and time_obj.tzinfo is not None:
        # Already timezone-aware, convert to user's timezone
        time_obj = time_obj.astimezone(timezone)
    else:
        # Naive time, assume it's in UTC and localize
        time_obj = pytz.utc.localize(datetime.combine(datetime.utcnow().date(), time_obj))
        time_obj = time_obj.astimezone(timezone)
    
    return format_time(time_obj, format=format, locale=locale)

def format_number_filter(number, format=None, locale=None):
    """Format a number using Babel."""
    if number is None:
        return ''
    if locale is None:
        locale = get_locale()
    return format_decimal(number, format=format, locale=locale)

def format_percent_filter(number, format=None, locale=None):
    """Format a number as a percentage using Babel."""
    if number is None:
        return ''
    if locale is None:
        locale = get_locale()
    return format_percent(number, format=format, locale=locale)

def get_locale():
    """Get the current locale from the session or user preferences."""
    # First check if locale is set in the session
    if 'language' in session:
        return session['language']
    
    # Then check if user is logged in and has a preferred locale
    if current_user.is_authenticated and hasattr(current_user, 'locale') and current_user.locale:
        return current_user.locale
    
    # Fall back to the application's default locale
    return current_app.config.get('BABEL_DEFAULT_LOCALE', 'en')

def get_user_timezone():
    """Get the current user's timezone."""
    # First check if timezone is set in the session
    if 'timezone' in session:
        try:
            return pytz.timezone(session['timezone'])
        except pytz.UnknownTimeZoneError:
            pass
    
    # Then check if user is logged in and has a preferred timezone
    if current_user.is_authenticated and hasattr(current_user, 'timezone') and current_user.timezone:
        try:
            return pytz.timezone(current_user.timezone)
        except pytz.UnknownTimeZoneError:
            pass
    
    # Fall back to the application's default timezone
    return pytz.timezone(current_app.config.get('BABEL_DEFAULT_TIMEZONE', 'UTC'))

def get_user_currency():
    """Get the current user's preferred currency."""
    # First check if currency is set in the session
    if 'currency' in session:
        return session['currency']
    
    # Then check if user is logged in and has a preferred currency
    if current_user.is_authenticated and hasattr(current_user, 'currency') and current_user.currency:
        return current_user.currency
    
    # Fall back to the application's default currency
    return current_app.config.get('DEFAULT_CURRENCY', 'USD')

def get_user_avatar_url(user=None):
    """Get the URL for the user's avatar."""
    if user is None:
        user = current_user
    
    if not user.is_authenticated:
        return url_for('static', filename='images/default-avatar.png')
    
    # Check if user has a custom avatar
    if hasattr(user, 'avatar') and user.avatar:
        return url_for('uploads.uploaded_file', filename=user.avatar)
    
    # Fall back to Gravatar or default avatar
    email_hash = hashlib.md5(user.email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=200"

def register_template_filters(app):
    """Register all template filters."""
    app.jinja_env.filters['date'] = format_date_filter
    app.jinja_env.filters['datetime'] = format_datetime_filter
    app.jinja_env.filters['time'] = format_time_filter
    app.jinja_env.filters['number'] = format_number_filter
    app.jinja_env.filters['percent'] = format_percent_filter
    app.jinja_env.filters['currency'] = format_currency
