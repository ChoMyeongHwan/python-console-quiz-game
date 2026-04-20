from quiz import DEFAULT_QUIZZES

STATE_FILE = "state.json"

class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = DEFAULT_QUIZZES[:]  # 일단 기본 데이터 사용
        self.best_score = 0

    # ── 메뉴 ─────────────────────────────────────
    def show_menu(self):
        print("\n" + "="*35)
        print("       🎮 Python 퀴즈 게임")
        print("="*35)
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 점수 확인")
        print("  5. 종료")
        print("="*35)

    def run(self):
        print("퀴즈 게임에 오신 것을 환영합니다! 👋")
        while True:
            self.show_menu()
            choice = self._get_valid_number("메뉴 선택: ", 1, 5)
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("안녕히 가세요 👋")  # ← 아직 저장 기능 없음
                break

    # ── 공통 입력 처리 ────────────────────────────
    def _get_valid_number(self, prompt, min_val, max_val):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("⚠️  값을 입력해주세요.")
                    continue
                num = int(user_input)
                if min_val <= num <= max_val:
                    return num
                print(f"⚠️  {min_val}~{max_val} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️  숫자만 입력해주세요.")

    def _get_valid_text(self, prompt):
        while True:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print("⚠️  내용을 입력해주세요.")