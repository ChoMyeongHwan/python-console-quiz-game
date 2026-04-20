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
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리에서 Quiz 객체를 생성 (파일 불러올 때 사용)"""
        return Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )