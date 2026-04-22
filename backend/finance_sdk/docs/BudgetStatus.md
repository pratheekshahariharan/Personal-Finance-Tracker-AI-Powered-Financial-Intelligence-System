# BudgetStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** |  | 
**monthly_limit** | **float** |  | 
**current_spending** | **float** |  | 
**projected_spending** | **float** |  | 
**days_left** | **int** |  | 
**exceeded** | **bool** |  | 

## Example

```python
from openapi_client.models.budget_status import BudgetStatus

# TODO update the JSON string below
json = "{}"
# create an instance of BudgetStatus from a JSON string
budget_status_instance = BudgetStatus.from_json(json)
# print the JSON string representation of the object
print(BudgetStatus.to_json())

# convert the object into a dict
budget_status_dict = budget_status_instance.to_dict()
# create an instance of BudgetStatus from a dict
budget_status_from_dict = BudgetStatus.from_dict(budget_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


