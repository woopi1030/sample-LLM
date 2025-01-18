import os
from openai import OpenAI

# ::::: [def] :::::

# 파일에서 API_KEY 반환
def getApiKeyFromFile () -> str:
    # 현재 스크립트의 디렉토리 경로
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 파일 경로 생성
    file_path = os.path.join(current_directory, "api_key.txt")

    try:
        # 파일 읽기
        with open(file_path, 'r') as file:
            return file.readline().strip()  # 첫 번째 줄 읽기 및 공백 제거
    except FileNotFoundError:
        raise FileNotFoundError("api_key.txt 파일을 찾을 수 없습니다.")
    except Exception as e:
        raise Exception(f"파일 읽기 중 오류가 발생했습니다: {e}") 

# ::::: [process] :::::

# API Key 세팅
openai_api_key = getApiKeyFromFile()

# 사용자 질의를 받음 (system_message, instructions)
system_message ="""
당신은 주어진 텍스트를 바탕으로 튜토리얼을 생성하는 AI 어시스턴트입니다.
텍스트에 어떤 절차를 진행하는 방법에 대한 지침이 포함되어 있다면,
글머리 기호 목록 형식으로 튜토리얼을 생성하십시오.
그렇지 않으면 텍스트에 지침이 포함되어 있지 않음을 사용자에게 알리십시오.

텍스트 : 
"""

instructions = """
이탈리아 제노바에서 유명한 소스를 준비하려면, 먼저 잣을 구워
바질과 마늘과 함께 부억 절구에 넣어 굵게 다집니다.
그런 다음 절구에 오일의 절반을 넣고 소금과 후추로 간을 합니다.
마지막으로 페스토를 그릇에 옮기고 파르메산 치즈 간것을 넣고 저어줍니다.
"""

# 클라이언트를 초기화하고 채팅을 완성
client = OpenAI(api_key=openai_api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": instructions}
    ]
)

print(response.choices[0])
