class Item:
    def __init__(self, name, weight=0, price=0):
        self.name = name
        self.weight = weight
        self.price = price

class Weapon(Item):
    def __init__(self, name, damage_dice, scaling_stat, weight=0, price=0):
        """
        :param damage_dice: Ejemplo "1d6", "2d4" o un número entero.
        :param scaling_stat: 'str', 'dex' o 'int'.
        """
        super().__init__(name, weight, price)
        self.damage_dice = damage_dice
        self.scaling_stat = scaling_stat

class Armor(Item):
    def __init__(self, name, ac_bonus, armor_type, weight=0, price=0):
        """
        :param ac_bonus: El valor de protección (ej: 15 para una coraza).
        :param armor_type: 'light', 'medium', 'heavy'.
        """
        super().__init__(name, weight, price)
        self.ac_bonus = ac_bonus
        self.armor_type = armor_type