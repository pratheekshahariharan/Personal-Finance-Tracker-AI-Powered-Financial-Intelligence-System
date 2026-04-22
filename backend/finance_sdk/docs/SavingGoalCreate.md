# SavingGoalCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**target_amount** | **float** |  | 

## Example

```python
from openapi_client.models.saving_goal_create import SavingGoalCreate

# TODO update the JSON string below
json = "{}"
# create an instance of SavingGoalCreate from a JSON string
saving_goal_create_instance = SavingGoalCreate.from_json(json)
# print the JSON string representation of the object
print(SavingGoalCreate.to_json())

# convert the object into a dict
saving_goal_create_dict = saving_goal_create_instance.to_dict()
# create an instance of SavingGoalCreate from a dict
saving_goal_create_from_dict = SavingGoalCreate.from_dict(saving_goal_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


