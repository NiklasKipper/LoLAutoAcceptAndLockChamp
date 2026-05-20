import os
import time
import base64
import requests
import urllib3

urllib3.disable_warnings()

# =========================================
# CONFIG
# =========================================

# =========================================
# CHAMPION IDS
# =========================================

# Aatrox = 266
# Ahri = 103
# Akali = 84
# Akshan = 166
# Alistar = 12
# Amumu = 32
# Anivia = 34
# Annie = 1
# Aphelios = 523
# Ashe = 22
# Aurelion Sol = 136
# Aurora = 893
# Azir = 268

# Bard = 432
# Bel'Veth = 200
# Blitzcrank = 53
# Brand = 63
# Braum = 201
# Briar = 233

# Caitlyn = 51
# Camille = 164
# Cassiopeia = 69
# Cho'Gath = 31
# Corki = 42

# Darius = 122
# Diana = 131
# Dr. Mundo = 36
# Draven = 119

# Ekko = 245
# Elise = 60
# Evelynn = 28
# Ezreal = 81

# Fiddlesticks = 9
# Fiora = 114
# Fizz = 105

# Galio = 3
# Gangplank = 41
# Garen = 86
# Gnar = 150
# Gragas = 79
# Graves = 104
# Gwen = 887

# Hecarim = 120
# Heimerdinger = 74
# Hwei = 910

# Illaoi = 420
# Irelia = 39
# Ivern = 427

# Janna = 40
# Jarvan IV = 59
# Jax = 24
# Jayce = 126
# Jhin = 202
# Jinx = 222

# Kai'Sa = 145
# Kalista = 429
# Karma = 43
# Karthus = 30
# Kassadin = 38
# Katarina = 55
# Kayle = 10
# Kayn = 141
# Kennen = 85
# Kha'Zix = 121
# Kindred = 203
# Kled = 240
# Kog'Maw = 96

# LeBlanc = 7
# Lee Sin = 64
# Leona = 89
# Lillia = 876
# Lissandra = 127
# Lucian = 236
# Lulu = 117
# Lux = 99

# Malphite = 54
# Malzahar = 90
# Maokai = 57
# Master Yi = 11
# Milio = 902
# Miss Fortune = 21
# Mordekaiser = 82
# Morgana = 25

# Naafiri = 950
# Nami = 267
# Nasus = 75
# Nautilus = 111
# Neeko = 518
# Nidalee = 76
# Nilah = 895
# Nocturne = 56
# Nunu = 20

# Olaf = 2
# Orianna = 61
# Ornn = 516

# Pantheon = 80
# Poppy = 78
# Pyke = 555

# Qiyana = 246
# Quinn = 133

# Rakan = 497
# Rammus = 33
# Rek'Sai = 421
# Rell = 526
# Renata Glasc = 888
# Renekton = 58
# Rengar = 107
# Riven = 92
# Rumble = 68
# Ryze = 13

# Samira = 360
# Sejuani = 113
# Senna = 235
# Seraphine = 147
# Sett = 875
# Shaco = 35
# Shen = 98
# Shyvana = 102
# Singed = 27
# Sion = 14
# Sivir = 15
# Skarner = 72
# Smolder = 901
# Sona = 37
# Soraka = 16
# Swain = 50
# Sylas = 517
# Syndra = 134

# Tahm Kench = 223
# Taliyah = 163
# Talon = 91
# Taric = 44
# Teemo = 17
# Thresh = 412
# Tristana = 18
# Trundle = 48
# Tryndamere = 23
# Twisted Fate = 4
# Twitch = 29

# Udyr = 77
# Urgot = 6

# Varus = 110
# Vayne = 67
# Veigar = 45
# Vel'Koz = 161
# Vex = 711
# Vi = 254
# Viego = 234
# Viktor = 112
# Vladimir = 8
# Volibear = 106

# Warwick = 19
# Wukong = 62

# Xayah = 498
# Xerath = 101
# Xin Zhao = 5

# Yasuo = 157
# Yone = 777
# Yorick = 83
# Yuumi = 350

# Zac = 154
# Zed = 238
# Zeri = 221
# Ziggs = 115
# Zilean = 26
# Zoe = 142
# Zyra = 143

PICK_CHAMPION_ID = 157
BAN_CHAMPION_ID = 84

