from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(text):
    """
    Convert markdown text to HTML.
    """
    if not text:
        return ''
    
    # Configure markdown with common extensions
    extensions = [
        'extra',  # Adds tables, fenced code blocks, etc.
        'nl2br',  # Convert newlines to <br>
    ]
    
    # Add codehilite if pygments is available (optional)
    try:
        import pygments
        extensions.append('codehilite')
    except ImportError:
        pass
    
    md = markdown.Markdown(extensions=extensions)
    html = md.convert(text)
    return mark_safe(html)


@register.filter(name='markdown_safe')
def markdown_safe_filter(text):
    """
    Convert markdown text to HTML (safe for use in templates).
    This is an alias for the markdown filter.
    """
    return markdown_filter(text)
