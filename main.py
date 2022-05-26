from Lieferando import Lieferando

if __name__ == "__main__":
    print("Script starting...")
    area = input('Search area: ')
    liefe = Lieferando(area)
    liefe.loadListRestaurantsURL()
    liefe.getRestaurantsData()
