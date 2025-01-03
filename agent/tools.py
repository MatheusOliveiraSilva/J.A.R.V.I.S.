import gitlab_tools.tools as gl_tools

# List of tools that can be used in multiple files, so they can be imported like this.
TOOLS = [
    gl_tools.get_opened_issues,
    gl_tools.issue_spent_time,
    gl_tools.change_assignee,
    gl_tools.change_labels,
    # Add more tools here
    # gmail.check_mailbox,
    # gmail.send_email
]
