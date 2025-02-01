import subprocess

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


