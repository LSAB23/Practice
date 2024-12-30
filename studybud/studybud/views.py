from django.shortcuts import render, HttpResponse, redirect
from simple.models import UserModels
from .forms import quiz, ques, ques_no_image, ans_text, correct_ans_text, ans_img_text, ans_image, correct_ans_image, correct_ans, ans
from .models import Quiz, Questions, Answers, Report
from django.urls import reverse
from .deleteimg import delete_image
from itertools import zip_longest
from django.template.loader import render_to_string
from simple.views import login_required, generate_username


def id_gen(number=7):
    id = generate_username(number)
    return id

def validate_input(post_info):
    return  ques_no_image(post_info).is_valid() and ans_text(post_info).is_valid() and correct_ans_text(post_info).is_valid() or ques(post_info).is_valid() or ans(post_info).is_valid() or correct_ans(post_info).is_valid() or ans_img_text(post_info) or correct_ans_image(post_info).is_valid() or ans_image(post_info).is_valid()



@login_required
def home(request,  user=None,*args):

    quiz_form  = quiz()
    quizzes = Quiz.objects.filter(user=user).all()
    

    if request.method == 'POST':
        valid = quiz(request.POST).is_valid()
        if valid:
            quiz_id = id_gen()
            quiz_name = request.POST['quiz_name']
            try:
                
                Quiz.objects.create(user=user, quiz_id=quiz_id, quiz_name=quiz_name).save()
                
                return render(request, 'test_created.html', {'quiz_name':quiz_name,'quiz_id':quiz_id})
            except Exception as e:
                error = e.args[0]
                if error ==  'UNIQUE constraint failed: studybud_quiz.quiz_id':
                    quiz_id = id_gen()
                    Quiz.objects.create(user=user, quiz_id=quiz_id, quiz_name=quiz_name).save()
                    return render(request, 'test_created.html', {'quiz_name':quiz_name,'quiz_id':quiz_id})

                if error == 'UNIQUE constraint failed: studybud_quiz.quiz_name':
                    quiz_name = quiz_name + id_gen(3)
                    Quiz.objects.create(user=user, quiz_id=quiz_id, quiz_name=quiz_name).save()
                    return render(request, 'test_created.html', {'quiz_name':quiz_name,'quiz_id':quiz_id})
            return 
    return render(request, 'home.html', {'quiz_form':quiz_form, 'quizes': quizzes})

@login_required
def add_questions(request, user=None,*args, **kwargs):
    quiz_id = kwargs.get('quiz_id')
    check_exist = Quiz.objects.filter(quiz_id=quiz_id,user=user).exists()

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
        if validate_input(post_info):
            
            if correct_anss not in join_answers:
                ques_id = id_gen()
                quess = str(post_info.get('question'))
                ques_image = images.get('ques_image')
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
                return HttpResponse('Correct answer is in answers')
        else:
            return HttpResponse('Try checking your input and try again or the file size of your image')
    context = {
        'question': question,
        'quiz_id': quiz_id,
        'answer': answer,
        'correct': correct_answer,
        'questions': questions,
        'can_practice': True,
        'quiz_id': quiz_id,
    }
    return render(request, 'add_ques.html', context)



@login_required
def edit_question(request, user=None,*args, **kwargs):
    ques_id = kwargs.get('ques_id')
    
    ques_query = Questions.objects.select_related().filter(ques_id=ques_id)
    if request.method == 'POST':
        post_info = request.POST
        images = request.FILES
        if validate_input(post_info):
            quiz_id=post_info.get('quiz_id')
            # edit quetions
            ques_edit = str(post_info.get('question')).strip()
            ques_edit_image = images.get('image')
            ques_id = post_info.get('ques_id')

            # edit correct answer
            correct_ans_edit = post_info.get('correct_answer')
            correct_ans_id = post_info.get('correct_ans_id')
            
            # edit answers
            ans_edit= post_info.getlist('answer')

            if correct_ans_edit in ans_edit:
                return HttpResponse('Correct answer is in answers')
            if ques_edit_image:
                Questions.objects.filter(ques_id=ques_id).update(ques=ques_edit, ques_image=ques_edit_image)

            Questions.objects.filter(ques_id=ques_id).update(ques=ques_edit)
            answers = list(zip_longest(post_info.getlist('ids'), ans_edit, fillvalue=None))
            quiz_inst = Quiz(quiz_id=quiz_id)
            ques_inst = Questions(ques_id=ques_id)
            for id,answer_edit in answers:
                # update_or_create was causing integrity errors so i used this instead
                id = id
                if id is None:

                    Answers.objects.create(ans_id=id_gen(),quiz_id=quiz_inst,ques_id=ques_inst,ans=answer_edit,ans_image=None).save()
                else:
                    Answers.objects.filter(ans_id=id).update(ans=answer_edit)
            if correct_ans_id:
                Answers.objects.filter(ans_id=id).update(ans=correct_ans_edit)
            
            return HttpResponse('Update Done')
        return HttpResponse('Error check your inputs')
    if not ques_query:
        return redirect('/')
    quiz_id = ques_query.values()[0].get('quiz_id_id')
    
    context = {
        'ques':ques_query,
        'id':ques_id,
        'quiz_id':quiz_id,
        'can_practice': True,
        'quiz_id': quiz_id,

    }
    return render(request, 'edit_question.html', context)

