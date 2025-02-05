import subprocess
import random
import webbrowser
from src.audio.elevenlabs_utils import speak

def abrir_ambiente_desenvolvimento() -> str:
    """
    Abre os aplicativos PyCharm, Slack, GitKraken e OpenVPN no macOS.

    Args:
        None
    """
    try:
        # Lista de aplicativos a serem abertos
        aplicativos = {
            "PyCharm": "/Applications/PyCharm.app",
            "Slack": "/Applications/Slack.app",
            "GitKraken": "/Applications/GitKraken.app",
            "OpenVPN": "/Applications/OpenVPN Connect.app"
        }

        # Abrir cada aplicativo
        for nome, caminho in aplicativos.items():
            subprocess.run(["open", caminho])
            print(f"{nome} foi iniciado com sucesso.")

        speak("Todos os aplicativos do seu setup de desenvolvimento foram iniciados com sucesso! Posso ajudar em mais alguma coisa?")

    except Exception as e:
        print(f"Erro ao abrir os aplicativos: {e}")

def abrir_playlist_favorita() -> str:
    """
    Abre uma playlist de trabalho favorita escolhida aleatoriamente.
    Args:
        None
    """

    # Lista de links para playlists
    playlists = [
        "https://www.youtube.com/watch?v=GlmwkPdkaN4",
        "https://www.youtube.com/watch?v=jfKfPfyJRdk",
        "https://www.youtube.com/watch?v=DFuFDdL9sl4&t=58s"
    ]

    # Escolher aleatoriamente uma playlist
    playlist_escolhida = random.choice(playlists)

    # Abrir a playlist no navegador padrão
    webbrowser.open(playlist_escolhida)

    return f"Abrindo a playlist: {playlist_escolhida}"

def abrir_links(links: list) -> str:
    """
    Abre links no navegador padrão.
    Args:
        None
    """
    for link in links:
        webbrowser.open(link)

    return f"Abrindo a playlist: {playlist_escolhida}"

def abrir_google_calendar() -> str:
    """
    Abre o Google Calendar no navegador padrão.
    Args:
        None
    """
    webbrowser.open("https://calendar.google.com/")

    return "Abrindo o Google Calendar..."

def fechar_ambiente_desenvolvimento() -> str:
    """
    Fecha os aplicativos PyCharm, Slack, GitKraken e OpenVPN no macOS.
    Args:
        None
    """
    try:
        # Lista de aplicativos a serem fechados
        aplicativos = ["Slack", "GitKraken", "OpenVPN Connect"]

        for app in aplicativos:
            # Usar AppleScript para enviar comando de encerramento
            subprocess.run(["osascript", "-e", f'tell application "{app}" to quit'])
            print(f"{app} foi encerrado com sucesso.")

        return "Todos os aplicativos foram fechados com sucesso."
    except Exception as e:
        print(f"Erro ao fechar os aplicativos: {e}")

