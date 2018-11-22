from util import scrape
import csv

def getNumbersFromPair(nutri):
    num = nutri[0]
    percent = nutri[1]
    if 'mg' in num:
        try:
            num =  float(num.replace('mg', ''))
        except:
            print(num)
            num = -1
    else:
        try:
            num = float(num.replace('g', ''))
        except:
            print(num)
            num = -1
    try:
        percent = float(percent.replace('%', ''))
    except:
        print(percent)
        percent = -1
    return num, percent

def getNumberFromPercent(nutri):
    try:
        num = float(nutri.replace('%', ''))
    except:
        print(nutri)
        num = -1
    return num

def get_items(date):
    menu = scrape.scraper_for_day_overview(date)
    overviewMenu = menu['overviewMenu']
    items = []

    for period in list(overviewMenu):
        pmenu = overviewMenu[period]
        
        for hall in list(pmenu):
            hall_menu = pmenu[hall]
            
            for location in list(hall_menu):
                loc_menu = hall_menu[location]
                
                for item in loc_menu:
                    item_dict = {}
                    item_dict['name'] = item['name']
                    item_dict['recipe_link'] = item['recipe_link']
                    item_dict['itemcodes'] = "/".join(list(item['itemcodes']))#.encode('UTF-8')
                    item_dict['location'] = location
                    item_dict['dining_hall'] = hall
                    item_dict['dining_period'] = period
                    nutrition = item['nutrition']
                    for nutri_fact in list(nutrition):
                        if(type(nutrition[nutri_fact]) == str):
                            if(nutri_fact in ['serving_size']):
                                theString = nutrition[nutri_fact].replace('Serving Size ', '').replace('\xa0', ' ')
                                item_dict[nutri_fact] = theString
                            
                            elif(nutri_fact not in ['ingredients', 'allergens']):
                                item_dict[nutri_fact] = getNumberFromPercent(nutrition[nutri_fact])
                            else:
                                item_dict[nutri_fact] = nutrition[nutri_fact]
                        elif(type(nutrition[nutri_fact]) == list):
                            #item_dict['nf_'+nutri_fact] = '_'.join(nutrition[nutri_fact])#.encode('UTF-8')
                            num, percent = getNumbersFromPair(nutrition[nutri_fact])
                            item_dict[nutri_fact] = num
                            item_dict[nutri_fact+'_percent'] = percent
                        else:
                            print("Weird data type for nutri fact")
                    items.append(item_dict)
    return items

items = get_items('2018-11-15')
field_names = list(items[0])
file_name = "Items.csv"
try:
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = field_names)
        writer.writeheader()
        for item in items:
            writer.writerow(item)
except IOError:
    print("I/O Error")
