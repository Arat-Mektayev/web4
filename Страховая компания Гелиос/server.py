import os
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_cors import CORS  # Импортируем CORS
CORS(app)  # Разрешаем все запросы с любых источников

# Функция загрузки пользователя


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.route('/')
def index():
    page = request.args.get('page', 'first')
    print(current_user)
    if isinstance(current_user, AnonymousUserMixin):
        return render_template('index.html', page=page, name='')
    return render_template('index.html', page=page, name=current_user.username)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/first')
def first():
    return render_template('first.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/licenses')
def licenses():
    return render_template('licenses.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/product')
def product():
    p = request.args['p']
    return render_template('product.html', p=p)


@app.route('/json_prod')
def json_prod():
    p = request.args['p']
    prod = Prod.query.filter(Prod.name == p).first()
    prod_dict = prod.__dict__
    prod_dict.pop('_sa_instance_state', None)

    return jsonify(prod_dict)


@app.route('/json_prod_cases')
def json_prod_cases():
    p_id = request.args['p_id']
    if p_id:
        cases = Case.query.filter(Case.prod_id == p_id).all()
        print(cases)
        cases_list = [case.__dict__ for case in cases]

        # Убираем SQLAlchemy-specific поля (например, _sa_instance_state)
        for case in cases_list:
            case.pop('_sa_instance_state', None)
        return jsonify(cases_list)


@app.route('/category')
def category():
    tag = request.args['tag']
    return render_template('category.html', tag=tag)


@app.route('/json_prods')
def json_prods():
    tag = request.args['tag']
    if tag == '0':
        prods = Prod.query.all()
    else:
        prods = Prod.query.filter(Prod.tag == tag).all()
    # Преобразуем объекты в список словарей с помощью __dict__
    prods_list = [prod.__dict__ for prod in prods]

    # Убираем SQLAlchemy-specific поля (например, _sa_instance_state)
    for prod in prods_list:
        prod.pop('_sa_instance_state', None)
    print(prods_list)
    return jsonify(prods_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {"message": 'Вы успешно вошли в систему!',
                "name": '',
                "status": '1'}

        email = request.form['email']
        password = request.form['password']

        # Проверка, что пароли совпадают
        user = User.query.filter((User.email == email)).first()
        # print(user)
        if not user:
            data["message"] = 'Пользователя с таким адресом эл. почты не существует'
            return jsonify(data)

        if not check_password_hash(user.password, password):
            data["message"] = 'Неправильный пароль или адрес эл. почты'
            return jsonify(data)

        data["status"] = '0'
        data["name"] = user.username
        return jsonify(data)  # Направляем на страницу входа

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        data = {"message": 'Регистрация успешна! Пожалуйста, войдите в систему.',
                "status": 1}

        # Проверка, что пользователь с таким email или телефоном не существует
        existing_user = User.query.filter((User.email == email) | (User.phone == phone)).first()
        if existing_user:
            data["message"] = 'Пользователь с таким номером телефона или email уже существует'
            return jsonify(data)

        # Хеширование пароля перед сохранением в базе данных
        hashed_password = generate_password_hash(password, method='pbkdf2:sha1')
        # Создание нового пользователя
        new_user = User(username=username, phone=phone, email=email, password=hashed_password)
        # Добавление пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()

        data["status"] = 0
        return jsonify(data)  # Направляем на страницу входа

    return render_template('register.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        data = {"message": 'Форма успешно отправлена!'}

        post = request.get_json()

        name = post.get('name')
        email = post.get('email')
        text = post.get('text')

        feedback = Feedback(name=name, email=email, text=text)
        db.session.add(feedback)
        db.session.commit()
        return jsonify(data)

    return render_template('feedback.html')


if __name__ == '__main__':
    # print('asd@asd.asd')
    app.run()