# =========================================
# LOCKFILE FINDER
# =========================================

def find_lockfile():

    possible_roots = [
        r"C:\Riot Games",
        r"D:\Riot Games",
        r"E:\Riot Games",
    ]

    for root in possible_roots:

        if not os.path.exists(root):
            continue

        for current_root, dirs, files in os.walk(root):

            if "League of Legends" in current_root:

                if "lockfile" in files:
                    return os.path.join(current_root, "lockfile")

    return None


# =========================================
# AUTH
# =========================================

def get_credentials(lockfile_path):

    with open(lockfile_path, "r") as f:
        data = f.read().split(":")

    return {
        "port": data[2],
        "password": data[3]
    }


def build_headers(password):

    auth = base64.b64encode(
        f"riot:{password}".encode()
    ).decode()

    return {
        "Authorization": f"Basic {auth}"
    }


# =========================================
# AUTO ACCEPT API
# =========================================

def get_ready_check(port, headers):

    url = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check"

    try:

        response = requests.get(
            url,
            headers=headers,
            verify=False,
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

    except:
        pass

    return None


def accept_queue(port, headers):

    url = f"https://127.0.0.1:{port}/lol-matchmaking/v1/ready-check/accept"

    for attempt in range(5):

        try:

            response = requests.post(
                url,
                headers=headers,
                verify=False,
                timeout=5
            )

            print(f"Accept Versuch {attempt + 1}: {response.status_code}")

            if response.status_code == 200:
                return True

        except Exception as e:
            print("Accept Fehler:", e)

        time.sleep(0.5)

    return False


# =========================================
# CHAMP SELECT API
# =========================================

def get_session(port, headers):

    url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"

    try:

        response = requests.get(
            url,
            headers=headers,
            verify=False,
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

    except:
        pass

    return None


def perform_action(port, headers, action_id, champion_id):

    url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session/actions/{action_id}"

    data = {
        "championId": champion_id,
        "completed": True
    }

    try:

        response = requests.patch(
            url,
            json=data,
            headers=headers,
            verify=False,
            timeout=5
        )

        return response.status_code in [200, 204]

    except Exception as e:
        print("Action Fehler:", e)

    return False


# =========================================
# MAIN
# =========================================

print("Warte auf League...")

lockfile = None
accepted = False

while True:

    # =========================================
    # WARTEN AUF LEAGUE
    # =========================================

    while not lockfile:

        lockfile = find_lockfile()

        if not lockfile:
            print("League nicht gefunden...")
            time.sleep(5)

    try:

        creds = get_credentials(lockfile)

        port = creds["port"]
        password = creds["password"]

        headers = build_headers(password)

        # =========================================
        # AUTO ACCEPT
        # =========================================

        ready_check = get_ready_check(port, headers)

        if ready_check:

            state = ready_check.get("state")
            player_response = ready_check.get("playerResponse")

            if (
                state == "InProgress"
                and player_response == "None"
                and not accepted
            ):

                print("QUEUE POP!")

                success = accept_queue(port, headers)

                if success:
                    accepted = True
                    print("Match angenommen!")

            if state != "InProgress":
                accepted = False

        # =========================================
        # CHAMP SELECT
        # =========================================

        session = get_session(port, headers)

        if session:

            local_player_id = session.get("localPlayerCellId")

            actions = session.get("actions", [])

            for action_group in actions:

                for action in action_group:

                    actor = action.get("actorCellId")

                    if actor != local_player_id:
                        continue

                    if action.get("completed"):
                        continue

                    action_id = action.get("id")
                    action_type = action.get("type")

                    # =========================================
                    # AUTO BAN
                    # =========================================

                    if action_type == "ban":

                        print("Ban Phase erkannt!")

                        success = perform_action(
                            port,
                            headers,
                            action_id,
                            BAN_CHAMPION_ID
                        )

                        if success:
                            print("Akali gebannt!")

                    # =========================================
                    # AUTO PICK
                    # =========================================

                    if action_type == "pick":

                        print("Pick Phase erkannt!")

                        success = perform_action(
                            port,
                            headers,
                            action_id,
                            PICK_CHAMPION_ID
                        )

                        if success:
                            print("Yasuo gepickt und gelockt!")

        time.sleep(1)

    except Exception as e:

        print("Fehler:", e)

        lockfile = None
        accepted = False

        time.sleep(5)