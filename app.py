from flask import Flask, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] <= 3:
        article = Article.query.get_or_404(id)
        return jsonify({'id': article.id, 'title': article.title, 'content': article.content})
    else:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

@app.route('/clear', methods=['GET'])
def clear_session():
    session.clear()
    return jsonify({'message': 'Session cleared'})

if __name__ == '__main__':
    app.run(debug=True)
