from getpass import getpass
import sys
from webapp import create_app
from webapp.model import db, User

app = create_app()

with app.app_context():
    username = input('enter username: ')
    if User.query.filter(User.username == username).count():
        print('такой пользователь уже есть')
        sys.exit()

    password1 = getpass('ввeдите пароль: ')
    password2 = getpass('еще раз пароль: ')
    
    if not password1 == password2:
        print('Пароли не совпадают')
        sys.exit()

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print(f'Пользователь {new_user.username} успешно создан!')
    # sys.exit()
