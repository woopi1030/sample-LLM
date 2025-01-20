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
    
def get_system_message(case):
    if case == "case1":
        return """
        당신은 주어진 텍스트를 바탕으로 튜토리얼을 생성하는 AI 어시스턴트입니다.
        텍스트에 어떤 절차를 진행하는 방법에 대한 지침이 포함되어 있다면,
        글머리 기호 목록 형식으로 튜토리얼을 생성하십시오.
        그렇지 않으면 텍스트에 지침이 포함되어 있지 않음을 사용자에게 알리십시오.

        텍스트 : 
        """
    elif case == "case2":
        return """
        당신은 기사를 요약하는 AI 어시스턴트인니다.
        이 작업을 완료하며녀 다음 하위 작업을 수행하십시오:

        제공된 기사 내용을 종합적으로 읽고 주요 주제와 핵심 요점을 식별합니다.
        현재 기사 내용을 요약하여 본직적인 정보와 주요 아이디어를 전달하는 단락 요약을 생성합니다.
        과정의 각 단계를 출력합니다.

        기사:
        """
    else:
        return "not supported system message."

def get_instructions(case):
    if case == "case1":
        return """
        이탈리아 제노바에서 유명한 소스를 준비하려면, 먼저 잣을 구워
        바질과 마늘과 함께 부억 절구에 넣어 굵게 다집니다.
        그런 다음 절구에 오일의 절반을 넣고 소금과 후추로 간을 합니다.
        마지막으로 페스토를 그릇에 옮기고 파르메산 치즈 간것을 넣고 저어줍니다.
        """
    elif case == "case2":
        return """
        순환 신경망, 장단기 기억 및 게이트 순환 신경망은 특히 언어 모델링 및 기계 번역과 같은 시퀀스 모델링 및 변환 문제에서 최첨단 접근 방식으로 확고히 자리 잡았습니다. 
        그 이후로 수많은 노력들이 순환 언어 모델과 인코더-디코더 아키텍처의 경계를 계속 확장하고 있습니다.
        순환 모델은 일반적으로 입력 및 출력 시퀀스의 심볼 위치를 따라 계산을 요인화합니다. 
        계산 시간의 단계에 맞추어 위치를 정렬하면, 이전 숨겨진 상태 ht-1 및 위치 t에 대한 입력의 함수로서 숨겨진 상태 ht의 시퀀스를 생성합니다. 
        이러한 본질적으로 순차적인 특성은 훈련 예제 내에서 병렬화를 방지하여 더 긴 시퀀스 길이에서 중요해집니다. 
        메모리 제한이 예제 간 배칭을 제한하기 때문입니다. 
        최근 작업에서는 팩토라이제이션 트릭 및 조건부 계산을 통해 계산 효율성을 크게 개선하면서 후자의 경우 모델 성능도 개선했습니다. 
        그러나 순차 계산의 근본적인 제약은 여전히 남아 있습니다.
        어텐션 메커니즘은 다양한 작업에서 설득력 있는 시퀀스 모델링 및 변환 모델의 필수 요소가 되어 입력 또는 출력 시퀀스의 거리와 관계없이 종속성을 모델링할 수 있게 합니다. 
        하지만 몇 가지 경우를 제외하고 이러한 어텐션 메커니즘은 순환 네트워크와 함께 사용됩니다.
        이 작업에서는 반복을 배제하고 입력과 출력을 연결하기 위해 전적으로 어텐션 메커니즘에 의존하는 모델 아키텍처인 트랜스포머를 제안합니다. 
        트랜스포머는 훨씬 더 많은 병렬 처리가 가능하며, 8개의 P100 GPU에서 12시간 동안 훈련한 후 번역 품질에서 새로운 최첨단에 도달할 수 있습니다.
        """
    else:
        return "not supported instructions"

# ::::: [process] :::::

# API Key 세팅
openai_api_key = getApiKeyFromFile()

# 클라이언트를 초기화하고 채팅을 완성
client = OpenAI(api_key=openai_api_key)

case = "case2"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": get_system_message(case)},
        {"role": "user", "content": get_instructions(case)}
    ]
)

# print(response.choices[0])
print(response.choices[0].message.content)
