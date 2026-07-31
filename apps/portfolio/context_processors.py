from .models import ProfileInfo, SocialLink

def global_portfolio_context(request):
    """
    Global context processor to make profile info and social links 
    available across all templates automatically.
    """
    profile = ProfileInfo.objects.first()
    social_links = SocialLink.objects.all()
    return {
        'profile': profile,
        'social_links': social_links,
    }
