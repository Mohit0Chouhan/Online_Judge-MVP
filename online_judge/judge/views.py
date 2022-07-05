from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from distutils.command.upload import upload
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render ,redirect
import subprocess
import filecmp
from judge.models import Problem, Solution, Test
from judge.helper import save_submission
from django.core.files import File

# Create your views here.
def index(request):
    return render(request , 'index.html')

def problems(request):
    problems = Problem.objects.all()
    return render(request , 'problems.html' , { 'problems' : problems})

def problem(request , problem_id):
    problem = get_object_or_404(Problem , pk=problem_id)
    context = {
        'problem':problem
    }
    return render(request, 'problem.html', context)
        
    

# def submit(request , pid):
#     # fetch problem object using pid and then test with problem_name
#     problem = Problem.objects.get(pk=pid)
#     test = Test.objects.get(problem__problem_name=problem.problem_name)
#     # checking method
#     if request.method == 'POST':
#         sol =save_submission(request , problem)
#         if not sol :
#             return HttpResponseRedirect('/judge/problem/' + str(pid))

#         sol_id = sol.id

#         name = sol.code_file.url
#         s_file = 'media/' + name
#         outfile = 'm.exe'
#         inputfile = 'media/' + test.test_input.url
#         testout = 'media/' + test.test_output.url

#         subprocess.call(["g++",s_file,"-o",outfile],shell=True)
#         k = subprocess.call(["output.exe"],stdin=inputfile ,stdout='media/out_file/p_output.txt',shell=True)
#         # os.system('g++ ' + s_file + ' -o ' + outfile)
#         # os.system('echo Evaluating your code..... ')
#         # os.system(outfile + ' < ' + inputfile + ' > media/out_file/p_output.txt')
#         result = filecmp.cmp('media/out_file/p_output.txt', testout, shallow=False)
#         subprocess.call(['del','m.exe'])
#         if result:
#             Solution.objects.filter(id=sol_id).update(verdict='AC')
#             return HttpResponse("Hurray!! You are doing great today. Keep it Up")
#         else:
#             Solution.objects.filter(id=sol_id).update(verdict='WA')
#             return HttpResponse("Failure is not an end of the world")
        
#     else:
#         return HttpResponse("Usage: Message used is not POST.")


def submit(request , pid):
    # fetch problem object using pid and then test with problem_name
    problem = Problem.objects.get(pk=pid)
    test = Test.objects.get(problem__problem_name=problem.problem_name)
#     # checking method
    if request.method == 'POST':
        # fetching file and code submitted by user
        user_codefile = request.FILES.get('codeFile', False)
        codeInEditor = request.POST.get('codeEditor', False)
        if user_codefile:
            codefile_content = user_codefile.read()
            with open('temp.cpp' , 'wb+') as temp_code:
                temp_code.write(codefile_content)
            temp_code.close()
            # inputfile = 'media/' + test.test_input.url
            out_container = open('mohit.txt' , 'w')
            testout = 'media/' + test.test_output.url
            subprocess.call(["g++","temp.cpp","-o","temp.exe"],shell=True)
            k = subprocess.call(['temp.exe'],stdin=test.test_input ,stdout=out_container,shell=True)
            out_container.close()
            if k:
                # mo = open(inputfile , 'r')
                # errorContent = mo.read()
                # mo.close()
                return HttpResponse(k.stdout)
            else:
                result = filecmp.cmp('mohit.txt', testout, shallow=False)
                if result:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='AC'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/judge/submit/correct_ans/")
                else:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='WA'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/judge/submit/wrong_ans/")
        elif codeInEditor:
            
            byte_content = codeInEditor.encode()
            with open('temp.cpp' , 'wb+') as temp_code:
                temp_code.write(byte_content)
            temp_code.close()
            # inputfile = 'media/' + test.test_input.url
            out_container = open('mohit.txt' , 'w')
            testout = 'media/' + test.test_output.url
            subprocess.call(["g++","temp.cpp","-o","temp.exe"],shell=True)
            k = subprocess.call(['temp.exe'],stdin=test.test_input ,stdout=out_container , stderr=out_container,shell=True)
            out_container.close()
            if k :
                # mo = open(inputfile , 'r')
                # errorContent = mo.read()
                # mo.close()
                return HttpResponse('Internal error occur!!')
            else:
                result = filecmp.cmp('mohit.txt', testout, shallow=False)
                if result:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='AC'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/judge/submit/correct_ans/")
                else:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solution(
                        problem=problem,
                        language=request.POST['language'],
                        code_file=myfile,
                        verdict='WA'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/judge/submit/wrong_ans/")
            # return HttpResponse('Yep! I got your code')
        else:
            return HttpResponse('No code file uploaded!!')
    else:
        return HttpResponse('Usage: Post method is not used.')



def result(request , status):
    context = {
        'status':status
    }
    return render(request ,'submit.html' , context)

def submissions(request):
    submissions = Solution.objects.all().order_by('-id')[:10]
    return render(request,'submissions.html' , {'submissions' : submissions})



def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request,"register.html", context={"register_form":form})