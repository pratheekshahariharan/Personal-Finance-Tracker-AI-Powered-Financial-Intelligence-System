# openapi_client.BudgetApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**budget_status_budget_status_get**](BudgetApi.md#budget_status_budget_status_get) | **GET** /budget/status | Budget Status
[**set_budget_budget_post**](BudgetApi.md#set_budget_budget_post) | **POST** /budget/ | Set Budget


# **budget_status_budget_status_get**
> List[BudgetStatus] budget_status_budget_status_get(month=month, year=year)

Budget Status

Return spending vs budget for each configured category.

### Example


```python
import openapi_client
from openapi_client.models.budget_status import BudgetStatus
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BudgetApi(api_client)
    month = 56 # int |  (optional)
    year = 56 # int |  (optional)

    try:
        # Budget Status
        api_response = api_instance.budget_status_budget_status_get(month=month, year=year)
        print("The response of BudgetApi->budget_status_budget_status_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BudgetApi->budget_status_budget_status_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **month** | **int**|  | [optional] 
 **year** | **int**|  | [optional] 

### Return type

[**List[BudgetStatus]**](BudgetStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_budget_budget_post**
> BudgetOut set_budget_budget_post(budget_create)

Set Budget

Create or update a monthly budget for a category.

### Example


```python
import openapi_client
from openapi_client.models.budget_create import BudgetCreate
from openapi_client.models.budget_out import BudgetOut
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BudgetApi(api_client)
    budget_create = openapi_client.BudgetCreate() # BudgetCreate | 

    try:
        # Set Budget
        api_response = api_instance.set_budget_budget_post(budget_create)
        print("The response of BudgetApi->set_budget_budget_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BudgetApi->set_budget_budget_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_create** | [**BudgetCreate**](BudgetCreate.md)|  | 

### Return type

[**BudgetOut**](BudgetOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

