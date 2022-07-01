import cProfile
import imp
from django.http import HttpResponse
from django.shortcuts import render
import os
import filecmp
from .forms import Submission_form
from judge.models import Problem, Solution
from django.core.files.storage import default_storage

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
        'problem':problem
    }
    return render(request, 'problem.html', context)
        
    

def submit(request , pid):
    problem = Problem.objects.get(pk=pid)
    if request.method == 'POST':
        file = request.FILES['codefile']
        sol = Solution(
            problem=problem,
            language=request.POST['language'],
            code_file=file,
            verdict='PS'
        )
        sol.save()

        name = sol.code_file.url
        # name = s_file[0]
        # extn = s_file[1]
        s_file = 'media/' + name
        outfile = 'm.exe'

        inputfile = 'media/test_inputs/count_anagrms.txt'
        os.system('g++ ' + s_file + ' -o ' + outfile)
        os.system('echo Evaluating your code..... ')
        os.system(outfile + ' < ' + inputfile + ' > media/out_file/p_output.txt')
        # with open('p_output.txt' , 'r') as src:
        #     with open('media/test_outputs/count.txt' , 'r') as dest:
        #         src_cont = src.read()
        #         dest_cont = dest.read()
        result = filecmp.cmp('media/out_file/p_output.txt', 'media/test_outputs/count.txt', shallow=False)
        # os.system('del media\out_file\p_output.txt')
        os.system('del m.exe')
        if result:
            sol.verdict = 'AC'
            return HttpResponse("Hurray!! You are doing great today. Keep it Up")
        else:
            sol.verdict = 'WA'
            return HttpResponse("Failure is not an end of the world")
        
    else:
        return HttpResponse("method is not post")

