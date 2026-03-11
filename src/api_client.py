import requests

BASE_URL = "https://api.open5e.com/monsters/"

def get_monsters_cr(cr):
    monster_ids = []
    url = f"{BASE_URL}?cr={cr}"

    while url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for monster in data['results']:
                monster_ids.append(monster['slug'])

            url = data['next']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching monsters: {e}")
            break
    return monster_ids

def get_monster_details(monster_id):
    response = requests.get(f"{BASE_URL}{monster_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching monster details: {response.status_code}")
        return None