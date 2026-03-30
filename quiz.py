class Quiz:
    """개별 퀴즈를 표현하는 클래스"""
    
    def __init__(self, question, choices, answer):
        """
        Quiz 인스턴스를 초기화합니다.
        
        Args:
            question (str): 퀴즈 문제
            choices (list): 4개의 선택지 리스트
            answer (int): 정답 번호 (1-4)
        """
        self.question = question
        self.choices = choices
        self.answer = answer
    
    def display(self, question_number=None):
        """
        퀴즈를 화면에 출력합니다.
        
        Args:
            question_number (int): 문제 번호 (선택사항)
        """
        if question_number:
            print(f"\n[문제 {question_number}]")
        else:
            print("\n[문제]")
        
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")
    
    def check_answer(self, user_answer):
        """
        사용자의 답이 정답인지 확인합니다.
        
        Args:
            user_answer (int): 사용자가 입력한 정답 번호
            
        Returns:
            bool: 정답이 맞으면 True, 틀리면 False
        """
        return user_answer == self.answer
    
    def to_dict(self):
        """
        퀴즈를 딕셔너리로 변환합니다 (JSON 저장용).
        
        Returns:
            dict: 퀴즈 정보를 담은 딕셔너리
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }
    
    @staticmethod
    def from_dict(data):
        """
        딕셔너리로부터 Quiz 인스턴스를 생성합니다 (JSON 불러오기용).
        
        Args:
            data (dict): 퀴즈 정보 딕셔너리
            
        Returns:
            Quiz: 생성된 Quiz 인스턴스
        """
        return Quiz(data["question"], data["choices"], data["answer"])
