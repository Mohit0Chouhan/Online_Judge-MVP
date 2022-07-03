from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os
import subprocess
import filecmp
from judge.models import Problem, Solution, Test
from judge.helper import save_submission

# Create your views here.
def index(request):
    return render(request , 'index.html')

def problems(request):
    problems = Problem.objects.all()
    return render(request , 'problems.html' , { 'problems' : problems})

# def (request , problem_id):
#     problem = Problem.objects.get(pk = problem_id)
#     return render(request , 'problem.html' , { 'problem': problem} )


def problem(request , problem_id):
    problem = Problem.objects.get(pk = problem_id)
    context = {
        'problem':problem,
        'msg':''
    }
    return render(request, 'problem.html', context)
        
    

def submit(request , pid):
    problem = Problem.objects.get(pk=pid)
    test = Test.objects.get(problem__problem_name=problem.problem_name)
    if request.method == 'POST':
        # file = request.FILES['codefile']
        # sol = Solution(
        #     problem=problem,
        #     language=request.POST['language'],
        #     code_file=file,
        #     verdict='PS'
        # )
        # sol.save()
        sol =save_submission(request , problem)
        if not sol :
            problem = Problem.objects.get(pk = pid)
            context = {
                'problem':problem,
                'msg':'Please select a file!!!'
            }
            return render(request, 'problem.html', context)

        sol_id = sol.id

        name = sol.code_file.url
        s_file = 'media/' + name
        outfile = 'm.exe'
        inputfile = 'media/' + test.test_input.url
        testout = 'media/' + test.test_output.url

        subprocess.call(["g++",s_file,"-o",outfile],shell=True)
        k = subprocess.call(["output.exe"],stdin=inputfile ,stdout='media/out_file/p_output.txt',shell=True)
        # os.system('g++ ' + s_file + ' -o ' + outfile)
        # os.system('echo Evaluating your code..... ')
        # os.system(outfile + ' < ' + inputfile + ' > media/out_file/p_output.txt')
        result = filecmp.cmp('media/out_file/p_output.txt', testout, shallow=False)
        # os.system('del media\out_file\p_output.txt')
        # os.system('del m.exe')
        subprocess.call(['del','m.exe'])
        if result:
            Solution.objects.filter(id=sol_id).update(verdict='AC')
            return HttpResponse("Hurray!! You are doing great today. Keep it Up")
        else:
            Solution.objects.filter(id=sol_id).update(verdict='WA')
            return HttpResponse("Failure is not an end of the world")
        
    else:
        return HttpResponse("method is not post")

