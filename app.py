from flask import Flask, render_template, session, redirect, url_for, request, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
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
        'name': 'Manga Miniature - Naruto',
        'price': 24.99,
        'image': "https://rukminim2.flixcart.com/image/850/1000/ku5ufm80/action-figure/v/d/r/3-naruto-action-figure-miniature-doll-toy-figure-limited-edition-original-imag7cbgkhcd3zmm.jpeg?q=20&crop=false",
        'description': "Naruto Uzumaki, a mischievous ninja, dreams of becoming Hokage, the strongest ninja leader. With the Nine-Tails Fox sealed inside him, he faces rejection but never gives up. Join him on his journey filled with friendships, epic battles, and self-discovery."
    },
    {
        'id': 2,
        'name': 'One Piece - Volume 1',
        'price': 19.99,
        'image': "https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p186423_b_v8_ae.jpg",
        'description': "Monkey D. Luffy sets sail on an adventure to find the legendary One Piece and become the Pirate King. With his rubber-like powers and a crew of misfits, he faces dangerous foes, uncovering secrets of the Grand Line in this thrilling voyage."
    },
    {
        'id': 3,
        'name': 'Dragon Ball Z - Volume 1',
        'price': 22.99,
        'image': "https://m.media-amazon.com/images/I/81Lc+Yln3gL._AC_UF1000,1000_QL80_.jpg",
        'description': "Son Goku, a martial artist with a monkey tail, embarks on a quest to collect the mystical Dragon Balls. Along the way, he trains under masters, fights powerful warriors, and protects Earth from alien invaders and deadly threats."
    },
    {
        'id': 4,
        'name': 'Attack on Titan - Volume 1',
        'price': 21.99,
        'image': "https://m.media-amazon.com/images/I/81qPzeEO5IL.jpg",
        'description': "Humanity's last survivors live behind massive walls, fearing monstrous Titans that roam outside. Eren Yeager, driven by vengeance, joins the military to fight these creatures, uncovering dark secrets about the Titans and their origins."
    },
    {
        'id': 5,
        'name': 'Demon Slayer - Volume 1',
        'price': 20.99,
        'image': "https://m.media-amazon.com/images/I/81DjuU26RrL.jpg" ,
        'description': "Tanjiro Kamado’s peaceful life shatters when his family is slaughtered by demons, leaving only his sister Nezuko, who has turned into one. Determined to save her, he trains as a Demon Slayer, facing deadly demons and uncovering hidden mysteries."
    },
    {
        'id': 6,
        'name': 'Tokyo Ghoul - Volume 1',
        'price': 18.99,
        'image': "https://m.media-amazon.com/images/I/71D7jILMozL.jpg",
        'description': "Ken Kaneki, an ordinary student, survives a brutal attack only to find himself transformed into a half-ghoul. Now forced to consume human flesh, he struggles between his humanity and monster instincts while navigating a dangerous underground world."
    },
    {
        'id': 7,
        'name': 'Death Note - Volume 1',
        'price': 23.99,
        'image': "https://upload.wikimedia.org/wikipedia/en/6/6f/Death_Note_Vol_1.jpg",
        'description': "Light Yagami, a brilliant student, finds a mysterious Death Note that allows him to kill anyone by writing their name. As he takes justice into his own hands, a cat-and-mouse game begins with the genius detective L, testing the limits of morality."
    },
    {
        'id': 8,
        'name': 'Jujutsu Kaisen - Volume 1',
        'price': 22.49,
        'image': "https://m.media-amazon.com/images/I/81XO20bHFjL.jpg",
        'description': "Yuji Itadori, a high schooler with extraordinary strength, eats a cursed object and becomes the host of a powerful demon. Now a part of the Jujutsu Sorcerers, he must fight monstrous curses and uncover the dark mysteries behind his new powers."
    },
    {
        'id': 9,
        'name': 'Fullmetal Alchemist - Volume 1',
        'price': 21.49,
        'image': "https://m.media-amazon.com/images/I/71bHV97PPmL.jpg",
        'description': "Edward and Alphonse Elric break the laws of alchemy in a failed experiment to bring back their mother. Losing their bodies, they set out on a dangerous journey to find the Philosopher’s Stone and reclaim what they lost, facing powerful enemies."
    },
    {
        'id': 10,
        'name': 'Bleach - Volume 1',
        'price': 19.49,
        'image': "https://m.media-amazon.com/images/I/61aSap+A1iL._AC_UF1000,1000_QL80_.jpg",
        'description': "Ichigo Kurosaki, an ordinary teen, gains Soul Reaper powers to protect the living from evil spirits called Hollows. As he fights stronger enemies, he unravels hidden truths about the Soul Society and his own mysterious past."
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
