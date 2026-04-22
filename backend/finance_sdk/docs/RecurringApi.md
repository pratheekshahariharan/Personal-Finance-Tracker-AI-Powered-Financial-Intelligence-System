# openapi_client.RecurringApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_recurring_recurring_post**](RecurringApi.md#create_recurring_recurring_post) | **POST** /recurring/ | Create Recurring
[**delete_recurring_recurring_rec_id_delete**](RecurringApi.md#delete_recurring_recurring_rec_id_delete) | **DELETE** /recurring/{rec_id} | Delete Recurring
[**list_recurring_recurring_get**](RecurringApi.md#list_recurring_recurring_get) | **GET** /recurring/ | List Recurring


# **create_recurring_recurring_post**
> RecurringOut create_recurring_recurring_post(recurring_create)

Create Recurring

Create a recurring transaction template.

### Example


```python
import openapi_client
from openapi_client.models.recurring_create import RecurringCreate
from openapi_client.models.recurring_out import RecurringOut
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
    api_instance = openapi_client.RecurringApi(api_client)
    recurring_create = openapi_client.RecurringCreate() # RecurringCreate | 

    try:
        # Create Recurring
        api_response = api_instance.create_recurring_recurring_post(recurring_create)
        print("The response of RecurringApi->create_recurring_recurring_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RecurringApi->create_recurring_recurring_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **recurring_create** | [**RecurringCreate**](RecurringCreate.md)|  | 

### Return type

[**RecurringOut**](RecurringOut.md)

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

# **delete_recurring_recurring_rec_id_delete**
> delete_recurring_recurring_rec_id_delete(rec_id)

Delete Recurring

Cancel a recurring transaction template.

### Example


```python
import openapi_client
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
    api_instance = openapi_client.RecurringApi(api_client)
    rec_id = 56 # int | 

    try:
        # Delete Recurring
        api_instance.delete_recurring_recurring_rec_id_delete(rec_id)
    except Exception as e:
        print("Exception when calling RecurringApi->delete_recurring_recurring_rec_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rec_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_recurring_recurring_get**
> List[RecurringOut] list_recurring_recurring_get()

List Recurring

List all recurring transaction templates.

### Example


```python
import openapi_client
from openapi_client.models.recurring_out import RecurringOut
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
    api_instance = openapi_client.RecurringApi(api_client)

    try:
        # List Recurring
        api_response = api_instance.list_recurring_recurring_get()
        print("The response of RecurringApi->list_recurring_recurring_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RecurringApi->list_recurring_recurring_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[RecurringOut]**](RecurringOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

