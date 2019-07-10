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
def get_request(request_url):
    r = requests.get("https://plantgrowthsystembackend.azurewebsites.net/" + request_url)
    return r.content.decode("utf-8") 


def main():
    new_research_url = "Research/GetNewResearchByGrowthControlUnitIP?ip=1.1.1.1"
    check_research_stopped_url = "Plant/GetIntervalsByDate?id="
    is_image_proccessing_happend = False
    plant = PlantData()
    while True:
        plant_id = get_request(new_research_url)
        while not plant_id:
            plant_id = get_request(new_research_url)
            time.sleep(10)
              
        while get_request(check_research_stopped_url + plant_id) != '"stop"':
            if is_image_proccessing_happend is False:
                # capture_and_set_images()
                plant.calculate_plant_data()
                print(plant)
                send_data_to_server(plant_id, plant.plant_volume, plant.plant_height)
                is_image_proccessing_happend = True
            time.sleep(20)
            send_data_to_server(plant_id, plant.plant_volume, plant.plant_height)
  
    # cv2.waitKey(0)

if __name__ == "__main__":
    main()