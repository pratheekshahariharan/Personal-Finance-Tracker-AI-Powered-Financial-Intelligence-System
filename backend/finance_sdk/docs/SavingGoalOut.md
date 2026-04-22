# SavingGoalOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**target_amount** | **float** |  | 
**current_amount** | **float** |  | 

## Example

```python
from openapi_client.models.saving_goal_out import SavingGoalOut

# TODO update the JSON string below
json = "{}"
# create an instance of SavingGoalOut from a JSON string
saving_goal_out_instance = SavingGoalOut.from_json(json)
# print the JSON string representation of the object
print(SavingGoalOut.to_json())

# convert the object into a dict
saving_goal_out_dict = saving_goal_out_instance.to_dict()
# create an instance of SavingGoalOut from a dict
saving_goal_out_from_dict = SavingGoalOut.from_dict(saving_goal_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


