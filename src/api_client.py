from requests import *

BASE_URL = "https://api.open5e.com/"

def get_monsters_cr(cr):
    monster_ids = []
    url = f"{BASE_URL}monsters/?cr={cr}"
    while url:
        try:
            response = get(url)
            response.raise_for_status()
            data = response.json()
            
            for monster in data['results']:
                monster_ids.append(monster['slug'])

            url = data['next']
        except exceptions.RequestException as e:
            print(f"Error fetching monsters: {e}")
            break
    return monster_ids

def get_monster_details(monster_id):
    response = get(f"{BASE_URL}{monster_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching monster details: {response.status_code}")
        return None
    
def get_monster_image(monster_id):
    details = get_monster_details(monster_id)
    if details and 'image' in details:
        return details['image']
    return None
    
def get_weapons():
    weapon_ids = []
    url = f"{BASE_URL}/v1/weapons/"
    while url:
        try:
            response = get(url)
            response.raise_for_status()
            data = response.json()
            
            for weapon in data['results']:
                weapon_ids.append(weapon['slug'])

            url = data['next']
        except exceptions.RequestException as e:
            print(f"Error fetching weapons: {e}")
            break
    return weapon_ids

def get_weapon_details(weapon_id):
    response = get(f"{BASE_URL}/v1/weapons/{weapon_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weapon details: {response.status_code}")
        return None

def get_armors():
    armor_ids = []
    url = f"{BASE_URL}/v1/armor/"
    while url:
        try:
            response = get(url)
            response.raise_for_status()
            data = response.json()

            for armor in data['results']:
                armor_ids.append(armor['slug'])

            url = data['next']
        except exceptions.RequestException as e:
            print(f"Error fetching armors: {e}")
            break
    return armor_ids

def get_armor_details(armor_id):
    response = get(f"{BASE_URL}/v1/armor/{armor_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching armor details: {response.status_code}")
        return None
    
def get_shields():
    shield_ids = []
    url = f"{BASE_URL}/v1/armor/?category=Shield"
    while url:
        try:
            response = get(url)
            response.raise_for_status()
            data = response.json()

            for armor in data['results']:
                if armor.get('category') == 'Shield':
                    shield_ids.append(armor['slug'])

            url = data['next']
        except exceptions.RequestException as e:
            print(f"Error fetching shields: {e}")
            break
    return shield_ids

def get_shield_details(shield_id):
    details = get_armor_details(shield_id)
    if details and details.get('category') == 'Shield':
        return details
    return None

def get_spells(spell_level):
    spell_ids = []
    url = f"{BASE_URL}/v1/spells/?spell_level={spell_level}"
    while url:
        try:
            response = get(url)
            response.raise_for_status()
            data = response.json()

            for spell in data['results']:
                spell_ids.append(spell['slug'])

            url = data['next']
        except exceptions.RequestException as e:
            print(f"Error fetching spells: {e}")
            break
    return spell_ids

def get_spell_details(spell_id):
    response = get(f"{BASE_URL}/v1/spells/{spell_id}/")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching spell details: {response.status_code}")
        return None
    
def get_spell_image(spell_id):
    details = get_spell_details(spell_id)
    if details and 'image' in details:
        return details['image']
    return None