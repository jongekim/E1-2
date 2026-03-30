"""게임 통계 관련 함수"""


def calculate_average_score(game_history):
    """
    게임 히스토리에서 평균 점수를 계산합니다.
    
    Args:
        game_history (list): 게임 기록 리스트
    
    Returns:
        float: 평균 점수 (0 ~ 100)
    """
    if not game_history:
        return 0.0
    
    total_percentage = sum(record.get("percentage", 0) for record in game_history)
    return total_percentage / len(game_history) if game_history else 0.0


def calculate_total_games(game_history):
    """
    총 게임 횟수를 반환합니다.
    
    Args:
        game_history (list): 게임 기록 리스트
    
    Returns:
        int: 게임 횟수
    """
    return len(game_history)


def calculate_improvement(game_history):
    """
    첫 게임과 마지막 게임의 점수 향상도를 계산합니다.
    
    Args:
        game_history (list): 게임 기록 리스트
    
    Returns:
        int: 향상도 (percentage 포인트). 음수일 수 있음.
    """
    if len(game_history) < 2:
        return 0
    
    first_score = game_history[0].get("percentage", 0)
    last_score = game_history[-1].get("percentage", 0)
    
    return last_score - first_score
