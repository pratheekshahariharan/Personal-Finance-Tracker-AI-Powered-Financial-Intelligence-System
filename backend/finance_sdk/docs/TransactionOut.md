# TransactionOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**amount** | **float** |  | 
**description** | **str** |  | 
**transaction_type** | **str** |  | 
**category** | **str** |  | 
**auto_tagged** | **bool** |  | 
**timestamp** | **datetime** |  | 
**note** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.transaction_out import TransactionOut

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionOut from a JSON string
transaction_out_instance = TransactionOut.from_json(json)
# print the JSON string representation of the object
print(TransactionOut.to_json())

# convert the object into a dict
transaction_out_dict = transaction_out_instance.to_dict()
# create an instance of TransactionOut from a dict
transaction_out_from_dict = TransactionOut.from_dict(transaction_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


