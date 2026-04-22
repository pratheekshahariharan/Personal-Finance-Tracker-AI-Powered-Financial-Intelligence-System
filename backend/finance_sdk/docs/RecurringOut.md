# RecurringOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**description** | **str** |  | 
**amount** | **float** |  | 
**transaction_type** | **str** |  | 
**category** | **str** |  | 
**frequency** | **str** |  | 
**next_due_date** | **date** |  | [optional] 

## Example

```python
from openapi_client.models.recurring_out import RecurringOut

# TODO update the JSON string below
json = "{}"
# create an instance of RecurringOut from a JSON string
recurring_out_instance = RecurringOut.from_json(json)
# print the JSON string representation of the object
print(RecurringOut.to_json())

# convert the object into a dict
recurring_out_dict = recurring_out_instance.to_dict()
# create an instance of RecurringOut from a dict
recurring_out_from_dict = RecurringOut.from_dict(recurring_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


