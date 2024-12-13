from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


def to_dict():
    return{
    }

def find_message_by_id(id):
    return Message.query.where(Message.id == id).first()


@app.get('/messages')
def messages():
    all_messages = Message.query.all()

    message_dicts=[ message.to_dict(['body','username', 'created_at']) for message in all_messages ]
    
    return message_dicts

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     found_message = Message.query.where(Message.id == id).first()

#     if found_message:
#         return found_message.to_dict(), 200
    
#     else:
#          return {"status":404,"message": "Not found"}, 404

@app.post('/messages')
def posted_new_message(id):
    Body = request.json 

    try:

        new_message = Message( body= Body.get('body'), username= Body.get('username'))

        db.session.add( new_message)
        db.session.commit()

        return new_message.to_dict(), 201
    
    except Exception as error:

        return {
            "status": 400,
            "message": "Something went really wrong... do you have an associated_llcs?",
            "error_text": str(error)
        }, 400
    

@app.patch('/messages/<int:id>')
def update_message(id):
    found_message= find_message_by_id(id)

    if found_message:
        try:
            data = request.json

            for key in data:
                setattr(found_message, key, data[key])

            db.session.add(found_message)
            db.session.commit()

            return found_message.to_dict(rules=['body', 'username']), 202
        


        except:
                return {"status": 400, "message": "that didn't work"}, 400
        
    else: 
        return {"status": 404, "message": "not found"}, 400


@app.delete('/messages/<int:id>')
def delete_message_by_id(id):
    found_message = find_message_by_id(id)

    if found_message:
        db.session.delete(found_message)
        db.session.commit()

        return {"message": "Deleted successfully"}, 201
    
    else:
        return {"status": 404 , "message": "Not found"}, 404






if __name__ == '__main__':
    app.run(port=5555, debug=True)
