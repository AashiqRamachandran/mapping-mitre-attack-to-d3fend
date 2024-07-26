# External Imports
import requests

# MITRE's API Base URL
BASE_URL = "https://d3fend.mitre.org"




def fetch_offensive_technique(technique_id):
   url = f"{BASE_URL}/api/offensive-technique/attack/{technique_id}.json"
   response = requests.get(url)
   if response.status_code == 200:
       return response.json()
   else:
       raise Exception(f"Failed to retrieve data: {response.status_code}")




def map_technique_to_defenses(technique_id):
   data = fetch_offensive_technique(technique_id)
   defenses = []
   for binding in data["off_to_def"]["results"]["bindings"]:
       defense = {
           "offensive_technique": binding['off_tech_label']['value'],
           "defensive_technique": binding.get('def_tech_label', {}).get('value', None),
           "defensive_tactic": binding.get('def_tactic_label', {}).get('value', None)
       }
       defenses.append(defense)
   return defenses




def main(technique_id):
   response_dictionary = {} # This is a dictionary where we will store the attacks and their relevant defences to return to the user
   try:
       defenses = map_technique_to_defenses(technique_id)
       for defense in defenses:
           if defense['offensive_technique'] not in response_dictionary:
               response_dictionary[defense['offensive_technique']] = []


           print(f"Offensive Technique: {defense['offensive_technique']}")


           if defense['defensive_technique']:
               print(f"  Defensive Technique: {defense['defensive_technique']}")
               response_dictionary[defense['offensive_technique']].append(f"Technique: {defense['defensive_technique']}")


           if defense['defensive_tactic']:
               print(f"  Defensive Tactic: {defense['defensive_tactic']}")
               response_dictionary[defense['offensive_technique']].append(f"Tactic: {defense['defensive_tactic']}")
           print()
   except Exception as e:
       print(e)
   return response_dictionary




if __name__ == "__main__":
   TECHNIQUE_ID = "T1204"
   json_response = main(TECHNIQUE_ID)
   print(json_response)