@login_required
def practice(request, user=None,*args, **kwargs):
    quiz_id = kwargs.get('quiz_id')
    quiz_filter = Quiz.objects.filter(quiz_id=quiz_id, user=user).prefetch_related()

    if request.POST:
        flip = request.POST.get('flip')
        test = request.POST.get('test')
        if test:
            context = {
                'quiz': quiz_filter.all(),
            }
            return render(request, 'practice_test.html', context)
        
        return HttpResponse('Feature Not yet implemeted')
    if quiz_filter.exists():
        context = {
            'quiz_id':quiz_id,
        }
        return render(request, 'practice.html', context)
    return redirect('/')

@login_required
def check_answer(request, user=None,*args):
    post_info = request.POST
    lst_template = []
    correct = []
    correct_len = 0
    wrong = []
    wrong_len = 0
    anss = ''
    if post_info:
        question = post_info.getlist('question')
        filters = Answers.objects.filter(ques_id__in = question).select_related().all()
        for ques in question:
            for answer in filters:
                if answer.ans_correct:
                    anss = answer.ans
                    quiz_id=answer.quiz_id
                
                if answer.ques_id.ques_id == ques:
                    chosen_answer  = post_info.get(ques)
                    if chosen_answer == answer.ans_id and answer.ans_correct:
                        context = {
                        'question':answer.ques_id.ques,
                        'correct':True,
                        'answer':anss,
                    }
                        correct.append(context)
                        correct_len +=1
                        template = render_to_string('check.html', context)
                        lst_template.append(template)
                    else:
                        if chosen_answer == answer.ans_id and not answer.ans_correct:
                            chosen_answer = answer.ans
                            context = {
                                'question':answer.ques_id.ques,
                                'correct':False,
                                'answer':anss,
                                'chosen':chosen_answer,
                            }
                            wrong.append(context)
                            wrong_len+=1
                            template = render_to_string('check.html', context)
                            lst_template.append(template)
        score = f'{correct_len}/{correct_len+wrong_len}'
        Report(user=user,quiz_id=quiz_id,score=score,wrong=wrong, correct=correct, correct_len=correct_len, wrong_len=wrong_len).save()
            
        return render(request, 'results.html', {'lst_template':lst_template, 'correct_ans':correct_len, 'total':correct_len+wrong_len})
    return redirect(home)



@login_required
def report(request, user=None,*args, **kwargs):

    quiz_id = kwargs.get('quiz_id')
    get_report = Report.objects.filter(quiz_id=quiz_id, user=request.user).select_related()

    if get_report:
        return render(request, 'report.html', {'reports':get_report})
       
    return HttpResponse('No Reports')



@login_required
def get_form(request, user=None,*args, **kwargs):
    what_form = kwargs.get('what_form')

    
    forms = {
        'ques':ques(),
        'text_ans':ans_text(),
        'ans_with_image':ans_img_text(),
        'correct_ans_img_only': correct_ans_image(),
        'correct_ans': correct_ans(),
    }
    get_form = forms.get(what_form) # type: ignore
    if get_form:
        return HttpResponse(f'{get_form}')
    return HttpResponse('Form do not exist')

@login_required
def delete(request, user,*args, **kwargs):
    type = str(kwargs.get('type')).lower()
    id = kwargs.get('id')

    if type == 'quiz':
        Quiz.objects.filter(quiz_id=id, user=user).delete()
        return HttpResponse('Quiz Deleted')
    if type == 'question':
        Questions.objects.filter(ques_id=id).delete()
        return HttpResponse('Question Deleted')
    if type == 'answer':
        Answers.objects.filter(ans_id=id).delete()
        return HttpResponse('Answer Deleted')
    return 