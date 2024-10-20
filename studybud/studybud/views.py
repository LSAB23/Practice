from django.shortcuts import render, HttpResponse, redirect
from .forms import quiz, ques, ques_no_image, ans_text, correct_ans_text, ans_img_text, ans_image, correct_ans_image, correct_ans, ans
from .models import Quiz, Questions, Answers
from django.urls import reverse
from secrets import choice
from string import hexdigits
from .deleteimg import delete_image

def id_gen(number=7):
    id = ''
    for len in range(number):
        id += choice(hexdigits)
    return id

def home(request):

    quiz_form  = quiz()
    quizes = Quiz.objects.all()
    if request.method == 'POST':
        valid = quiz(request.POST).is_valid()
        if valid:
            quiz_id = id_gen()
            quiz_name = request.POST['quiz_name']
            user = request.user
            try:
                Quiz.objects.create(user=user, quiz_id=quiz_id, quiz_name=quiz_name).save()
            except Exception as e:
                error = repr(e)
                if error ==  'UNIQUE constraint failed: studybud_quiz.quiz_id':
                    quiz_id = id_gen()
                    Quiz.objects.create(user=user, quiz_id=quiz_id, quiz_name=quiz_name).save()
                if error == 'UNIQUE constraint failed: studybud_quiz.quiz_name':
                    quiz_name = quiz_name + id_gen(3)
                    Quiz.objects.create(user=user, quiz_id=quiz_id, quiz_name=quiz_name).save()
        return HttpResponse('Quiz Created you can now add questions')
    return render(request, 'home.html', {'quiz_form':quiz_form, 'quizes': quizes})

def add_questions(request, quiz_id):
    check_exist = Quiz.objects.filter(quiz_id=quiz_id).exists()
    if not check_exist:
        return HttpResponse(f'You have to create a test first at <a href="{request.build_absolute_uri(reverse('home'))}">This Link</a>')
    
    question = ques_no_image()
    answer = ans_text()
    correct_answer = correct_ans_text()
    questions = Questions.objects.filter(quiz_id=quiz_id).all()
    if request.method == 'POST':
        post_info = request.POST
        images = request.FILES
        anss = post_info.getlist('answer')
        anss_with_image = post_info.getlist('answer_with_image')
        correct_anss = post_info.get('correct_answer')
        join_answers = anss + anss_with_image

        # validate the forms before it start to create the question and answers
        if ques_no_image(post_info).is_valid() and ans_text(post_info).is_valid() and correct_ans_text(post_info).is_valid() or ques(post_info).is_valid() or ans(post_info).is_valid() or correct_ans(post_info).is_valid() or ans_img_text(post_info) or correct_ans_image(post_info).is_valid() or ans_image(post_info).is_valid():
            
            if correct_anss in join_answers:
                ques_id = id_gen()
                quess = post_info.get('question')
                ques_image = post_info.get('image')
                quiz_inst = Quiz(quiz_id=quiz_id)
                ques_inst = Questions(ques_id=ques_id)
                
                answer_image = images.getlist('ans_img')

                correct_ans_img = images.get('correct_img')
                
                # Create answers with images
                if answer_image:
                    if len(anss_with_image) == len(answer_image):
                        Questions.objects.create(quiz_id=quiz_inst, ques_id=ques_id,ques=quess, ques_image=ques_image).save()
                        for anss_,image_ in list(zip(anss_with_image, answer_image)):
                            ans_id = id_gen()
                            Answers.objects.create(ans_id=ans_id, quiz_id=quiz_inst, ques_id=ques_inst,ans=anss_,ans_image=image_).save()
                    else:
                        return HttpResponse('Check the form images and try again')
                else:
                    # Create question
                    Questions.objects.create(quiz_id=quiz_inst, ques_id=ques_id,ques=quess, ques_image=ques_image).save()

                # Create answers
                for answer in anss:
                    ans_id = id_gen()
                    Answers.objects.create(ans_id=ans_id, quiz_id=quiz_inst, ques_id=ques_inst,ans=answer,ans_image=None).save()

                # Add Correct answer 
                ans_id = id_gen()
                Answers.objects.create(ans_id=ans_id, quiz_id=quiz_inst, ques_id=ques_inst, ans=correct_anss,ans_image=correct_ans_img, ans_correct=True).save()

                return render(request, 'question.html', {'ques_id':ques_id, 'quess':quess})
            else:
                return HttpResponse('Correct answer is not in answers')
        else:
            return HttpResponse('Try checking your input and try again or the file size of your image')
    context = {
        'question': question,
        'quiz_id': quiz_id,
        'answer': answer,
        'correct': correct_answer,
        'questions': questions,
    }
    return render(request, 'add_ques.html', context)

def edit_question(request, ques_id):
    ques_query = Questions.objects.select_related().filter(ques_id=ques_id)
    if request.method == 'POST':
        print(ques_no_image(request.POST).is_valid(),)
        return HttpResponse('it works')
    if not ques_query.exists():
        return redirect('/')
    context = {
        'ques':ques_query,
        'ques_id':ques_id,
    }
    return render(request, 'edit_question.html', context=context)

def get_form(request, what_form):
    forms = {
        'ques':ques(),
        'text_ans':ans_text(),
        'ans_with_image':ans_img_text(),
        'correct_ans_img_only': correct_ans_image(),
        'correct_ans': correct_ans(),
    }
    get_form = forms.get(what_form)
    if get_form:
        return HttpResponse(f'{get_form}')
    return HttpResponse('Form do not exist')

def delete(request, type, id):
    if type == 'quiz':
        Quiz.objects.filter(quiz_id=id).delete()
        return HttpResponse('Quiz Deleted')
    if type == 'question':
        Questions.objects.filter(ques_id=id).delete()
        return HttpResponse('Question Deleted')