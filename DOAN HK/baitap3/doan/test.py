'''
from flask import Flask, render_template, request, redirect, url_for, session
import locale

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thay đổi secret key để bảo mật

# Đặt định dạng địa phương cho VN
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

def number_format(value, decimal_places=0, decimal_point=',', thousands_sep='.'):
    """Định dạng số thành chuỗi theo kiểu VN."""
    if value is None:
        return ''
    formatted_value = f"{value:,.{decimal_places}f}".replace(',', 'X').replace('.', decimal_point).replace('X', thousands_sep)
    return formatted_value

products = [
    {"id": 1, "name": "Quần xám", "price": 300000},
    {"id": 2, "name": "Quần đen", "price": 300000},
    {"id": 3, "name": "Giày đen", "price": 350000},
]

@app.route('/')
def index():
    # Đếm tổng số lượng sản phẩm trong giỏ hàng
    cart_items = session.get('cart', [])
    cart_count = sum(item.get('quantity', 0) for item in cart_items)  # Đếm tổng số lượng sản phẩm
    return render_template('index.html', products=products, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        existing_product = next((item for item in session['cart'] if item['id'] == product_id), None)
        if existing_product:
            existing_product['quantity'] += 1  # Tăng số lượng nếu sản phẩm đã có
        else:
            product_with_quantity = product.copy()
            product_with_quantity['quantity'] = 1  # Khởi tạo số lượng là 1
            session['cart'].append(product_with_quantity)
        session.modified = True
    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        for item in session.get('cart', []):
            quantity = request.form.get(f'quantity_{item["id"]}', 1)
            item['quantity'] = int(quantity) if quantity.isdigit() and int(quantity) > 0 else 1

    cart_items = session.get('cart', [])
    total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Xử lý thông tin thanh toán
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        district = request.form.get('district')
        ward = request.form.get('ward')
        city = request.form.get('city')

        # Có thể làm gì đó với thông tin này, như lưu vào cơ sở dữ liệu

        # Chuyển hướng đến trang chọn phương thức thanh toán
        return redirect(url_for('payment'))

    return render_template('checkout.html')  # Trả về trang thanh toán

@app.route('/payment')
def payment():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)  # Tính tổng tiền
    return render_template('payment.html', cart=cart_items, total=total)  # Trả về trang chọn phương thức thanh toán

# Đăng ký hàm định dạng với Jinja2
app.jinja_env.filters['number_format'] = number_format

if __name__ == '__main__':
    app.run(debug=True)





from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import locale

app = Flask(__name__, 
    static_folder='static',
    template_folder='templates')
    
app.secret_key = 'your_secret_key'

# Cấu hình PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:liemlam159@localhost:5432/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Đặt định dạng địa phương cho VN
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

# Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(100))
    ward = db.Column(db.String(100))
    city = db.Column(db.String(100))
    total_amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

def number_format(value, decimal_places=0, decimal_point=',', thousands_sep='.'):
    if value is None:
        return ''
    formatted_value = f"{value:,.{decimal_places}f}".replace(',', 'X').replace('.', decimal_point).replace('X', thousands_sep)
    return formatted_value

@app.route('/')
def index():
    try:
        # Lấy sản phẩm từ database
        products = Product.query.all()
        cart_items = session.get('cart', [])
        cart_count = sum(item.get('quantity', 0) for item in cart_items)
        return render_template('index.html', products=products, cart_count=cart_count)
    except Exception as e:
        print(f"Lỗi khi truy cập trang chủ: {e}")
        return "Có lỗi xảy ra khi tải trang", 500

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        if 'cart' not in session:
            session['cart'] = []
        
        existing_product = next((item for item in session['cart'] if item['id'] == product_id), None)
        if existing_product:
            existing_product['quantity'] += 1
        else:
            session['cart'].append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': 1
            })
        session.modified = True
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Lỗi khi thêm vào giỏ hàng: {e}")
        return "Có lỗi xảy ra", 500

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    try:
        if request.method == 'POST':
            for item in session.get('cart', []):
                quantity = request.form.get(f'quantity_{item["id"]}', 1)
                item['quantity'] = int(quantity) if quantity.isdigit() and int(quantity) > 0 else 1

        cart_items = session.get('cart', [])
        total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
        return render_template('cart.html', cart=cart_items, total=total)
    except Exception as e:
        print(f"Lỗi khi xem giỏ hàng: {e}")
        return "Có lỗi xảy ra", 500

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    try:
        if 'cart' in session:
            session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
            session.modified = True
        return redirect(url_for('cart'))
    except Exception as e:
        print(f"Lỗi khi xóa sản phẩm khỏi giỏ hàng: {e}")
        return "Có lỗi xảy ra", 500

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    try:
        if request.method == 'POST':
            cart_items = session.get('cart', [])
            total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
            
            order = Order(
                name=request.form.get('name'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                address=request.form.get('address'),
                district=request.form.get('district'),
                ward=request.form.get('ward'),
                city=request.form.get('city'),
                total_amount=total
            )
            db.session.add(order)
            db.session.flush()

            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['id'],
                    quantity=item['quantity'],
                    price=item['price']
                )
                db.session.add(order_item)
            
            db.session.commit()
            session['cart'] = []
            return redirect(url_for('payment'))
            
        return render_template('checkout.html')
    except Exception as e:
        print(f"Lỗi khi thanh toán: {e}")
        db.session.rollback()
        return "Có lỗi xảy ra khi xử lý đơn hàng", 500

@app.route('/payment')
def payment():
    try:
        cart_items = session.get('cart', [])
        total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
        return render_template('payment.html', cart=cart_items, total=total)
    except Exception as e:
        print(f"Lỗi khi hiển thị trang thanh toán: {e}")
        return "Có lỗi xảy ra", 500

# Đăng ký hàm định dạng với Jinja2
app.jinja_env.filters['number_format'] = number_format

# Khởi tạo database và thêm dữ liệu mẫu
def init_db():
    with app.app_context():
        # Tạo tất cả bảng
        db.create_all()
        
        # Kiểm tra xem đã có dữ liệu mẫu chưa
        if not Product.query.first():
            # Thêm dữ liệu mẫu
            products = [
                Product(name="Quần xám", price=300000),
                Product(name="Quần đen", price=300000),
                Product(name="Giày đen", price=350000),
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("Đã khởi tạo database và thêm dữ liệu mẫu!")
        else:
            print("Database đã có dữ liệu!")

if __name__ == '__main__':
    init_db()  # Khởi tạo database khi chạy app
    app.run(debug=True)
'''




