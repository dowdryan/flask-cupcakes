"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, url_for, redirect
from models import db, connect_db, Cupcake, default_img
from forms import CupcakeForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_menu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ohsoohsosecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def homepage():
    cupcakes = Cupcake.query.order_by(Cupcake.id).all()
    return render_template('homepage.html',
                           cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=['GET', 'POST'])
def add_cupcake():
    form = CupcakeForm()
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data
        with app.app_context():
            example = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
            db.session.add(example)
            db.session.commit()
            response = {
                "cupcake": {
                    "id": example.id,
                    "flavor": flavor,
                    "size": size,
                    "rating": rating,
                    "image": image
                }
            }
        return jsonify(response), 201
        # return redirect(url_for('homepage'))
    return render_template('addcupcake.html',
                           form=form)

@app.route('/api/cupcakes')
def get_all_cupcakes():
    cupcakes = Cupcake.query.order_by(Cupcake.id).all()
    # Insert each cupcake 1 at a time instead of all at once
    all_cupcakes = [cupcake.to_dict() for cupcake in cupcakes]
    response = {"cupcakes": all_cupcakes}
    return jsonify(response)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())


if __name__ == "__main__":
    app.run(debug=True)