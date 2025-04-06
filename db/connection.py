from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()  # .env 파일 로드

# 전역 변수로 클라이언트 선언
client = None

def connect():
    global client
    try:
        user_id = os.getenv("MONGODB_USER_ID")
        password = os.getenv("MONGODB_USER_PASSWORD")

        uri = f"mongodb+srv://{user_id}:{password}@personalization.hmzxr.mongodb.net/?retryWrites=true&w=majority&appName=personalization"

        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("### success : Connected to MongoDB!")
        return client
    except Exception as e:
        print(f"### fail : MongoDB connection failed: {e}")
        return None

def disconnect():
    global client
    if client:
        client.close()
        print("### success :  Disconnected from MongoDB.")
    else:
        print("### fail : No active MongoDB connection to close.")


# 테스트
# connect()
# disconnect()