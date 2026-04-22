# OptimizationRecommendation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** |  | 
**count** | **int** |  | 
**potential_monthly_savings** | **float** |  | 
**message** | **str** |  | 

## Example

```python
from openapi_client.models.optimization_recommendation import OptimizationRecommendation

# TODO update the JSON string below
json = "{}"
# create an instance of OptimizationRecommendation from a JSON string
optimization_recommendation_instance = OptimizationRecommendation.from_json(json)
# print the JSON string representation of the object
print(OptimizationRecommendation.to_json())

# convert the object into a dict
optimization_recommendation_dict = optimization_recommendation_instance.to_dict()
# create an instance of OptimizationRecommendation from a dict
optimization_recommendation_from_dict = OptimizationRecommendation.from_dict(optimization_recommendation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


