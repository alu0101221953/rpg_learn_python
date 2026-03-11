# Entity interface for most entities in the game, such as players, NPCs, enemies

class Entity:
    def __init__(self, name, hp, stats):
        self.name = name
        self.max_hp = hp
        self.hp = hp

        self.str_mod = self._calculate_stat_mod(stats.get('str', 10))
        self.dex_mod = self._calculate_stat_mod(stats.get('dex', 10))
        self.con_mod = self._calculate_stat_mod(stats.get('con', 10))
        self.int_mod = self._calculate_stat_mod(stats.get('int', 10))
        self.wis_mod = self._calculate_stat_mod(stats.get('wis', 10))
        self.cha_mod = self._calculate_stat_mod(stats.get('cha', 10))

    def _calculate_stat_mod(self, stat):
        return (stat - 10) // 2
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

class Enemy(Entity):
    def __init__(self, name, hp, stats, cr):
        super().__init__(name, hp, stats)
        self.cr = cr