from apps.rundeck.models import Jobs
from apps.rundeck.api import RundeckClient
import unicodedata

dict_queries = {
    "saudation": {
        "input": ["Olá", "Tudo bem?", "Bom dia", "Boa Tarde", "Boa Noite"],
        "output": "Opa, fala comigo! Estou aqui para ajudar",
    },
    "explanation": {
        "input": ["para que você serve?", "qual a sua utilidade?", "quem é você?", "quem é vc?"],
        "output": "Eu sou um bot. Minha função é ajudar! Posso fazer deploy de ambientes. Basta me pedir!"
    },
    "command_list_enviroment": {
        "input": ["quais os ambientes?", "quais os projetos?"],
        "output": ""
    },
    "command_deploy": {
        "input": [],
        "output": "vamos fazer"
    },
}

def get_type_conversation(text):
    term = __text(text)
    if str(term[0:6], 'utf-8') == "deploy":
        return "command_deploy"

    for key, value in dict_queries.items():
        if term in dict_unaccent(value.get("input", [])):
            return key

    return None

def get_answer_for_type(type, term=""):

    if type == "command_list_enviroment":

        jobs = Jobs.objects.filter(use_chatbot=True)

        response_text = "os ambiente disponiveis são: \n\n"

        for job in jobs:
            response_text += "Nome: {}\nDescrição: {}\n\n".format(job.name, job.description)

        return response_text

    elif type == "command_deploy":

        job_name = extract_project_from_term(term)

        job = Jobs.objects.filter(name=job_name, use_chatbot=True)

        if not job.exists():
            return "Não pude encontrar o projeto: {}".format(job_name)

        job = job.first()

        rundeckcli = RundeckClient()
        rundeckcli.run_job(job.id)

        return "Já iniciamos o procedimento de deploy"

    else:
        try:
            return dict_queries.get(type).get("output")
        except:
            return None

def extract_project_from_term(term):
    return term.replace("deploy ", "").strip()

def __text(accented_string):
    return unicodedata.normalize('NFKD', accented_string).encode('ASCII', 'ignore').lower()

def dict_unaccent(dict):
    result = []
    for value in dict:
        result.append(__text(value))

    return result