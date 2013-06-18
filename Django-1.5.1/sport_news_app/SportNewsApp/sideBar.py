from main.models import SportNewsMainCategory, SportNewsCategory

def getSideBar(category_id = -1):
    side_bar = []
    main_categories_list = SportNewsMainCategory.objects.all()
    side_bar.append(main_categories_list)
    categories_map = {}
    for main_category in main_categories_list:
        if category_id == main_category.id:
            categories_map[main_category.id] = SportNewsCategory.objects.filter(mainCategory__name=main_category.name)
    side_bar.append(categories_map)
    
    return side_bar