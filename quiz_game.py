import json
import os
import random
from quiz import Quiz
from utils import get_valid_integer, get_non_empty_string
from stats import calculate_average_score, calculate_total_games, calculate_improvement


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""
    
    STATE_FILE = "state.json"
    
    def __init__(self):
        """QuizGame 인스턴스를 초기화합니다."""
        self.quizzes = []
        self.best_score = 0
        self.game_history = []  # 게임 기록 히스토리
        self.load_data()
    
    def create_default_quizzes(self):
        """기본 퀴즈 데이터를 생성합니다."""
        default_quizzes = [
            Quiz(
                "마블 시네마틱 유니버스에서 타노스가 모은 인피니티 스톤의 개수는?",
                ["4개", "5개", "6개", "7개"],
                3
            ),
            Quiz(
                "영화 '인터스텔라'의 감독은?",
                ["스티븐 스필버그", "크리스토퍼 놀란", "팀 버튼", "제임스 카메론"],
                2
            ),
            Quiz(
                "Python의 창시자는?",
                ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Arthur"],
                1
            ),
            Quiz(
                "HTML에서 문서의 기본 구조를 정의하는 요소는?",
                ["<div>", "<section>", "<html>", "<body>"],
                3
            ),
            Quiz(
                "Git의 기본 브랜치 이름은?",
                ["main", "master", "develop", "trunk"],
                2
            ),
            Quiz(
                "JavaScript에서 변수를 선언하는 최신 방식은?",
                ["var", "let", "const", "define"],
                2
            ),
            Quiz(
                "React의 핵심 개념은?",
                ["MVC", "Component", "Service", "Model"],
                2
            ),
            Quiz(
                "Docker는 무엇을 사용하여 애플리케이션을 패키징하는가?",
                ["이미지", "컨테이너", "가상머신", "클라우드"],
                2
            ),
            Quiz(
                "REST API에서 POST는 어떤 작업에 사용되는가?",
                ["조회", "생성", "수정", "삭제"],
                2
            ),
            Quiz(
                "데이터베이스에서 PRIMARY KEY는 무엇을 보장하는가?",
                ["빠른 실행", "유일성", "암호화", "백업"],
                2
            ),
        ]
        return default_quizzes
    
    def load_data(self):
        """state.json에서 데이터를 불러옵니다."""
        if not os.path.exists(self.STATE_FILE):
            # 파일이 없으면 기본 데이터로 초기화
            self.quizzes = self.create_default_quizzes()
            self.best_score = 0
            self.game_history = []
            self.save_data()
            return
        
        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 퀴즈 로드
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            self.game_history = data.get("game_history", [])
            
            # 로드된 데이터가 없으면 기본값 사용
            if not self.quizzes:
                self.quizzes = self.create_default_quizzes()
                self.save_data()
        
        except json.JSONDecodeError:
            # 파일이 손상된 경우
            print("⚠️ 저장된 데이터가 손상되었습니다. 기본 데이터로 복구합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = 0
            self.game_history = []
            self.save_data()
        
        except Exception as e:
            # 다른 오류 발생
            print(f"⚠️ 데이터 로드 중 오류가 발생했습니다: {e}")
            self.quizzes = self.create_default_quizzes()
            self.best_score = 0
            self.game_history = []
            self.save_data()
    
    def save_data(self):
        """데이터를 state.json에 저장합니다."""
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
                "game_history": self.game_history
            }
            
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            print(f"⚠️ 데이터 저장 중 오류가 발생했습니다: {e}")
    
    def display_menu(self):
        """메인 메뉴를 출력합니다."""
        print("\n" + "=" * 50)
        print("🎯 나만의 퀴즈 게임 🎯".center(50))
        print("=" * 50)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 50)
    
    def get_menu_choice(self):
        """메뉴 선택을 입력받습니다."""
        try:
            return get_valid_integer("선택: ", 1, 5)
        except EOFError:
            print("\n프로그램을 종료합니다.")
            self.save_data()
            exit()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            self.save_data()
            exit()
    
    def play_quiz(self):
        """퀴즈를 풀기 시작합니다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        
        # 퀴즈 순서를 랜덤하게 섞기
        shuffled_quizzes = self.quizzes.copy()
        random.shuffle(shuffled_quizzes)
        
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(shuffled_quizzes)}문제 - 랜덤 순서)")
        print("-" * 50)
        
        score = 0
        
        try:
            for i, quiz in enumerate(shuffled_quizzes, 1):
                quiz.display(i)
                answer = get_valid_integer("정답 입력: ", 1, 4)
                
                if quiz.check_answer(answer):
                    print("✅ 정답입니다!")
                    score += 1
                else:
                    print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
                
                print("-" * 50)
        
        except EOFError:
            print("\n프로그램을 종료합니다.")
            self.save_data()
            exit()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            self.save_data()
            exit()
        
        # 결과 표시
        self.display_result(score, len(shuffled_quizzes))
    
    def display_result(self, correct, total):
        """퀴즈 결과를 표시합니다."""
        from datetime import datetime
        
        percentage = (correct / total) * 100
        
        print("\n" + "=" * 50)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({int(percentage)}점)")
        
        # 게임 기록 저장
        game_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": correct,
            "total": total,
            "percentage": int(percentage)
        }
        self.game_history.append(game_record)
        
        # 최고 점수 업데이트
        if correct > self.best_score:
            self.best_score = correct
            print("🎉 새로운 최고 점수입니다!")
            self.save_data()
        else:
            self.save_data()
        
        print("=" * 50)
    
    def add_quiz(self):
        """새로운 퀴즈를 추가합니다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        print("-" * 50)
        
        try:
            question = get_non_empty_string("문제를 입력하세요: ")
            
            choices = []
            for i in range(1, 5):
                choice = get_non_empty_string(f"선택지 {i}: ")
                choices.append(choice)
            
            answer = get_valid_integer("정답 번호 (1-4): ", 1, 4)
            
            # 퀴즈 추가
            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)
            self.save_data()
            print("✅ 퀴즈가 추가되었습니다!")
        
        except EOFError:
            print("\n프로그램을 종료합니다.")
            self.save_data()
            exit()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            self.save_data()
            exit()
    
    def display_quiz_list(self):
        """저장된 퀴즈 목록을 출력합니다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        
        print("\n" + "=" * 50)
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("=" * 50)
        
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")
        
        print("=" * 50)
    
    def display_best_score(self):
        """최고 점수를 출력합니다."""
        print("\n" + "=" * 50)
        print("🏆 점수 확인".center(50))
        print("=" * 50)
        
        if self.best_score == 0 and self.quizzes:
            print("아직 퀴즈를 풀지 않았습니다.")
        else:
            total = len(self.quizzes)
            if total > 0:
                percentage = (self.best_score / total) * 100
                print(f"최고 점수: {self.best_score}문제 중 {self.best_score}문제 정답 ({int(percentage)}점)")
            else:
                print("등록된 퀴즈가 없습니다.")
        
        # 게임 통계
        if self.game_history:
            print("\n📊 게임 통계:")
            print("-" * 50)
            total_games = calculate_total_games(self.game_history)
            avg_score = calculate_average_score(self.game_history)
            improvement = calculate_improvement(self.game_history)
            
            print(f"총 게임 횟수: {total_games}회")
            print(f"평균 정답률: {int(avg_score)}%")
            print(f"향상도: {improvement:+d}%포인트")
            
            print("\n최근 게임 기록:")
            print("-" * 50)
            for i, record in enumerate(self.game_history[-5:], 1):
                print(f"{i}. {record['timestamp']} - {record['score']}/{record['total']} ({record['percentage']}%)")
        
        print("=" * 50)
    
    def run(self):
        """게임 메인 루프를 실행합니다."""
        print("\n📂 저장된 데이터를 불러왔습니다.")
        print(f"   퀴즈: {len(self.quizzes)}개, 최고점수: {self.best_score}점\n")
        
        try:
            while True:
                self.display_menu()
                choice = self.get_menu_choice()
                
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.display_quiz_list()
                elif choice == 4:
                    self.display_best_score()
                elif choice == 5:
                    print("\n게임을 종료합니다. 안녕히 가세요!")
                    self.save_data()
                    break
        
        except EOFError:
            print("\n프로그램을 종료합니다.")
            self.save_data()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            self.save_data()


if __name__ == "__main__":
    game = QuizGame()
    game.run()
