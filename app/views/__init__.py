from app import myapp


@myapp.route('/')
def home():
    return "Welcome to office management system"
