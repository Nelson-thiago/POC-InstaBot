
from botcity.web import WebBot, Browser, By
from datetime import datetime
import instaloader
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    try:
        instabot = instaloader.Instaloader()

        maestro = BotMaestroSDK.from_sys_args()
        execution = maestro.get_execution()

        bot = WebBot()

        # Configurando para rodar em modo headless
        bot.headless = False

        bot.browser = Browser.CHROME
        bot.driver_path = r"C:\Users\Nelson Thiago\Desktop\Botcity\BotCotacao2\resources\chromedriver.exe"
        
        maestro.alert(
            task_id=execution.task_id,
            title="BotInstagram - Inicio",
            message="Estamos iniciando o processo de coleta de dados do Instagram",
            alert_type=AlertType.INFO
        )

        # URL do perfil do Instagram
        perfil = execution.parameters.get("perfil", "marycagnin")
        bot.browse(f"https://www.instagram.com/{perfil}")
        bot.wait(5000)  # Aguardar o carregamento da página
        
        profile = instaloader.Profile.from_username(instabot.context, perfil)
        print(type(profile))

        # Identificador do Instagram e ID do perfil
        print(f"Nome de usuário:", profile.username)
        print(f"ID do usuário", profile.userid)
        # Número de seguidores e seguidos
        print(f"Numero de seguidores:", profile.followers)
        print(f"Numero de seguidos:", profile.followees)
        print(f"Numero de publicações:", profile.mediacount)

        # Coletar os dados de texto dos elementos
        id = profile.userid
        publicacoes = profile.mediacount
        seguidores = profile.followers
        seguindo = profile.followees

        # Salvando uma captura de tela
        bot.save_screenshot("captura_instagram.png")
        # Enviando para a plataforma com o nome "Captura Instagram..."
        maestro.post_artifact(
            task_id=execution.task_id,
            artifact_name=f"Captura Instagram {perfil}.png",
            filepath="captura_instagram.png"
        )

        status = AutomationTaskFinishStatus.SUCCESS
        message = "Tarefa BotInstagram finalizada com sucesso"

    except Exception as ex:
        # Salvando captura de tela do erro
        bot.save_screenshot("erro_instagram.png")

        # Dicionario de tags adicionais
        tags = {"perfil": perfil}

        # Registrando o erro
        maestro.error(
            task_id=execution.task_id,
            exception=ex,
            screenshot="erro_instagram.png",
            tags=tags
        )

        status = AutomationTaskFinishStatus.FAILED
        message = "Tarefa BotInstagram finalizada com falha"

    finally:
        maestro.new_log_entry(
            activity_label="EstatisticasInstagram",
            values = {
                "data_hora": datetime.now().strftime("%Y-%m-%d_%H-%M"),
                "id": id,
                "perfil": perfil,
                "publicacoes": publicacoes,
                "seguidores": seguidores,
                "seguindo": seguindo
            }
        )

        bot.wait(2000)
        bot.stop_browser()

        # Finalizando a tarefa
        maestro.finish_task(
            task_id=execution.task_id,
            status=status,
            message=message
        )

def not_found(label):
    print(f"Element not found: {label}")

if __name__ == '__main__':
    main()
