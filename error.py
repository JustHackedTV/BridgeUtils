def ready():
    print("[Erro Module] Ready.")

def reason(errorcode):
    if errorcode == "UserAlredyRegister":
        return "Você já está registrado."
    elif errorcode == "UserNotRegistered":
        return "Você não está registrado, utilize **b!register** para se registrar."
    elif errorcode == "CommandNotFound":
        return "Esse Commando não foi encontrado."
    elif errorcode == "InvitedThemselfs":
        return "Você não pode convidar você mesmo."
    elif errorcode == "MissingPermissions":
        return "Você não tem permissões para utilizar esse comando."
    elif errorcode == "GameNotFound":
        return "Esse jogo não existe."
    elif errorcode == 'UnknownError':
        return 'ERROR'