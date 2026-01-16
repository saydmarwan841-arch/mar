"""
Quiz Application Views
======================
Handles the main quiz application logic including home, quiz,
and results pages with session management for tracking user progress.

This module implements a step-by-step quiz interface where users
answer one question at a time and receive a romantic result message.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import models
from django.contrib.sessions.models import Session
from .models import Question

# Password for manager page
MANAGER_PASSWORD = "habiba123"


@require_http_methods(["GET"])
def home(request):
    """
    Home Page View
    ==============
    Displays the welcome page with a call-to-action button to start the quiz.
    
    Features:
    - Welcome message for the user
    - Quiz introduction
    - Link to begin the quiz
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered home.html template
    """
    context = {
        'name': 'حبيبتي',  # "My Love" in Arabic - Customize this name as needed
    }
    return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
def quiz(request):
    """
    Quiz View
    =========
    Displays quiz questions one at a time and processes user answers.
    Uses Django sessions to track progress through the quiz.
    
    Features:
    - Display one question at a time
    - Process and validate answers
    - Track score and progress
    - Redirect to results when quiz is complete
    
    Session Keys:
    - quiz_started (bool): Indicates quiz is in progress
    - current_question (int): Index of current question
    - answers (dict): User's answers by question ID
    - score (int): Current score
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered quiz.html template or redirect to results
    """
    # Get all questions from database
    questions = list(Question.objects.all())
    
    # Redirect to home if no questions exist
    if not questions:
        return redirect('home')
    
    if request.method == 'GET':
        # Initialize session for new quiz attempt
        request.session['quiz_started'] = True
        request.session['current_question'] = 0
        request.session['answers'] = {}
        request.session['score'] = 0
        
        return render(request, 'quiz.html', get_quiz_context(request, questions))
    
    elif request.method == 'POST':
        # Process submitted answer
        answer = request.POST.get('answer')
        question_id = int(request.POST.get('question_id'))
        current_index = request.session.get('current_question', 0)
        
        # Store the answer
        if answer:
            request.session['answers'][str(question_id)] = answer
            question = questions[current_index]
            
            # Check if answer is correct and update score
            if answer == question.correct_answer:
                request.session['score'] = request.session.get('score', 0) + 1
        
        # Move to next question
        current_index += 1
        request.session['current_question'] = current_index
        request.session.modified = True
        
        # Check if quiz is completed
        if current_index >= len(questions):
            return redirect('results')
        
        # Display next question
        return render(request, 'quiz.html', get_quiz_context(request, questions))


def get_quiz_context(request, questions):
    """
    Helper function to build context dictionary for quiz template.
    
    This function calculates the current question, progress percentage,
    and prepares all necessary data for the quiz template rendering.
    
    Args:
        request (HttpRequest): The HTTP request object (for session access)
        questions (list): List of all Question objects
        
    Returns:
        dict: Context dictionary containing:
            - question: Current Question object
            - question_number: 1-based question index
            - total_questions: Total number of questions
            - progress: Percentage of quiz completion (0-100)
            - options: Formatted answer options for current question
    """
    current_index = request.session.get('current_question', 0)
    
    # Safeguard against invalid indices
    if current_index >= len(questions):
        return redirect('results')
    
    current_question = questions[current_index]
    
    # Calculate progress as percentage (0-100)
    progress = ((current_index + 1) / len(questions)) * 100
    
    return {
        'question': current_question,
        'question_number': current_index + 1,
        'total_questions': len(questions),
        'progress': progress,
        'options': current_question.get_options(),
    }


@require_http_methods(["GET"])
def results(request):
    """
    Results Page View
    =================
    Displays the final quiz results with a romantic personalized message
    based on the user's score.
    
    Features:
    - Display final score and percentage
    - Show romantic congratulations message (in Arabic and English)
    - Provide detailed feedback based on performance
    - Offer options to retake quiz or return home
    - Clear session data for security
    
    Score-based Messages:
    - 100%: Perfect score message
    - 80-99%: Excellent performance message
    - 60-79%: Very good performance message
    - Below 60%: Encouraging message
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered results.html template
    """
    # Retrieve score and total questions from session
    score = request.session.get('score', 0)
    total = Question.objects.count()
    
    # Redirect home if no questions or session data
    if total == 0:
        return redirect('home')
    
    # Calculate percentage
    percentage = (score / total) * 100 if total > 0 else 0
    
    # Select romantic message based on performance
    if percentage == 100:
        # Perfect score - highest praise
        message = "مثالي! أنتِ رائعة! ♥️ أنا أحبك كثيراً!"
        message_en = "Perfect! You're amazing! ♥️ I love you so much!"
    elif percentage >= 80:
        # Excellent performance
        message = "ممتاز! أنتِ ذكية جداً! ♥️ أحبك!"
        message_en = "Excellent! You're so smart! ♥️ I love you!"
    elif percentage >= 60:
        # Very good performance
        message = "جيد جداً! أنتِ رائعة! ♥️"
        message_en = "Very Good! You're wonderful! ♥️"
    else:
        # Encouraging message
        message = "محاولة جيدة يا عزيزتي! ♥️ نحن معاً أقوى!"
        message_en = "Good try, my dear! ♥️ We're stronger together!"
    
    # Prepare context data
    context = {
        'score': score,
        'total': total,
        'percentage': percentage,
        'message': message,
        'message_en': message_en,
    }
    
    # Clear session data for security (remove after rendering)
    request.session.flush()
    
    return render(request, 'results.html', context)


@require_http_methods(["GET", "POST"])
def manager_login(request):
    """
    Manager Login - Password Protected
    ===================================
    Verify manager password before accessing manager page.
    
    GET: Display login form
    POST: Verify password
    """
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        
        if password == MANAGER_PASSWORD:
            # Set session flag for manager access
            request.session['manager_access'] = True
            request.session['manager_access_time'] = str(__import__('datetime').datetime.now())
            return redirect('manager')
        else:
            context = {'error': 'كلمة المرور غير صحيحة!'}
            return render(request, 'manager_login.html', context)
    
    return render(request, 'manager_login.html')


@require_http_methods(["GET", "POST"])
def manager(request):
    """
    Manager Page - Add/Delete Questions
    ====================================
    Simple admin interface to add and delete questions.
    
    GET: Display all questions and form to add new ones
    POST: Add new question or delete existing one
    """
    # Check if user is authenticated
    if not request.session.get('manager_access'):
        return redirect('manager_login')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Add new question
            question_text = request.POST.get('question_text', '').strip()
            question_type = request.POST.get('question_type', 'MCQ')
            
            if question_text:
                # Get the next order number
                max_order = Question.objects.aggregate(models.Max('order'))['order__max'] or 0
                
                if question_type == 'MCQ':
                    option_a = request.POST.get('option_a', '').strip()
                    option_b = request.POST.get('option_b', '').strip()
                    option_c = request.POST.get('option_c', '').strip()
                    option_d = request.POST.get('option_d', '').strip()
                    correct_answer = request.POST.get('correct_answer', 'A')
                    
                    if all([option_a, option_b, option_c, option_d]):
                        Question.objects.create(
                            text=question_text,
                            question_type='MCQ',
                            option_a=option_a,
                            option_b=option_b,
                            option_c=option_c,
                            option_d=option_d,
                            correct_answer=correct_answer,
                            order=max_order + 1
                        )
                else:  # True/False
                    correct_answer = request.POST.get('correct_answer', 'True')
                    Question.objects.create(
                        text=question_text,
                        question_type='TF',
                        correct_answer=correct_answer,
                        order=max_order + 1
                    )
                
                return redirect('manager')
        
        elif action == 'delete':
            # Delete question
            question_id = request.POST.get('question_id')
            try:
                Question.objects.get(id=question_id).delete()
            except Question.DoesNotExist:
                pass
            return redirect('manager')
    
    # Get all questions
    questions = Question.objects.all().order_by('order')
    
    context = {
        'questions': questions,
        'total_questions': questions.count(),
    }
    
    return render(request, 'manager.html', context)


@require_http_methods(["GET"])
def manager_logout(request):
    """
    Manager Logout
    ==============
    Clear manager session and redirect to home.
    """
    request.session.pop('manager_access', None)
    request.session.pop('manager_access_time', None)
    return redirect('home')


