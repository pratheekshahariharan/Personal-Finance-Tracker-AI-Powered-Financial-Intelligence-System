# DashboardOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_income** | **float** |  | 
**total_expenses** | **float** |  | 
**balance** | **float** |  | 
**total_savings** | **float** |  | 
**monthly_income** | **float** |  | 
**monthly_expenses** | **float** |  | 
**carried_savings** | **float** |  | 
**total_transactions** | **int** |  | 
**top_spending_category** | **str** |  | 
**recent_activity** | [**List[TransactionOut]**](TransactionOut.md) |  | 

## Example

```python
from openapi_client.models.dashboard_out import DashboardOut

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardOut from a JSON string
dashboard_out_instance = DashboardOut.from_json(json)
# print the JSON string representation of the object
print(DashboardOut.to_json())

# convert the object into a dict
dashboard_out_dict = dashboard_out_instance.to_dict()
# create an instance of DashboardOut from a dict
dashboard_out_from_dict = DashboardOut.from_dict(dashboard_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


