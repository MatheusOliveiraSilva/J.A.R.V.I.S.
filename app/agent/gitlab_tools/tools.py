import os
import gitlab
from typing import Literal
from dotenv import load_dotenv
from app.agent.gitlab_tools.people_info import PEOPLE_INFO

load_dotenv(dotenv_path="../../.env")

GL = gitlab.Gitlab(url=os.getenv("GITLAB_URL"), private_token=os.getenv("PRIVATE_TOKEN"))
PROJECT = GL.projects.get(os.getenv("PROJECT_ID"))

def get_opened_issues() -> str:
    """
    Função que deve ser chamada quando queremos saber sobre as tarefas em aberto
    """

    issues = PROJECT.issues.list(state="opened", all=True)

    relatorio = "As issues abertas do projeto sao:\n"

    if not issues:
        return "Nenhuma issue aberta no momento."

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

    # Faz um assert para verificar se está no formato contendo apenas d h m além dos digitos de 0 a 9.
    if not all(c.isdigit() or c == "d" or c == "h" or c == "m" for c in spent_time):
        raise ValueError("O tempo gasto deve estar no formato contendo apenas d h m e os digitos de 0 a 9.")

    issue = PROJECT.issues.get(issue_id)
    issue.add_spent_time(spent_time)

    issue.save()

    return f"Tempo gasto foi adicionado ao gilab."

def change_assignee(issue_id: int, user_name: str) -> str:
    """
    Função que vai ser chamada quando quisermos mudar o assignee da issue.
    Assignee pode ter como sinonimo o responsavel/dono/owner da issue.
    Args:

    issue_id (int): ID da issue
    user_name (str): Nome do usuario
    """

    issue = PROJECT.issues.get(issue_id)

    if user_name.lower() not in PEOPLE_INFO:
        raise ValueError(f"O usuario {user_name} nao foi encontrado na base de dados.")

    user_info = PEOPLE_INFO[user_name.lower()][0]

    # Atualizar a issue com os novos assignees
    issue.assignee_ids = [user_info['id']]
    issue.save()

    return f"A tarefa foi designada para: {user_name}."

def change_labels(issue_id: int, new_label: Literal["To Do", "Doing", "To Review"]) -> str:
    """
    Atualiza o status de uma issue para To Do, Doing ou To Review.

    Args:
        issue_id (int): ID da issue que terá o label alterado.
        new_label (Literal["To Do", "Doing", "To Review"]): Novo label que será aplicado à issue.

    """
    issue = PROJECT.issues.get(issue_id)

    if new_label in issue.labels:
        raise ValueError(f"A issue {issue_id} ja possui o label {new_label}.")

    # Remove o label atual da issue se for um dos literais exceto o do input
    for label in issue.labels:
        if label in ["To Do", "Doing", "To Review"]:
            issue.labels.remove(label)

    issue.labels.append(new_label)
    issue.save()

    return f"A tarefa foi designada para: {new_label}."