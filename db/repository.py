from db import connection

db = None          # DB 이름
collection = None  # Collection 이름

def set_collection(client):
    db = client["sample_db"]
    collection = db["sample_collection"]
    return collection

def save(data):
    client = connection.connect()

    # 사용할 DB와 Collection 선택
    try:
        collection = set_collection(client)

        # 저장
        result = collection.insert_one(data)

        # 결과 출력
        print("Inserted ID:", result.inserted_id)
        
    except Exception as e:
        print(f"MongoDB save failed: {e}")

    connection.disconnect()


def find(requset_param):
    client = connection.connect()

    # 사용할 DB와 Collection 선택
    try:
        collection = set_collection(client)

        condition = {
            "date" : requset_param
        }

        result = collection.find_one(condition)
        return result
        
    except Exception as e:
        print(f"MongoDB find failed: {e}")


    connection.disconnect()


# save("")
# find("20250327")