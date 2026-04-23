import json
from quiz import Quiz, DEFAULT_QUIZZES

STATE_FILE = "state.json"

class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []       # Quiz 객체 목록
        self.best_score = 0     # 최고 점수 (맞힌 문제 수)
        self.has_played = False # 게임 플레이 여부 
        self.load_state()       # 시작 시 파일 불러오기

    # ── 파일 입출력 ──────────────────────────────
    def load_state(self):
        """state.json에서 데이터 불러오기"""
        try:
            # UTF-8 인코딩으로 state.json 파일을 읽는다.
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                # JSON 문자열을 파이썬 dict로 변환
                data = json.load(f)
                
                # 저장된 퀴즈 dict 목록을 Quiz 객체 목록으로 복원
                # 리스트 컴프리헨션 = "반복 + 변환 + 리스트 생성"을 한 줄로 표현
                # [변환식 for 요소 in 반복대상]
                self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]

                # best_score 키가 없더라도 기본값 0을 사용하도록 get 사용
                self.best_score = data.get("best_score", 0)
        
        except FileNotFoundError:
            # 파일 없음 → 기본 데이터 사용
            # [:]는 리스트 자체는 새로 복사하지만, 내부 객체는 공유되는 얕은 복사이다.
            # 따라서 DEFAULT_QUIZZES 리스트 자체 변경은 막지만, 내부 객체 변경은 영향을 줄 수 있다.
            self.quizzes = DEFAULT_QUIZZES[:]
            self.best_score = 0

        except (json.JSONDecodeError, KeyError):
            # 파일 손상 → 안내 후 기본 데이터로 복구
            print("⚠️  데이터 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self.quizzes = DEFAULT_QUIZZES[:]
            self.best_score = 0

        except OSError as e:
            # 파일 읽기 실패, 권한 문제 등 입출력 예외 처리
            print(f"⚠️  파일을 읽는 중 오류가 발생했습니다: {e}")
            self.quizzes = DEFAULT_QUIZZES[:]
            self.best_score = 0
            self.has_played = False

    def save_state(self):
        """state.json에 데이터 저장"""
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
                "has_played": self.has_played
            }

            # 쓰기 모드로 파일을 열고 전체 데이터를 저장한다.
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                # ensure_ascii=False:
                # 한글이 \uXXXX 형태로 깨지지 않고 그대로 저장되도록 함
                #
                # indent=2:
                # 사람이 읽기 좋은 들여쓰기 형식으로 저장
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        except IOError as e:
            # 디스크 쓰기 실패, 권한 문제 등 입출력 예외 처리
            print(f"⚠️  저장 중 오류 발생: {e}")

    # ── 메뉴 ─────────────────────────────────────
    def show_menu(self):
        """메인 메뉴 출력"""
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
        """게임 메인 루프"""
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
                self.save_state()
                print("저장 완료! 안녕히 가세요 👋")
                break

    # ── 공통 입력 처리 ────────────────────────────
    def _get_valid_number(self, prompt, min_val, max_val):
        """유효한 숫자를 입력받을 때까지 반복"""
        while True:
            try:
                # input() 결과는 문자열이므로 strip()으로 앞뒤 공백 제거
                user_input = input(prompt).strip()
                
                # 빈 입력 방지
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
        """빈 문자열이 아닌 텍스트를 입력받을 때까지 반복"""
        while True:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print("⚠️  내용을 입력해주세요.")

    def play_quiz(self):
        """퀴즈 풀기 기능"""
        if not self.quizzes:
            print("⚠️  등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        print("\n🎯 퀴즈 풀기 시작!")
        
        score = 0

        # 등록된 퀴즈를 순서대로 출제
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"\n[{i}/{len(self.quizzes)}]")
            quiz.display()

            user_answer = self._get_valid_number("정답 번호 입력: ", 1, 4)

            if quiz.check_answer(user_answer):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번이에요.")

        # 결과 출력
        total = len(self.quizzes)
        print(f"\n{'='*35}")
        print(f"🏁 결과: {total}문제 중 {score}개 정답!")
        print(f"{'='*35}")

        # 게임 플레이 여부 기록
        self.has_played = True

        # 최고 점수 갱신
        if score > self.best_score:
            self.best_score = score
            print(f"🎉 새로운 최고 점수! {score}점")
        
        self.save_state()

    def add_quiz(self):
        """새 퀴즈 등록"""
        print("\n➕ 퀴즈 추가")
        print("-" * 35)

        question = self._get_valid_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self._get_valid_text(f"선택지 {i}번: ")
            choices.append(choice)

        answer = self._get_valid_number("정답 번호 (1~4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        # 새 퀴즈 추가 시 최고 점수 초기화 (새로운 문제 추가 → 기존 최고 점수 의미 없어짐)
        self.best_score = 0
        self.has_played = False

        self.save_state()
        print("✅ 퀴즈가 추가되었습니다!")
        print("ℹ️  퀴즈가 추가되어 최고 점수가 초기화되었습니다.")

    def show_list(self):
        """등록된 퀴즈 목록 출력"""
        if not self.quizzes:
            print("⚠️  등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 35)
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"{i}. {quiz.question}")
            for j, choice in enumerate(quiz.choices, 1):
                print(f"   {j}. {choice}")
            print(f"   ✅ 정답: {quiz.answer}번")
            print()

    def show_score(self):
        """최고 점수 확인"""
        print("\n🏆 점수 확인")
        print("-" * 35)
        
        if not self.has_played:
            print("아직 퀴즈를 풀지 않았습니다.")
            print("퀴즈를 풀고 점수를 기록해보세요! 💪")
            return
            
        total = len(self.quizzes)
        # 최고 점수는 "맞힌 개수"
        print(f"최고 점수: {self.best_score} / {total} 문제")

        # 최고 점수를 전체 문제 수로 나누어 정답률 계산
        # 소수점 첫째 자리까지 출력
        print(f"정답률: {self.best_score / total * 100:.1f}%")
