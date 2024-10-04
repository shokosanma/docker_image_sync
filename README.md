# Auto Image Sync

This is a simple flask app that will sync images from a harbor to another harbor. With a HTTP request that send by `local_request.py` you can trigger the sync.

## Requirements
1. Python 3.6+
2. Flask
3. dotenv
4. docker

## Installation

1. Clone the repo:
```bash
git clone https://github.com/shokosanma/docker_image_sync.git
```

2. Install dependencies:
```bash
cd docker_image_sync
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

3. Run the app:
```bash
cp env.example .env
# edit the .env file
python app.py &> log.txt &
```

4. Run the local_request.py:
```bash
python local_request.py --image nginx:latest
```

The local_request.py will send a HTTP request to the app. The app will then sync the image from the source harbor to the destination harbor.
