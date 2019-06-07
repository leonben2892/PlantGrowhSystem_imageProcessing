from PlantData import *
from Cameras import *
import requests

# Https post
def send_data_to_server(plant_id, plant_volume, plant_height):
    r = requests.post("https://plantgrowthsystembackend.azurewebsites.net/Plant/UpdateSize", data = {'id': plant_id, 'Volume': plant_volume, 'Height': plant_height})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')

# Https get
def get_plant_id():
    request_ip = '10.12.61.80'
    r = requests.get("https://plantgrowthsystembackend.azurewebsites.net/Research/GetNewResearchByGrowthControlUnitIP?ip="+request_ip)
    return r.content


def main():
    plant = PlantData()
    plant.calculate_plant_data("Sherry")
    print("{} Plant information:\n{}".format(plant.plant_type, plant))
    cv2.imshow("{} Front".format(plant.plant_type), plant.front_image)
    cv2.imshow("{} Side".format(plant.plant_type), plant.side_image)
    cv2.imshow("{} Surface Area".format(plant.plant_type), plant.plant_area_image)
    
    # plant_id = get_plant_id()
    # send_data_to_server(plant_id, plant.volume, plant.height)
    # crop_image(200,0,900,800)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()