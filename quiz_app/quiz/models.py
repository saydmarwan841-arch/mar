"""
Quiz Application Models
========================
Modern, well-documented models for the Quiz Application.
Supports both Multiple Choice (MCQ) and True/False (TF) question types.

This module defines the Question model which stores all quiz data
including question text, type, options, and correct answers.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Question(models.Model):
    """
    Question Model
    ==============
    Stores quiz questions with support for multiple question types.
    
    Features:
    - Multiple Choice Questions (4 options: A, B, C, D)
    - True/False Questions
    - Display order management
    - Timestamps for tracking
    
    Attributes:
        text (TextField): The question text in Arabic or English
        question_type (CharField): Type of question ('MCQ' or 'TF')
        option_a, option_b, option_c, option_d (CharField): MCQ answer options
        correct_answer (CharField): The correct answer (A, B, C, D, True, False)
        order (IntegerField): Display order for quiz questions
        created_at (DateTimeField): Auto-set on creation
        updated_at (DateTimeField): Auto-updated on save
    """
    
    # Question type choices
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice (4 options)'),
        ('TF', 'True/False'),
    ]

    # Question content field
    text = models.TextField(
        verbose_name="نص السؤال",
        help_text="اكتب السؤال بوضوح"
    )
    
    # Question type selector
    question_type = models.CharField(
        max_length=3,
        choices=QUESTION_TYPE_CHOICES,
        default='MCQ',
        verbose_name="نوع السؤال"
    )
    
    # Multiple Choice Options (A, B, C, D)
    option_a = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="الخيار أ",
        help_text="يترك فارغاً للأسئلة True/False"
    )
    option_b = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="الخيار ب"
    )
    option_c = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="الخيار ج"
    )
    option_d = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="الخيار د"
    )
    
    # Correct answer field
    correct_answer = models.CharField(
        max_length=5,
        verbose_name="الإجابة الصحيحة",
        help_text="أدخل: A أو B أو C أو D أو True أو False"
    )
    
    # Display order for questions in quiz
    order = models.IntegerField(
        default=0,
        verbose_name="ترتيب العرض"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )

    class Meta:
        """Model metadata configuration"""
        ordering = ['order', 'id']  # Sort by display order, then by ID
        verbose_name = "سؤال"
        verbose_name_plural = "الأسئلة"
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['question_type']),
        ]

    def __str__(self):
        """String representation of the question"""
        return f"{self.order}. {self.text[:50]}..." if len(self.text) > 50 else f"{self.order}. {self.text}"

    def get_options(self):
        """
        Get formatted options for the question.
        
        Returns:
            list: List of dictionaries with option information
                For MCQ: {'label': 'أ', 'value': 'A', 'text': option_text}
                For TF: {'label': 'صحيح', 'value': 'True', 'text': 'صحيح'}
        """
        if self.question_type == 'MCQ':
            # Return MCQ options with Arabic labels
            return [
                {'label': 'أ', 'value': 'A', 'text': self.option_a},
                {'label': 'ب', 'value': 'B', 'text': self.option_b},
                {'label': 'ج', 'value': 'C', 'text': self.option_c},
                {'label': 'د', 'value': 'D', 'text': self.option_d},
            ]
        elif self.question_type == 'TF':
            # Return True/False options with Arabic labels
            return [
                {'label': 'صحيح', 'value': 'True', 'text': 'صحيح'},
                {'label': 'خطأ', 'value': 'False', 'text': 'خطأ'},
            ]
        return []

    def is_correct(self, answer):
        """
        Check if the provided answer is correct.
        
        Args:
            answer (str): The user's answer
            
        Returns:
            bool: True if answer matches correct_answer, False otherwise
        """
        return str(answer).strip().lower() == str(self.correct_answer).strip().lower()

