class Quiz:
    """개별 퀴즈 하나를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question   # str: 문제
        self.choices = choices     # list: 선택지 4개
        self.answer = answer       # int: 정답 번호 (1~4)

    def display(self):
        """문제와 선택지를 출력"""
        print(f"\n📝 {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer):
        """정답 여부 반환 (True/False)"""
        return self.answer == user_answer

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 변환"""
        # json.dump()는 사용자 정의 객체(Quiz)를 그대로 저장할 수 없기 때문에
        # 저장 가능한 기본 자료형(dict, list, str, int 등)으로 바꿔야 한다.
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    # @staticmethod은 self 매개변수를 받지 않으며, 클래스나 인스턴스 상태에 접근하지 않는 함수에 사용한다.
    @staticmethod
    def from_dict(data):
        """딕셔너리에서 Quiz 객체를 생성 (파일 불러올 때 사용)"""
        return Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )
    
# 기본 퀴즈 데이터 (파일이 없을 때 사용)
DEFAULT_QUIZZES = [
    Quiz("파이썬에서 리스트를 만드는 기호는?",
         ["()", "[]", "{}", "<>"], 2),

    Quiz("파이썬에서 주석을 작성하는 기호는?",
         ["//", "/*", "#", "--"], 3),

    Quiz("파이썬 반복문이 아닌 것은?",
         ["for", "while", "loop", "for-else"], 3),

    Quiz("파이썬에서 함수를 정의하는 키워드는?",
         ["func", "def", "function", "define"], 2),

    Quiz("파이썬에서 아무것도 없음을 나타내는 값은?",
         ["null", "undefined", "None", "empty"], 3),
]