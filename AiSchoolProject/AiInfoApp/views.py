from django.shortcuts import render, redirect
from .models import AiClass, AiStudent
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def home(request):
    class_obj_list = AiClass.objects.all()

    context = {
        'class_obj_list': class_obj_list
    }
    return render(request, 'home.html', context)


# url patterns 에 있는 변수명과 일치해야한다 !
def detail(request, class_pk):
    # class_pk에 해당하는 학생들을 가져온다 ( 그 반에 속해있는 학생 )
    student_obj_list = AiStudent.objects.filter(class_num=class_pk)

    context = {
        'class_pk': class_pk,
        'student_obj_list': student_obj_list
    }
    return render(request, 'detail.html', context)


def add(request, class_pk):
    # add 로 도착하는 요청은 두 개 다! 나눠서 처리하기 위해서 조건문을 활용한다.

    # add/ 에서 form request가 왔을 때 (두번째 POST 요청)
    if request.method == 'POST':
        # 데이터베이스에 데이터를 추가하자
        AiStudent.objects.create(
            class_num=class_pk,
            name=request.POST['name'],
            phone_num=request.POST['phone_num'],
            intro=request.POST['intro'],
        )

        return redirect('detail', class_pk)

    # detail/ 에서 add로 넘어올 때 (첫번째 GET 요청)
    context = {
        'class_pk': class_pk
    }
    return render(request, 'add.html', context)

def student(request, student_pk):
    
    student = AiStudent.objects.get(pk=student_pk)

    context = {
        'student' : student
    }

    return render(request, 'student.html', context)

def edit(request, student_pk):

    if request.method == 'POST':

        AiStudent.objects.filter(pk=student_pk).update(
            name = request.POST['name'],
            phone_num = request.POST['phone_num'],
            intro = request.POST['intro'],
        )

        return redirect('student', student_pk)

    student = AiStudent.objects.get(pk=student_pk)

    context = {
        'student' : student
    }

    return render(request, 'edit.html', context)

def delete(request, class_num, student_pk):

    target_student = AiStudent.objects.get(pk=student_pk)
    target_student.delete()

    class_pk = class_num

    return redirect('detail', class_pk)

ERROR_MSG = {
    'ID_EXIST' : '이미 사용중인 아이디입니다.',
    'ID_NOT_EXIST' : '존재하지 않는 아이디입니다.',
    'ID_PW_MISSING' : '아이디와 비밀번호를 다시 확인해주세요.',
    'PW_CHECK' : '비밀번호가 일치하지 않습니다.',
}

def signup(request) :

    context = {
        'error' : {
            'state' : False,
            'msg' : ''
        }
    }

    if request.method == 'POST':

        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) == 0:
                if (user_pw == user_pw_check):

                    user = User.objects.create_user(
                        username=user_id,
                        password=user_pw
                    )

                    auth.login(request, user)

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']

            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']

        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'signup.html', context)

def login(request):

    context = {
        'error' : {
            'state' : False,
            'msg' : ''
        }
    }

    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) != 0:

                user = auth.authenticate(
                    username=user_id,
                    password=user_pw
                )

                if user != None:
                    auth.login(request, user)

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']

            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']

        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'login.html', context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)

    return redirect('home')