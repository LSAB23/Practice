from django import forms

class quiz(forms.Form):
    quiz_name = forms.CharField(label='Name of Test: ', widget=forms.TextInput(attrs={'placeholder': 'Enter the name you want the quiz to have ..'}))

class ques(forms.Form):
    question = forms.CharField(label='Question :', widget=forms.Textarea(attrs={'rows':'2', 'placeholder':'hello'}))
    ques_image = forms.ImageField(label='Add image')

class ques_no_image(ques):
    ques_image = None

class ans(forms.Form):
    answer = forms.CharField(label='Answer: ')
    ans_img = forms.ImageField(label='Add Image (Answer):')

class ans_text(ans):
    ans_img = None

class ans_image(ans):
    answer = None

class correct_ans(forms.Form):
    correct_answer = forms.CharField(label='Correct Answer')
    correct_img = forms.ImageField(label='Add Image(correct answer)')

class correct_ans_text(correct_ans):
    correct_img = None
    
class correct_ans_image(correct_ans):
    correct_answer = None