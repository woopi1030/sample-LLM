# 아무것도 안 쓰고 비워둬도 됨
# __init__.py는 꼭 필요한 것만 import할 때만 사용
# 외부에서 모듈 사용하게 할것만 넣기

from .repository import save as save_contents, find as find_contents