# a flask app to sync docker image from docker hub to aliyun
import multiprocessing
from util import *
from flask import *
from dotenv import load_dotenv

load_dotenv()

# create a flask app
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/sync_image', methods=['POST'])
def sync_image():
    args = request.get_json()
    if not args:
        return jsonify({'error': 'Invalid request'})
    sync_image = args.get('sync_image')
    encrypted_message = args.get("encrypted_message")
    if verify(encrypted_message):
        prefix = os.getenv('SELF_HUB_PREFIX')
        new_image = f"{prefix}:{sync_image.replace('/', '_').replace(':', '_')}"
        # start new subprocess
        multiprocessing.Process(target=sync, args=(sync_image,new_image,)).start()
        return jsonify({'message': 'start sync image', "new_image": new_image})
    else:
        return jsonify({'error': 'Invalid password'})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)

