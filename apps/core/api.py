from apps.rundeck.models import Jobs, JobStatus
from apps.rundeck.api import RundeckClient
from django.db.models import Q
from django.conf import settings
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

def get_answer_for_type(type, term="", message_user_id=None):

    if type == "command_list_enviroment":

        jobs = Jobs.objects.filter(use_chatbot=True)

        response_text = "os ambiente disponiveis são: \n\n"

        for job in jobs:
            response_text += "Nome: {}\nDescrição: {}\n\n".format(job.name, job.description)

        return response_text, None

    elif type == "command_deploy":

        job_name = extract_project_from_term(term)

        job = Jobs.objects.filter(name=job_name, use_chatbot=True)

        if not job.exists():
            return "Não pude encontrar o projeto: {}".format(job_name), None

        job = job.first()
        run_job(job, message_user_id)

        return "<@{}> iniciamos o seu deploy. Assim que terminarmos, te avisaremos".format(message_user_id), \
               "O usuario <@{}> solicitou deploy.".format(message_user_id)

    else:
        try:
            return dict_queries.get(type).get("output"), None
        except:
            return None, None

def extract_project_from_term(term):
    return term.replace("deploy ", "").strip()

def __text(accented_string):
    return unicodedata.normalize('NFKD', accented_string).encode('ASCII', 'ignore').lower()

def dict_unaccent(dict):
    result = []
    for value in dict:
        result.append(__text(value))

    return result

def run_job(job, message_user_id):
    rundeckcli = RundeckClient()
    job_run = rundeckcli.run_job(job.id)

    jobstatus = JobStatus()
    jobstatus.id = job_run.get("id")
    jobstatus.permalink = job_run.get("permalink")
    jobstatus.status = job_run.get("status")
    jobstatus.project = job_run.get("project")
    jobstatus.job = job
    jobstatus.message_id = "slack"
    jobstatus.message_origin_user_id = message_user_id
    jobstatus.message_notified = False
    jobstatus.save()

def report_job_status(client):
    jobs = JobStatus.objects.filter(Q(status="succeeded") | Q(status="failed"), message_notified=False)

    for job in jobs:

        if job.status == "succeeded":
            answer_user = "<@{}> o deploy foi realizado com sucesso!".format(job.message_origin_user_id)
            answer_log = "O deploy solicitado por <@{}> foi realizado com sucesso!".format(job.message_origin_user_id)
        else:
            answer_user = "<@{}> tivemos um problema com seu deploy, não conseguimos finalizar, não entre em desespero, já notifiquei a equipe responsavel.".format(job.message_origin_user_id)
            answer_log = "Moçada, temos um problema, O deploy solicitado por <@{}> teve sucesso. O link para consulta é: {}".format(job.message_origin_user_id, job.permalink)

        client.rtm_send_message(
            settings.SLACK_CHANNEL_ID,
            answer_user
        )

        if settings.SLACK_DEPLOY_CHANNEL_ID != "":
            client.rtm_send_message(
                settings.SLACK_DEPLOY_CHANNEL_ID,
                answer_log
            )

        job.message_notified = True
        job.save()

def update_jobs_status():
    jobs = JobStatus.objects.filter(status="running", message_notified=False)

    rundeckcli = RundeckClient()

    for job in jobs:
        job_data = rundeckcli.get_job_status(job.id)

        job.status = job_data.get("status")
        job.save()