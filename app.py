"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push()

#-----App config--------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SECRET_KEY'] = 'kikostinky'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

#  ---------- ROUTES -----------------------
@app.route('/api/cupcakes', methods=["GET", "POST"])
def show_all_cupcakes():
    '''Show list of all cupcakes & handle adding new cupcake'''
    
    if request.method == "POST":
        data = request.json
        
        new_cupcake = Cupcake(
            flavor=data['flavor'],
            size=data['size'],
            rating=data['rating'],
            image=data['image'] or None
        )
        
        db.session.add(new_cupcake)
        db.session.commit()
        
        serialized = new_cupcake.serialize()
        
        return (jsonify(cupcake=serialized), 201)
    else:
        cupcakes = Cupcake.query.all()
        serialized = [c.serialize() for c in cupcakes]
        
        return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    '''Get data about one cupcake'''
    
    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()
    
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    '''Update a single cupcake'''
    data = request.json
    cupcake= Cupcake.query.get_or_404(id)

    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"]
    
    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    '''Delete a single cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="Cupcake Deleted")