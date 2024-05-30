# one-to-one relationship
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     address = relationship("Address", uselist=False, back_populates="user")
# class Address(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     email = Column(String)
#     user = relationship("User", back_populates="address")
#
# user = session.query(User).filter_by(name="John Doe").first()
# print(f"User: {user.name}, Email: {user.address.email}")

# one to many

# Define the User table
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     posts = relationship("Post", back_populates="user")
#
#
# # Define the Post table
# class Post(Base):
#     __tablename__ = "posts"
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     content = Column(String)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", back_populates="posts")
# user = session.query(User).filter_by(name="John Doe").first()
# print(f"User: {user.name}")
# for post in user.posts:
#     print(f"Post Title: {post.title}, Content: {post.content}")
#
# many to one
#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
#
# # Define the Post table
# class Post(Base):
#     __tablename__ = "posts"
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     content = Column(String)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user = relationship("User", back_populates="posts")
#
#
# User.posts = relationship("Post", order_by=Post.id, back_populates="user")

# posts = session.query(Post).all()
# for post in posts:
#     print(f"Post Title: {post.title}, Content: {post.content}, User: {post.user.name}")

# many to many

from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")


@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    emit("joined", {"msg": username + " has entered the room."}, room=room)


@socketio.on("leave")
def on_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    emit("message", {"msg": username + " has left the room."}, room=room)


@socketio.on("message")
def handle_message(data):
    emit("message", data, room=data["room"])


if __name__ == "__main__":
    socketio.run(app, port=4000)
