"""입력 검증 관련 유틸리티 함수"""


def get_valid_integer(prompt, min_value, max_value):
    """
    사용자로부터 지정된 범위의 정수를 입력받습니다.
    
    Args:
        prompt (str): 프롬프트 메시지
        min_value (int): 최소값
        max_value (int): 최대값
    
    Returns:
        int: 유효한 정수 입력값
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input:
                print(f"⚠️ 입력을 해주세요. ({min_value}-{max_value} 사이의 숫자)")
                continue
            
            value = int(user_input)
            
            if min_value <= value <= max_value:
                return value
            else:
                print(f"⚠️ {min_value}-{max_value} 사이의 숫자를 입력하세요.")
        
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
        except EOFError:
            raise
        except KeyboardInterrupt:
            raise


def get_non_empty_string(prompt):
    """
    사용자로부터 공백이 아닌 문자열을 입력받습니다.
    
    Args:
        prompt (str): 프롬프트 메시지
    
    Returns:
        str: 유효한 문자열 입력값
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if user_input:
                return user_input
            else:
                print("⚠️ 내용을 입력해주세요.")
        
        except EOFError:
            raise
        except KeyboardInterrupt:
            raise
