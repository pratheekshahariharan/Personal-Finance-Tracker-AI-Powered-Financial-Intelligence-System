# GamificationStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**streak_days** | **int** |  | 
**badges** | [**List[Badge]**](Badge.md) |  | 
**savings_progress** | **float** |  | 

## Example

```python
from openapi_client.models.gamification_status import GamificationStatus

# TODO update the JSON string below
json = "{}"
# create an instance of GamificationStatus from a JSON string
gamification_status_instance = GamificationStatus.from_json(json)
# print the JSON string representation of the object
print(GamificationStatus.to_json())

# convert the object into a dict
gamification_status_dict = gamification_status_instance.to_dict()
# create an instance of GamificationStatus from a dict
gamification_status_from_dict = GamificationStatus.from_dict(gamification_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


