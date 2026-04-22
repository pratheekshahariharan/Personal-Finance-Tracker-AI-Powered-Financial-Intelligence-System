# RecurringCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | 
**amount** | **float** |  | 
**transaction_type** | **str** |  | 
**frequency** | **str** |  | 
**next_due_date** | **date** |  | [optional] 

## Example

```python
from openapi_client.models.recurring_create import RecurringCreate

# TODO update the JSON string below
json = "{}"
# create an instance of RecurringCreate from a JSON string
recurring_create_instance = RecurringCreate.from_json(json)
# print the JSON string representation of the object
print(RecurringCreate.to_json())

# convert the object into a dict
recurring_create_dict = recurring_create_instance.to_dict()
# create an instance of RecurringCreate from a dict
recurring_create_from_dict = RecurringCreate.from_dict(recurring_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


