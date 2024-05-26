from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store (replace with database in production)
posts = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the content of the first post.'},
    {'id': 2, 'title': 'Second Post', 'content': 'This is the content of the second post.'}
]

# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

# Get a single post by ID
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = next((post for post in posts if post['id'] == id), None)
    if post:
        return jsonify(post)
    else:
        return jsonify({'message': 'Post not found'}), 404

# Create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Invalid request'}), 400

    new_post = {
        'id': len(posts) + 1,
        'title': data['title'],
        'content': data['content']
    }
    posts.append(new_post)
    return jsonify(new_post), 201

# Update a post by ID
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Invalid request'}), 400

    post = next((post for post in posts if post['id'] == id), None)
    if post:
        post['title'] = data['title']
        post['content'] = data['content']
        return jsonify(post)
    else:
        return jsonify({'message': 'Post not found'}), 404

# Delete a post by ID
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global posts
    initial_length = len(posts)
    posts = [post for post in posts if post['id'] != id]
    if len(posts) < initial_length:
        return jsonify({'message': 'Post deleted'}), 200
    else:
        return jsonify({'message': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
