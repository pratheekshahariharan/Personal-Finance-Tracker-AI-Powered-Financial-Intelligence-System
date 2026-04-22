# SavingsTransactionOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**type** | **str** |  | 
**amount** | **float** |  | 
**reason** | **str** |  | 
**goal_id** | **int** |  | 
**timestamp** | **datetime** |  | 

## Example

```python
from openapi_client.models.savings_transaction_out import SavingsTransactionOut

# TODO update the JSON string below
json = "{}"
# create an instance of SavingsTransactionOut from a JSON string
savings_transaction_out_instance = SavingsTransactionOut.from_json(json)
# print the JSON string representation of the object
print(SavingsTransactionOut.to_json())

# convert the object into a dict
savings_transaction_out_dict = savings_transaction_out_instance.to_dict()
# create an instance of SavingsTransactionOut from a dict
savings_transaction_out_from_dict = SavingsTransactionOut.from_dict(savings_transaction_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


