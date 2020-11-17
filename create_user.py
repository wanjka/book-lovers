from getpass import getpass
import sys
from app import create_app
from app.db import db
from app.models import User

app = create_app()
with app.app_context():
    username = input('Type user name: ')
    if User.query.filter(User.username == username).count():
        print(f'Error: User with name {username} already exists')
        sys.exit(0)

    password = getpass('Type your password: ')
    password_repeat = getpass('Type your password again: ')
    if password != password_repeat:
        print('Error: Passwords don\'t match')
        sys.exit(1)

    r = input('Choose new user role ([1] for admin, default for common user): ')
    try:
        role = 'admin' if int(r) == 1 else 'user'
    except ValueError:
        role = 'user'

    default_email = f'{username}@example.com'
    new_user = User(username=username, role=role, email=default_email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    print()
    print('Added user {new_user.username} '
         f'(role: {new_user.role}) with id {new_user.id}')
    print(f'The new user was given a default email address: {new_user.email}. '
           'If you want, you can change this in your profile settings')
