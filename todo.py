from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy #orm kurmak icin gerekli olan modul

# orm yapisi
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tanju/Desktop/vscode/todoapp/todo.db'
db = SQLAlchemy(app)

@app.route('/') #index url yapisi (main page)
def index():
    todos =Todo.query.all()
    return render_template('index.html',todos=todos)

@app.route('/add',methods = ['POST'])# /add url yapisi
def addTodo():
    title = request.form.get('title') #girdiyi aliyor
    newTodo = Todo(title= title, complete= False) #girdiye gore yeni veriyi hazirliyo
    db.session.add(newTodo) # yeni veriyi db ye ekleiyor
    db.session.commit()

    return redirect(url_for('index'))

# /complete url yapisi, tamamlama icin
@app.route('/complete/<string:id>')
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first() #orm yapisinin sql degisiklik ypatirina modulleri
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first() 
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


# veri tabaninda toablo olusturmak icin gerekli yapi
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(80))
    complete = db.Column(db.Boolean)

#  server'i ayaga kaldirma
if __name__ == '__main__':
    db.create_all() # yazdigimiz class larin veri tabaninda olusmasini sagliyor
    app.run(debug=True)