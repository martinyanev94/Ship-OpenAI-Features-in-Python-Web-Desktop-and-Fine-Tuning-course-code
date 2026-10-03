from django.db import models

class Quiz(models.Model):
    source_material = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    prompt = models.TextField()
    answer = models.TextField()

    class Meta:
        ordering = ["id"]
