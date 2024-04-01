from typing import List
from core.handyman.domain import model as mdl

def map_subcategories(category: mdl.HandymanCategory, sub_cats: List[str]):
    if category == mdl.HandymanCategory.PLUMBER:
        return [mdl.PlumberCategory(str(sub_category)) for sub_category in sub_cats]
    elif category == mdl.HandymanCategory.ELECTRICIAN:
        return [mdl.ElectricianCategory(str(sub_category)) for sub_category in sub_cats]
    elif category == mdl.HandymanCategory.CARPENTER:
        return [mdl.CarpenterCategory(str(sub_category)) for sub_category in sub_cats]
    elif category == mdl.HandymanCategory.PAINTER:
        return [mdl.PainterCategory(str(sub_category)) for sub_category in sub_cats]
    else:
        return []
    
def map_subcategories_from_string(category: mdl.HandymanCategory, sub_cats: List[str]):
    if category == mdl.HandymanCategory.PLUMBER:
        return [mdl.PlumberCategory[sub_category] for sub_category in sub_cats]
    elif category == mdl.HandymanCategory.ELECTRICIAN:
        return [mdl.ElectricianCategory[sub_category] for sub_category in sub_cats]
    elif category == mdl.HandymanCategory.CARPENTER:
        return [mdl.CarpenterCategory[sub_category] for sub_category in sub_cats]
    elif category == mdl.HandymanCategory.PAINTER:
        return [mdl.PainterCategory[sub_category] for sub_category in sub_cats]
    else:
        return []
