from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///groceries.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Groceries(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    item: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    quantity: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    result = db.session.execute(db.select(Groceries).order_by(Groceries.item))
    all_groceries = result.scalars().all()
    return render_template('index.html', groceries=all_groceries)
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        new_item = Groceries(
            item=request.form['item'],
            quantity=request.form['quantity']
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')
@app.route('/edit',methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        item_id = request.form['id']
        item_to_update = db.get_or_404(Groceries, item_id)
        item_to_update.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('home'))
    item_id = request.args.get('id')
    item_selected = db.get_or_404(Groceries, item_id)
    return render_template('edit.html', id=item_id, item=item_selected)
@app.route("/delete")
def delete():
    item_id = request.args.get('id')

    # DELETE A RECORD BY ID
    item_to_delete = db.get_or_404(Groceries, item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete_confirm")
def delete_confirm():
    item_id = request.args.get('id')
    item_to_delete = db.get_or_404(Groceries, item_id)
    return render_template('delete_confirm.html', item = item_to_delete)

if __name__ == "__main__":
    app.run(debug=True)