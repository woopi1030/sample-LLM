import os
from openai import OpenAI
from datetime import datetime
import json

from db import save_contents

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
    
# 시스템 메시지 세팅
def get_system_message(case):
    if case == "sample":
        return """
        당신은 주어진 텍스트를 바탕으로 튜토리얼을 생성하는 AI 어시스턴트입니다.
        텍스트에 어떤 절차를 진행하는 방법에 대한 지침이 포함되어 있다면,
        글머리 기호 목록 형식으로 튜토리얼을 생성하십시오.
        그렇지 않으면 텍스트에 지침이 포함되어 있지 않음을 사용자에게 알리십시오.

        텍스트 : 
        """
    elif case == "horoscope":
        return """
        당신은 운세 전문가 AI입니다.

        아래 두 가지 항목에 대한 오늘의 운세를 JSON 형식으로 생성하십시오:

        1. 띠별 운세 (12간지): 
        - 각 띠(쥐, 소, 호랑이, 토끼, 용, 뱀, 말, 양, 원숭이, 닭, 개, 돼지)에 대해
        - 해당 띠에 속하는 주요 출생 연도별 운세도 포함시켜 주세요. (예: 쥐띠 - 1948, 1960, 1972, 1984, 1996)

        2. 별자리 운세:
        - 양자리, 황소자리, 쌍둥이자리, 게자리, 사자자리, 처녀자리, 천칭자리, 전갈자리, 사수자리, 염소자리, 물병자리, 물고기자리

        반드시 다음 JSON 형태로 응답하세요:

        {
            "date": "YYYYMMDD",
            "horoscope": {
                "chinese_zodiac": {
                    "쥐": {
                        "1984": "운세 내용...",
                        "1996": "운세 내용...",
                        ...
                    },
                    ...
                },
                "zodiac_sign": {
                    "양자리": "운세 내용...",
                    ...
                }
            }
        }
        """
    else:
        return "not supported system message."

# instructions 세팅
def get_instructions(case):
    if case == "sample":
        return """
        이탈리아 제노바에서 유명한 소스를 준비하려면, 먼저 잣을 구워
        바질과 마늘과 함께 부억 절구에 넣어 굵게 다집니다.
        그런 다음 절구에 오일의 절반을 넣고 소금과 후추로 간을 합니다.
        마지막으로 페스토를 그릇에 옮기고 파르메산 치즈 간것을 넣고 저어줍니다.
        """
    elif case == "horoscope":
        today = datetime.today().strftime("%Y년 %m월 %d일")
        return f"""
        오늘은 {today}입니다. 위의 형식에 맞게 띠별과 별자리별 운세를 제공해주세요.
        """
    else:
        return "not supported instructions"

# OpenAI API를 사용하여 비용을 계산하는 함수
def calculate_cost(usage, model="gpt-4o"):
    if model == "gpt-4o":
        prompt_cost_per_1k = 0.005
        completion_cost_per_1k = 0.015
    else:
        raise ValueError("지원하지 않는 모델입니다.")

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens

    prompt_cost = (prompt_tokens / 1000) * prompt_cost_per_1k
    completion_cost = (completion_tokens / 1000) * completion_cost_per_1k
    total_cost = prompt_cost + completion_cost

    return round(total_cost, 6)

# OpenAI API를 사용하여 오늘의 띠별 및 별자리 운세를 가져오는 함수
def get_daily_horoscope(case):
    openai_api_key = getApiKeyFromFile()
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": get_system_message(case)},
            {"role": "user", "content": get_instructions(case)}
        ]
    )

    usage = response.usage
    print("##### Total costs :", calculate_cost(usage, model="gpt-4o"))

    return response.choices[0].message.content

# respose에서 json 코드 블록이 있다면 제거
def clean_json_response(text: str) -> str:
    """
    OpenAI 응답에서 markdown 코드 블록(```json ... ```)을 제거함
    """
    if text.startswith("```json"):
        text = text.replace("```json", "", 1)
    elif text.startswith("```"):
        text = text.replace("```", "", 1)

    text = text.strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


# python 스크립트 실행
try:
    result = get_daily_horoscope("horoscope")
    result_parsed_json = clean_json_response(result)

    parsed = json.loads(result_parsed_json)
    print(json.dumps(parsed, indent=4, ensure_ascii=False))

    save_contents(parsed)

except json.JSONDecodeError as e:
    print("⚠️ JSON 파싱 오류:", e)
