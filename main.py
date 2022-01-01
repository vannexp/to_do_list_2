from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(200))
    status = db.Column(db.Boolean)

@app.route("/", methods=['GET', 'POST'])
def home():
    todo_list = ToDo.query.all()
    return render_template('index.html', todos = todo_list)


@app.route("/add", methods=['GET', 'POST'])
def add():
    new_task = request.form.get('task')
    new_todo = ToDo(item=new_task, status = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    task_to_delete = ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)