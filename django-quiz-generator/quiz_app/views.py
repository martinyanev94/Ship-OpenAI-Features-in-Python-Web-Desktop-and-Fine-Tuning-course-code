import json
import os
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from openai import OpenAI
from .forms import QuizGenerationForm
from .models import Question, Quiz


def generate(request):
    form = QuizGenerationForm(request.POST or None)
    error = None
    if request.method == "POST" and form.is_valid():
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Return JSON with a questions array; each item has prompt and answer."},
                {"role": "user", "content": form.cleaned_data["source_material"]},
            ],
        )
        try:
            questions = json.loads(response.choices[0].message.content)["questions"]
            with transaction.atomic():
                quiz = Quiz.objects.create(source_material=form.cleaned_data["source_material"])
                for item in questions:
                    Question.objects.create(quiz=quiz, prompt=item["prompt"], answer=item["answer"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            error = f"The generated quiz was not valid: {exc}"
        else:
            return redirect("history")
    return render(request, "quiz_app/generate.html", {"form": form, "error": error})


def history(request):
    quizzes = Quiz.objects.order_by("-created_at")
    return render(request, "quiz_app/history.html", {"quizzes": quizzes})


def download(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    lines = [f"Quiz {quiz.id}", ""]
    for number, question in enumerate(quiz.questions.all(), 1):
        lines.extend([f"{number}. {question.prompt}", f"Answer: {question.answer}", ""])
    response = HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="quiz-{quiz.id}.txt"'
    return response
