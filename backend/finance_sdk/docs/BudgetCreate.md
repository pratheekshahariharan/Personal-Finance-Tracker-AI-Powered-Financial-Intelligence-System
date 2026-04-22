# BudgetCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** |  | 
**monthly_limit** | **float** |  | 

## Example

```python
from openapi_client.models.budget_create import BudgetCreate

# TODO update the JSON string below
json = "{}"
# create an instance of BudgetCreate from a JSON string
budget_create_instance = BudgetCreate.from_json(json)
# print the JSON string representation of the object
print(BudgetCreate.to_json())

# convert the object into a dict
budget_create_dict = budget_create_instance.to_dict()
# create an instance of BudgetCreate from a dict
budget_create_from_dict = BudgetCreate.from_dict(budget_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


