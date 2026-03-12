from api_client import *

class Item:
    def __init__(self, name, weight=0, price=0):
        self.name = name
        self.weight = weight
        self.price = price

class Weapon(Item):
    def __init__(self, api_data):
        if not api_data:
            raise ValueError("No se recibieron datos de la API")

        name = api_data.get('name')
        weight = api_data.get('weight', 0)
        price = api_data.get('cost', 0)
        super().__init__(name, weight, price)

        self.damage_dice = api_data.get('damage_dice', '1d4')

        d_type = api_data.get('damage_type')
        if isinstance(d_type, dict):
            self.damage_type = d_type.get('name', 'bludgeoning')
        else:
            self.damage_type = d_type if d_type else 'bludgeoning'

        properties = api_data.get('properties', [])
        # Buscamos 'finesse' en la lista (asegurándonos de que sean strings)
        if any('finesse' in str(p).lower() for p in properties):
            self.scaling = 'dex'
        else:
            self.scaling = 'str'

class Armor(Item):
    def __init__(self, api_data):
        name = api_data.get('name')
        weight = api_data.get('weight', 0)
        price = api_data.get('cost', 0)
        super().__init__(name, weight, price)
        self.base_ac = api_data.get('base_ac', 0)
        self.plus_cap = api_data.get('plus_max', 0)

        self.stat_dependencies = {
            'dex': api_data.get('plus_dex_mod', False),
            'con': api_data.get('plus_con_mod', False),
            'wis': api_data.get('plus_wis_mod', False)
        }

    def get_ac_bonus(self, entity):
        ac_bonus = self.base_ac
        for stat, active in self.stat_dependencies.items():
            if active:
                mod_value = getattr(entity, f"{stat}_mod")
                if stat == 'dex' and self.plus_cap is not None:
                    mod_value = min(mod_value, self.plus_cap)
                
                ac_bonus += mod_value
                
        return ac_bonus