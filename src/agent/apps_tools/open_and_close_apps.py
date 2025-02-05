import subprocess
import random
import webbrowser
from src.audio.elevenlabs_utils import ElevenLabsUtils

elevenlabs_utils = ElevenLabsUtils(dotenv_path="../../../.env")

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

        elevenlabs_utils.play_message("Todos os aplicativos do seu setup de desenvolvimento foram iniciados com sucesso! Posso ajudar em mais alguma coisa?")

        return "Todos os aplicativos foram abertos com sucesso."
    except Exception as e:
        print(f"Erro ao abrir os aplicativos: {e}")

def abrir_playlist_favorita() -> str:
    """
    Abre uma playlist de trabalho favorita escolhida aleatoriamente.
    Args:
        None
    """

    # Lista de links para playlists
    playlists = {
        "https://www.youtube.com/watch?v=GlmwkPdkaN4": "Creativity Playlist",
        "https://www.youtube.com/watch?v=jfKfPfyJRdk": "Lofi Hip Hop Playlist",
        "https://www.youtube.com/watch?v=DFuFDdL9sl4&t=58s": "Quiet 4:00 AM Playlist"
    }

    # Escolher aleatoriamente uma playlist
    playlist_escolhida = random.choice(list(playlists.keys()))

    # Abrir a playlist no navegador padrão
    webbrowser.open(playlist_escolhida)

    msg = f"Abri {playlists[playlist_escolhida]} para você!"

    elevenlabs_utils.play_message(msg)

    return f"Playlist aberta: {playlists[playlist_escolhida]}"

def abrir_links(links: list) -> str:
    """
    Abre links no navegador padrão.
    Args:
        None
    """
    for link in links:
        webbrowser.open(link)

    elevenlabs_utils.play_message("Pronto, abri o link como pedido.")
    return f"Link aberto com sucesso!"

def abrir_google_calendar() -> str:
    """
    Abre o Google Calendar no navegador padrão.
    Args:
        None
    """
    webbrowser.open("https://calendar.google.com/")

    elevenlabs_utils.play_message("Aqui está! Deseja fazer algo nesse google calendário?")
    return "Aqui está! Deseja fazer algo nesse google calendário?"

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

        elevenlabs_utils.play_message("Pronto, fechei seu ambiente de desenvolvimento! Seu dia de trabalho foi cansativo?")
        return "Todos os aplicativos foram fechados com sucesso."
    except Exception as e:
        print(f"Erro ao fechar os aplicativos: {e}")

if __name__ == "__main__":
    print(abrir_playlist_favorita())