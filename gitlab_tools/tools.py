import os
import gitlab
from dotenv import load_dotenv
from llm_utils.langchain_utils import get_llm

env_path = "../.env"

load_dotenv(dotenv_path=env_path)
llm = get_llm()

GL = gitlab.Gitlab(url=os.getenv("GITLAB_URL"), private_token=os.getenv("PRIVATE_TOKEN"))
PROJECT = GL.projects.get(os.getenv("PROJECT_ID"))

def get_opened_issues() -> str:
    """
    Função que deve ser chamada quando queremos saber sobre as tarefas em aberto
    """

    issues = PROJECT.issues.list(state="opened", all=True)

    relatorio = "As issues abertas do projeto sao:\n"

    for issue in issues:
        relatorio += f"ID da tarefa: {issue.iid}\n"
        relatorio += f"Título: {issue.title}\n"
        relatorio += f"Descrição: {issue.description}\n"
        relatorio += "----------------------------------------\n"

    return relatorio

def issue_spent_time(issue_id: int, spent_time: str) -> str:
    """
    Função que vai ser chamada quando quisermos dizer quanto tempo levou para ser finalizada.
    O tempo é uma string e deve ser formatado de acordo com o padrão do Gitlab.
    Exemplo: 1d2h3m.
    Args:
        issue_id (int): ID da issue
        spent_time (str): Tempo gasto na issue
    """

    issue = PROJECT.issues.get(issue_id)
    issue.add_spent_time(spent_time)

    issue.save()

    return f"Tempo gasto foi adicionado ao gilab."

