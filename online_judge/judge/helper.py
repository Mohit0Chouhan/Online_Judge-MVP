from asyncio import subprocess
from judge.models import Solution
from django.core.files.base import ContentFile, File


def save_submission(request , problem):
    file = request.FILES.get('codeFile', False)
    code = request.POST.get('codeEditor', False)
    if file:
        sol = Solution(
            problem=problem,
            language=request.POST['language'],
            code_file=file,
            verdict='PS'
        )
        sol.save()
        return sol
    elif code:
        language_map = {'c++': '.cpp', 'java': '.java', 'c': '.c'}
        lang = request.POST['language']
        name = 'temp_code' + language_map[lang]
        temp_file = open(name , 'w')
        temp_file.write(code)
        sol = Solution(
            problem=problem,
            language=request.POST['language'],
            code_file=temp_file,
            verdict='PS'
        )
        sol.save()
        temp_file.close()
        return sol


def run(name , extn):
    file = name+extn
    subprocess.call(["g++","sum.cpp","-o","output.exe"],shell=True)
    k = subprocess.call(["output.exe"],stdout=file,shell=True)