from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(200), nullable=False)
    vol = db.Column(db.Integer, primary_key=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all() 

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        vol_content = request.form['vol']
        exercise_content = request.form['exercise']
        new_task = Todo(
            exercise=exercise_content,
            vol = vol_content
            )

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_deleted = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_deleted)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)