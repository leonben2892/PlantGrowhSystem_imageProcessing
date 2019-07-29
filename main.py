# import the necessary packages
from PlantData import *
from Cameras import *
import requests
import time

def send_data_to_server(plant_id, plant_volume, plant_height):
    """
    An http post method to send the plant data to the server.
    
    Parameters
    ----------
    plant_id: string
        The ID of the plant
    
    plant_volume: double
        The estimation the the plant volume
        
    plant_height: double
        The measured height of the plant
        
    Returns
    ----------
    Nothing
    """
    r = requests.post("https://plantgrowthsystembackend.azurewebsites.net/Plant/UpdateSize", data = {'id': plant_id, 'Volume': plant_volume, 'Height': plant_height})
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')

def get_request(request_url):
    """
    An http get method to request a plant ID from the server.
    
    Parameters
    ----------
    request_url: string
        The URL for requesting a plant ID 
        
    Returns
    ----------
    string: The plant ID
    """
    r = requests.get("https://plantgrowthsystembackend.azurewebsites.net/" + request_url)
    return r.content.decode("utf-8") 


def main():
    new_research_url = "Research/GetNewResearchByGrowthControlUnitIP?ip=1.1.1.1"
    check_research_stopped_url = "Plant/GetIntervalsByDate?id="
    plant = PlantData()
    while True:
        plant_id = get_request(new_research_url)
        while not plant_id:
            plant_id = get_request(new_research_url)
            time.sleep(10)
                  
        while get_request(check_research_stopped_url + plant_id) != '"stop"':
            capture_and_set_images()
            plant.calculate_plant_volume()
            send_data_to_server(plant_id, plant.plant_volume, plant.plant_height)
            time.sleep(86400)
            
    cv2.waitKey(0)

if __name__ == "__main__":
    main()