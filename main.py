from quiz_game import QuizGame

# 현재 파일이 "직접 실행된 경우"에만 아래 코드를 실행한다.
# 다른 파일에서 import 했을 때는 실행되지 않도록 하는 파이썬 표준 패턴이다.
if __name__ == "__main__":

    game = QuizGame()
    try:
        game.run()
    
    # 사용자가 Ctrl+C를 누르거나(KeyboardInterrupt),
    # 입력 스트림 종료(Ctrl+D / EOFError)가 발생한 경우를 처리한다.
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️  프로그램이 중단되었습니다. 데이터를 저장합니다...")
        
        game.save_state()
        print("저장 완료! 안녕히 가세요 👋")