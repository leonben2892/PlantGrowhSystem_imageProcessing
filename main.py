from PlantData import *
import requests

def https_post(plant_volume, plant_height):
    r = requests.post("https://plantgrowthsystembackend.azurewebsites.net/Plant/UpdateSize", data = {'id': '5c9123439ec5fc4398bfef5b', 'Volume': plant_volume, 'Height': plant_height})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')


def main():
    plant = PlantData()
    plant.calculate_plant_data("Bamboo")
    print("Bamboo Plant information:\n{}".format(plant))
    cv2.imshow("Plant Front", plant.front_image)
    cv2.imshow("Plant Side", plant.side_image)
    cv2.imshow("Plant Front Area", plant.plant_area_image)
    
    #https_post(plant.volume, plant.height)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()