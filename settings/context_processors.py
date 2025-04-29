from .models import Settings

def settings_processor(request):
    """
    Context processor to make settings available in all templates
    """
    try:
        settings = Settings.get_settings()
    except:
        # If the settings table doesn't exist yet (before migrations)
        # or there are other errors, return an empty dict
        return {}
    
    return {
        'site_settings': settings
    }