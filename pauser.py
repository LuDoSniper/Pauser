import os
import json
import subprocess
import threading



def compute_conf_path(name):
    pwd = __file__.split('/')
    path = "/"
    for dir in pwd[1:-1]:
        path += f"{dir}/"
    path += name

    return path

CONF_FILE_PATH = compute_conf_path("conf.json")



def save(data):
    with open(CONF_FILE_PATH, "w") as file:
        file.write(json.dumps(data))

def load():
    if os.path.exists(CONF_FILE_PATH):
        with open(CONF_FILE_PATH, "r") as file:
            data = json.load(file)
    else:
        data = {
            "time_gain": 0,
            "duration": 60
        }
    
    return data

def work():
    subprocess.run(['zenity', '--warning', '--title=Fin de la pause !', '--text=Il est l\'heure de retourner travailler !'])

    data = load()
    start_timer(int(data['duration']), pause)

def pause():
    subprocess.run(['zenity', '--warning', '--title=Fin du timer !', '--text=C\'est l\'heure de la pause !'])

    result = subprocess.run(['zenity', '--question', '--title=Prendre la pause ?', '--text=Si vous choisissez de ne pas prendre la pause, vous aurez une pause plus grande lors de la prochaine.', '--cancel-label=Prendre la pause', '--ok-label=Continuer de travailler'])
    response = result.returncode

    data = load()
    if response == 0:
        tmp = int(data['time_gain']) + 5
        data['time_gain'] = tmp
        save(data)

        duration = int(data['duration'])
        action = pause
    elif response == 1:
        duration = 10 + int(data['time_gain'])
        action = work

        data['time_gain'] = 0
        save(data)
    
    start_timer(duration, action)

def ask_time():
    result = subprocess.run(['zenity', '--entry', '--title=Lancement du timer', '--text=Entrer le temps en minutes :'], capture_output=True, text=True)
    response = result.returncode

    if response == 0:
        try:
            duration = int(result.stdout.strip())
            return duration
        except ValueError:
            subprocess.run(['zenity', '--warning', '--title=Erreur', '--text=L\'entrée n\'est pas valide ! Recommencez.'])
            return None
    elif response == 1:
        quit()

def start_timer(duration, action):
    timer = threading.Timer(duration * 60, action)
    timer.start()



# main

result = subprocess.run(['zenity', '--question', '--title=Lancement du programme', '--text=Commencer la journée ?', '--cancel-label=Quitter', '--ok-label=Choisir un temps'])
response = result.returncode

if response == 0:
    duration = None
    while duration == None:
        duration = ask_time()

        data = load()
        data['duration'] = duration
        save(data)

        start_timer(duration, pause)
elif response == 1:
    quit()