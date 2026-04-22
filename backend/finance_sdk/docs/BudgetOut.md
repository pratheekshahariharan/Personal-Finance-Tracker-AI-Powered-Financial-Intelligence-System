# BudgetOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**category** | **str** |  | 
**monthly_limit** | **float** |  | 

## Example

```python
from openapi_client.models.budget_out import BudgetOut

# TODO update the JSON string below
json = "{}"
# create an instance of BudgetOut from a JSON string
budget_out_instance = BudgetOut.from_json(json)
# print the JSON string representation of the object
print(BudgetOut.to_json())

# convert the object into a dict
budget_out_dict = budget_out_instance.to_dict()
# create an instance of BudgetOut from a dict
budget_out_from_dict = BudgetOut.from_dict(budget_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


