from quiz_game import QuizGame

if __name__ == "__main__":
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️  프로그램이 중단되었습니다. 데이터를 저장합니다...")
        game.save_state()
        print("저장 완료! 안녕히 가세요 👋")