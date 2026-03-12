# Entity interface for most entities in the game, such as players, NPCs, enemies

class Entity:
    def __init__(self, name, hp, stats):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_ac = 10
        self.equipment = {"weapon": None, "armor": None, "shield": None}

        self.str_mod = self._calculate_stat_mod(stats.get('str', 10))
        self.dex_mod = self._calculate_stat_mod(stats.get('dex', 10))
        self.con_mod = self._calculate_stat_mod(stats.get('con', 10))
        self.int_mod = self._calculate_stat_mod(stats.get('int', 10))
        self.wis_mod = self._calculate_stat_mod(stats.get('wis', 10))
        self.cha_mod = self._calculate_stat_mod(stats.get('cha', 10))

    @property
    def ac(self):
        if self.equipment["armor"]:
            return self.base_ac + self.equipment["armor"].ac_bonus
        return self.base_ac + self.dex_mod

    def _calculate_stat_mod(self, stat):
        return (stat - 10) // 2
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def is_alive(self):
        return self.hp > 0
    
    def get_attacked(self, attack_roll, damage):
        weapon = self.equipment["weapon"]
        if weapon:
            return self.dex_mod if weapon.scaling == 'dex' else self.str_mod
        return self.str_mod

class Enemy(Entity):
    def __init__(self, api_data):
        stats = {
            'str': api_data.get('strength', 10),
            'dex': api_data.get('dexterity', 10),
            'con': api_data.get('constitution', 10),
            'int': api_data.get('intelligence', 10),
            'wis': api_data.get('wisdom', 10),
            'cha': api_data.get('charisma', 10)
        }
        name = api_data.get('name')
        hp = api_data.get('hp', 10)
        cr = api_data.get('challenge_rating', 0)
        super().__init__(name, hp, stats)
        self.cr = cr
        self.base_ac = api_data.get('armor_class', 10)