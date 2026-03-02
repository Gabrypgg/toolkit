import re

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    if not url:
        return None
    
    # (?:...) is a non-capturing group — it groups the alternatives without capturing them
    # v= matches URLs like: https://www.youtube.com/watch?v=VIDEO_ID
    # youtu\.be/ matches shortened URLs like: https://youtu.be/VIDEO_ID
    # | means “or”
    # ([a-zA-Z0-9_-]{11}) is a capturing group — it matches and saves the actual YouTube video ID
    # [a-zA-Z0-9_-] means it matches any letter (upper/lower), digit, underscore _, or dash -
    # {11} means it matches exactly 11 characters — which is the standard length of a YouTube video ID

    patterns = [
        r"(?:v=|youtu\.be/|embed/|v/|shorts/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$" # Direct ID
    ]   
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
            
    return None

def sanitize_filename(filename):
    """
    Sanitize a string to be a valid filename.
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)
