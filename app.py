from flask import Flask, render_template, session, redirect, url_for, request, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://database_example_1oys_user:hWVuGNzLGF0CESWaoDzsYTs9vKGNTH9a@dpg-cuqdh456l47c73blg5q0-a.oregon-postgres.render.com/database_example_1oys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)

    # Define columns for order items directly in the Order class
    item_names = db.Column(db.Text, nullable=False)  # Store names of items in a comma-separated format
    item_quantities = db.Column(db.Text, nullable=False)  # Store quantities in a comma-separated format
    item_prices = db.Column(db.Text, nullable=False)  # Store item prices in a comma-separated format
    total_prices = db.Column(db.Text, nullable=False)  # Store total prices for each item
    
    # Calculating the total order price can be done programmatically
    def calculate_total(self):
        return sum([float(price) for price in self.total_prices.split(',')])

    def add_item(self, name, quantity, price):
        # Add a new item to the order
        self.item_names += f"{name},"
        self.item_quantities += f"{quantity},"
        self.item_prices += f"{price},"
        self.total_prices += f"{float(quantity) * float(price)},"

@app.route('/submit_order', methods=['POST'])
def submit_order():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    notes = request.form.get('notes')

    # Create a new Order
    new_order = Order(
        full_name=full_name,
        email=email,
        phone=phone,
        address=address,
        notes=notes,
        item_names='',
        item_quantities='',
        item_prices='',
        total_prices=''
    )
    db.session.add(new_order)
    db.session.commit()  # Commit to get the order id for items

    cart = session.get('cart', {})
    for product_id, quantity in cart.items():
        product = next((item for item in products if item["id"] == int(product_id)), None)
        if product:
            # Add item to the order
            new_order.add_item(product["name"], quantity, product["price"])

    db.session.commit()  # Commit to save items in the order

    # Clear the cart after placing the order
    session.pop('cart', None)

    flash("Order placed successfully!", "success")
    return redirect(url_for('index'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        notes = request.form.get('notes')

        # Save to database
        new_order = Order(full_name=full_name, email=email, phone=phone, address=address, notes=notes)
        db.session.add(new_order)
        db.session.commit()

        flash("Order placed successfully!", "success")
        return redirect(url_for('index'))
    return render_template('checkout.html')
# Product Data
products = [
    {
        'id': 1,
        'name': 'Product 1',
        'price': 19.99,
        'image': "https://upload.wikimedia.org/wikipedia/commons/1/17/2014_0531_Cr%C3%A8me_br%C3%BBl%C3%A9e_Doi_Mae_Salong_%28cropped%29.jpg"
    },
    {
        'id': 2,
        'name': 'Product 2',
        'price': 29.99,
        'image': "https://i1.wp.com/www.bharatzkitchen.com/wp-content/uploads/2020/12/EGG-BHAJI-BIRYANI-.jpg?fit=1200%2C675&ssl=1"
    }, 
    {
        'id': 3,
        'name': 'Product 2',
        'price': 29.99,
        'image': "https://www.nehascookbook.com/wp-content/uploads/2022/10/Paneer-bhurji-WS-500x500.jpg"
    },
    {
        'id': 1,
        'name': 'Product 1',
        'price': 19.99,
        'image': "https://upload.wikimedia.org/wikipedia/commons/1/17/2014_0531_Cr%C3%A8me_br%C3%BBl%C3%A9e_Doi_Mae_Salong_%28cropped%29.jpg"
    },
    {
        'id': 2,
        'name': 'Product 2',
        'price': 29.99,
        'image': "https://i1.wp.com/www.bharatzkitchen.com/wp-content/uploads/2020/12/EGG-BHAJI-BIRYANI-.jpg?fit=1200%2C675&ssl=1"
    }, 
    {
        'id': 3,
        'name': 'Product 2',
        'price': 29.99,
        'image': "https://www.nehascookbook.com/wp-content/uploads/2022/10/Paneer-bhurji-WS-500x500.jpg"
    },{
        'id': 1,
        'name': 'Product 1',
        'price': 19.99,
        'image': "https://upload.wikimedia.org/wikipedia/commons/1/17/2014_0531_Cr%C3%A8me_br%C3%BBl%C3%A9e_Doi_Mae_Salong_%28cropped%29.jpg"
    },
    {
        'id': 2,
        'name': 'Product 2',
        'price': 29.99,
        'image': "https://i1.wp.com/www.bharatzkitchen.com/wp-content/uploads/2020/12/EGG-BHAJI-BIRYANI-.jpg?fit=1200%2C675&ssl=1"
    }, 
    {
        'id': 3,
        'name': 'Product 2',
        'price': 29.99,
        'image': "https://www.nehascookbook.com/wp-content/uploads/2022/10/Paneer-bhurji-WS-500x500.jpg"
    },
      {
        'id': 3,
        'name': 'Product 2',
        'price': 29.99,
        'image': "https://www.nehascookbook.com/wp-content/uploads/2022/10/Paneer-bhurji-WS-500x500.jpg"
    }


]
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # Fetch product details using the product_id
    product = next((item for item in products if item['id'] == product_id), None)
    
    # Calculate the total quantity in the cart
    cart_quantity = sum(session.get('cart', {}).values())
    
    # Get the current cart
    cart = session.get('cart', {})
    
    if product:
        # Pass product and cart data to the template
        return render_template('product.html', product=product, cart_quantity=cart_quantity, cart=cart)
    else:
        return "Product not found", 404


# Home Page - Display Products
@app.route('/')
def index():
    cart_quantity = sum(session.get('cart', {}).values())
    cart = session.get('cart', {})  # Count distinct products
    return render_template('index.html', products=products, cart_quantity=cart_quantity, user=current_user,cart=cart)

def login_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please login first", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Add to Cart (Using AJAX)
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        # Get the cart from the session, or initialize it if it doesn't exist
        cart = session.get('cart', {})

        # If the product is already in the cart, increment the quantity; otherwise, add it
        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        # Save the updated cart back to the session
        session['cart'] = cart

        # Calculate the total quantity of items in the cart (including duplicates)
        cart_quantity = sum(cart.values())

        # Return the updated cart quantity (total number of items)
        return jsonify({'success': True, 'cart_quantity': cart_quantity})
    return jsonify({'success': False, 'message': 'Product not found'}), 404

# Cart Page
@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    cart_quantity = sum(session.get('cart', {}).values())
    for product_id, quantity in cart.items():
        product = next((item for item in products if item["id"] == int(product_id)), None)
        if product:
            product['quantity'] = quantity
            product['total_price'] = product['price'] * quantity
            total_price += product['total_price']
            cart_items.append(product)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price, user=current_user, cart_quantity=cart_quantity)

# Increase Quantity
@app.route('/increase_quantity/<int:product_id>', methods=['POST'])
def increase_quantity(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    session['cart'] = cart
    return redirect(url_for('cart'))

# Decrease Quantity
@app.route('/decrease_quantity/<int:product_id>', methods=['POST'])
def decrease_quantity(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
    session['cart'] = cart
    return redirect(url_for('cart'))

# Remove from Cart
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    session['cart'] = cart
    return redirect(url_for('cart'))
# Display Peep Page

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)  # Auto-login after signup
        return redirect(url_for("index"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid email or password", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



if __name__ == '__main__':
    with app.app_context():
         # Drop all tables in the database
        db.create_all()
  
    app.run(debug=True)  
