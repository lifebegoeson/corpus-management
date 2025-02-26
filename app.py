from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corpus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 语料数据库模型
class Corpus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(255))
    source = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'source': self.source,
            'video_url': self.video_url,
            'created_at': self.created_at.isoformat()
        }

# 添加语料
@app.route('/add', methods=['POST'])
def add_entry():
    data = request.json
    new_entry = Corpus(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        tags=','.join(data.get('tags', [])),
        source=data.get('source', ''),
        video_url=data.get('video_url', '')
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Entry added successfully'})

# 搜索语料
@app.route('/search', methods=['GET'])
def search_entries():
    query = request.args.get('query', '')
    c
