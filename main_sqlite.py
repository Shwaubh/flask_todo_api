from flask import Flask, request
from db import db, Todo

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/todos", methods=["GET"])
def get_todos(): 
    todos = Todo.query.all()
    response = []
    for todo in todos:
        response.append({
            "id": todo.id,
            "task": todo.task,
            "done": todo.done
        })
    return response

@app.route("/todos/<int:id>", methods=["GET"])
def get_todo(id):
    todo = Todo.query.get(id)
    if todo:
        return {
            "id": todo.id,
            "task": todo.task,
            "done": todo.done
        }
    else:
        return {
            "error": "Todo not found"
        }, 404

@app.route("/todos", methods=["POST"])
def post_todos():
    requestdata = request.get_json()
    task = requestdata["task"]
    new_task = Todo(task=task)
    db.session.add(new_task)
    db.session.commit()
    return {
        "id": new_task.id,
        "task": new_task.task,
        "done": new_task.done
    }, 201
    
@app.route("/todos/<int:id>", methods=["PUT"])   
def put_todos(id):
    requestdata = request.get_json()
    todo = Todo.query.get(id)
    if todo:
        todo.task = requestdata.get("task", todo.task)
        todo.done = requestdata.get("done", todo.done)
        db.session.commit()
        return {
            "id": todo.id,
            "task": todo.task,
            "done": todo.done
        }
    else:
        return {
            "error": "Todo not found"
        }, 404

@app.route("/todos/<int:id>", methods=["DELETE"])  
def delete_todos(id):
    todo = Todo.query.get(id)
    if not todo:
        return {
            "error": "Todo not found"
        }, 404
    db.session.delete(todo)
    db.session.commit() 
    return {
        "message": "Todo deleted successfully"
    }

if __name__ == "__main__":
    app.run(debug=True)