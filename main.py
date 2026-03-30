#!/usr/bin/env python3
"""
나만의 퀴즈 게임 - 메인 진입점
"""

from quiz_game import QuizGame


def main():
    """프로그램의 메인 함수"""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