from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import locale

test = Flask(__name__,
            static_folder='static',
            template_folder='templates')

test.secret_key = 'your_secret_key'

# Cấu hình PostgreSQL
test.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:liemlam159@localhost:5432/my_database'
test.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(test)

# Đặt định dạng địa phương cho VN
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

# Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=True)  # nếu bạn cần lưu email
    full_name = db.Column(db.String(100), nullable=True)  # nếu bạn cần lưu tên đầy đủ
    phone = db.Column(db.String(15), nullable=True)  # nếu bạn cần lưu số điện thoại
    
class UserLogin(db.Model):
    __tablename__ = 'users_login'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(100))
    ward = db.Column(db.String(100))
    city = db.Column(db.String(100))
    total_amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

@test.cli.command("add_products")
def add_products():
    # Tạo dữ liệu cho sản phẩm
    giay_den = Product(
        name='Giày Đen',
        price=300000,
        description='Giày đen thời trang và thoải mái.',
        image_file='giày_đen.jpg'
    )

    quan_den = Product(
        name='Quần Đen',
        price=300000,
        description='Quần đen đẹp cho mọi dịp.',
        image_file='quần_đen.jpg'
    )

    quan_xam = Product(
        name='Quần Xám',
        price=300000,
        description='Quần xám thời trang.',
        image_file='quần_xám.jpg'
    )

    # Thêm sản phẩm vào cơ sở dữ liệu
    db.create_all()  # Tạo bảng nếu chưa có
    db.session.add(giay_den)
    db.session.add(quan_den)
    db.session.add(quan_xam)
    db.session.commit()

    print("Sản phẩm đã được thêm thành công!")

