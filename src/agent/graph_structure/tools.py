import src.agent.gitlab_tools.gitlab_tools as gl_tools
import src.agent.apps_tools.open_and_close_apps as open_and_close_tools
import src.agent.search_tools.web_search as web_search_tools

# List of tools that can be used in multiple files, so they can be imported like this.
TOOLS = [
    gl_tools.get_opened_issues,
    gl_tools.issue_spent_time,
    gl_tools.change_assignee,
    gl_tools.change_labels,

    # new feature
    open_and_close_tools.abrir_ambiente_desenvolvimento,
    open_and_close_tools.abrir_playlist_favorita,
    open_and_close_tools.abrir_links,
    open_and_close_tools.abrir_google_calendar,
    open_and_close_tools.fechar_ambiente_desenvolvimento,
    web_search_tools.web_search,

    # Add more tools here
]