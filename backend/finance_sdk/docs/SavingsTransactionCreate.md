# SavingsTransactionCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **float** |  | 
**reason** | **str** |  | [optional] 
**goal_id** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.savings_transaction_create import SavingsTransactionCreate

# TODO update the JSON string below
json = "{}"
# create an instance of SavingsTransactionCreate from a JSON string
savings_transaction_create_instance = SavingsTransactionCreate.from_json(json)
# print the JSON string representation of the object
print(SavingsTransactionCreate.to_json())

# convert the object into a dict
savings_transaction_create_dict = savings_transaction_create_instance.to_dict()
# create an instance of SavingsTransactionCreate from a dict
savings_transaction_create_from_dict = SavingsTransactionCreate.from_dict(savings_transaction_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


