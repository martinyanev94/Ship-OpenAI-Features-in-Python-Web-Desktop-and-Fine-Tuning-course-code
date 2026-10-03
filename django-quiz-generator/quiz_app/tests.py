from django.test import TestCase
from .models import Question, Quiz


class QuizModelTests(TestCase):
    def test_question_is_linked_to_source_quiz(self):
        quiz = Quiz.objects.create(source_material="A short study note.")
        question = Question.objects.create(
            quiz=quiz,
            prompt="What is stored?",
            option_a="A study note",
            option_b="A password",
            option_c="An image",
            option_d="A URL",
            correct_answer="A",
        )
        self.assertEqual(quiz.questions.first(), question)
        self.assertEqual(question.quiz.source_material, "A short study note.")