def init_db():
    with test.app_context():
        db.create_all()
        if 'last_login' not in [column.name for column in UserLogin.__table__.columns]:
            db.engine.execute('ALTER TABLE users_login ADD COLUMN last_login TIMESTAMP DEFAULT NOW()')
        if not Product.query.first():
            products = [
                Product(name="Quần xám", price=300000),
                Product(name="Quần đen", price=300000),
                Product(name="Giày đen", price=350000),
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()
            print("Database đã được khởi tạo và thêm dữ liệu mẫu!")

@test.route('/')
def index():
    products = Product.query.all()
    cart_items = session.get('cart', [])
    cart_count = sum(item.get('quantity', 0) for item in cart_items)
    
    username = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            username = user.username 

    return render_template('index.html', products=products, cart_count=cart_count)

@test.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@test.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if 'cart' not in session:
        session['cart'] = []
    existing_product = next((item for item in session['cart'] if item['id'] == product_id), None)
    if existing_product:
        existing_product['quantity'] += 1
    else:
        session['cart'].append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1
        })
    session.modified = True
    return redirect(url_for('index'))

@test.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['fullName']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

    # Kiểm tra xem email đã tồn tại chưa
        existing_email = db.session.query(User).filter_by(email=email).first()
        if existing_email:
            return "Email đã tồn tại, vui lòng chọn một email khác", 409  # Điều này sẽ trả về mã lỗi 409 cho email đã tồn tại

        # Kiểm tra xem tên người dùng đã tồn tại chưa
        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user:
            return "Tên người dùng đã tồn tại, vui lòng chọn một username khác", 409  # Điều này sẽ trả về mã lỗi 409 cho username đã tồn tại

        new_user = User(
            username=username,
            password=hashed_password,
            email=email,
            full_name=full_name,
            phone=phone
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('thank_you'))

    return render_template('register.html')

@test.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@test.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            user_login = UserLogin.query.filter_by(username=username).first()
            if user_login:
                # Update last login time for existing user
                user_login.last_login = datetime.utcnow()
            else:
                # Create new UserLogin entry if not exists
                hashed_password = user.password  # Use the existing hashed password
                user_login = UserLogin(
                    username=username, 
                    password=hashed_password,
                    last_login=datetime.utcnow()
                )
                db.session.add(user_login)
            
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "Tên đăng nhập hoặc mật khẩu không đúng.", 401
    return render_template('login.html')  # Trả về form đăng nhập

@test.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@test.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@test.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
    return redirect(url_for('cart'))

@test.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        cart_items = session.get('cart', [])
        total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
        order = Order(
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            district=request.form.get('district'),
            ward=request.form.get('ward'),
            city=request.form.get('city'),
            total_amount=total
        )
        db.session.add(order)
        db.session.flush()
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['id'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        db.session.commit()
        session['cart'] = []
        return redirect(url_for('index'))
    return render_template('checkout.html')

# Định nghĩa hàm number_format
def number_format(value, decimal_places=0, decimal_point=',', thousands_sep='.'):
    if value is None:
        return ''
    formatted_value = f"{value:,.{decimal_places}f}".replace(',', 'X').replace('.', decimal_point).replace('X', thousands_sep)
    return formatted_value

# Đăng ký bộ lọc với môi trường Jinja2
test.jinja_env.filters['number_format'] = number_format

if __name__ == '__main__':
    init_db()
    test.run(debug=True)
