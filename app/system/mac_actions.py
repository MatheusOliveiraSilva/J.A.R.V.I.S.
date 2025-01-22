import subprocess

class MacActions:
    def minimize_window(self):
        """
        Minimiza a janela ativa usando AppleScript.
        """
        script = '''
        tell application "System Events"
            keystroke "m" using {command down}
        end tell
        '''
        subprocess.run(["osascript", "-e", script])

if __name__ == "__main__":
    actions = MacActions()
    actions.minimize_window()