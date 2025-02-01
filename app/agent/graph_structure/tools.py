import app.agent.gitlab_tools.tools as gl_tools
import app.agent.apps_tools.open_app_tools as open_tools
import app.agent.apps_tools.close_app_tools as close_tools
import app.agent.search_tools.web_search as web_search_tools

# List of tools that can be used in multiple files, so they can be imported like this.
TOOLS = [
    gl_tools.get_opened_issues,
    gl_tools.issue_spent_time,
    gl_tools.change_assignee,
    gl_tools.change_labels,

    # new feature
    open_tools.abrir_ambiente_desenvolvimento,
    open_tools.abrir_playlist_favorita,
    open_tools.abrir_links,
    open_tools.abrir_google_calendar,
    close_tools.fechar_ambiente_desenvolvimento,
    web_search_tools.web_search,

    # Add more tools here
]