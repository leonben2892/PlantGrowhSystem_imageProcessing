from PlantData import *
from Cameras import *
import requests
import time

# Https post
def send_data_to_server(plant_id, plant_volume, plant_height):
    r = requests.post("https://plantgrowthsystembackend.azurewebsites.net/Plant/UpdateSize", data = {'id': plant_id, 'Volume': plant_volume, 'Height': plant_height})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')

# Https get
def get_plant_id():
    request_ip = '1.1.1.1'
    r = requests.get("https://plantgrowthsystembackend.azurewebsites.net/Research/GetNewResearchByGrowthControlUnitIP?ip="+request_ip)
    return r.content


def main():
    plant_id = get_plant_id()
    while not plant_id:
        plant_id = get_plant_id()
        time.sleep(10)

    # Add api to check if an experiment  has stopped or not
    capture_and_set_images()
    plant = PlantData()
    plant.calculate_plant_data()
    print(plant)
    send_data_to_server(plant_id, plant.plant_volume, plant.plant_height)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()