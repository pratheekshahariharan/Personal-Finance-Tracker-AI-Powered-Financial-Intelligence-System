# openapi_client.TransactionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_transaction_transactions_post**](TransactionsApi.md#add_transaction_transactions_post) | **POST** /transactions/ | Add Transaction
[**delete_transaction_transactions_transaction_id_delete**](TransactionsApi.md#delete_transaction_transactions_transaction_id_delete) | **DELETE** /transactions/{transaction_id} | Delete Transaction
[**export_csv_transactions_export_get**](TransactionsApi.md#export_csv_transactions_export_get) | **GET** /transactions/export | Export Csv
[**get_summary_transactions_summary_get**](TransactionsApi.md#get_summary_transactions_summary_get) | **GET** /transactions/summary | Get Summary
[**list_transactions_transactions_get**](TransactionsApi.md#list_transactions_transactions_get) | **GET** /transactions/ | List Transactions
[**reclassify_transactions_transaction_id_reclassify_patch**](TransactionsApi.md#reclassify_transactions_transaction_id_reclassify_patch) | **PATCH** /transactions/{transaction_id}/reclassify | Reclassify


# **add_transaction_transactions_post**
> TransactionOut add_transaction_transactions_post(transaction_create)

Add Transaction

Add a new transaction with auto-categorization and duplicate detection.

### Example


```python
import openapi_client
from openapi_client.models.transaction_create import TransactionCreate
from openapi_client.models.transaction_out import TransactionOut
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
    api_instance = openapi_client.TransactionsApi(api_client)
    transaction_create = openapi_client.TransactionCreate() # TransactionCreate | 

    try:
        # Add Transaction
        api_response = api_instance.add_transaction_transactions_post(transaction_create)
        print("The response of TransactionsApi->add_transaction_transactions_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->add_transaction_transactions_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_create** | [**TransactionCreate**](TransactionCreate.md)|  | 

### Return type

[**TransactionOut**](TransactionOut.md)

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

# **delete_transaction_transactions_transaction_id_delete**
> delete_transaction_transactions_transaction_id_delete(transaction_id)

Delete Transaction

Delete a transaction by ID.

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
    api_instance = openapi_client.TransactionsApi(api_client)
    transaction_id = 56 # int | 

    try:
        # Delete Transaction
        api_instance.delete_transaction_transactions_transaction_id_delete(transaction_id)
    except Exception as e:
        print("Exception when calling TransactionsApi->delete_transaction_transactions_transaction_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 

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

# **export_csv_transactions_export_get**
> object export_csv_transactions_export_get()

Export Csv

Download all transactions as a CSV file.

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
    api_instance = openapi_client.TransactionsApi(api_client)

    try:
        # Export Csv
        api_response = api_instance.export_csv_transactions_export_get()
        print("The response of TransactionsApi->export_csv_transactions_export_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->export_csv_transactions_export_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

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

# **get_summary_transactions_summary_get**
> object get_summary_transactions_summary_get(month=month, year=year)

Get Summary

Monthly summary grouped by category (expenses shown as positive values).

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
    api_instance = openapi_client.TransactionsApi(api_client)
    month = 56 # int |  (optional)
    year = 56 # int |  (optional)

    try:
        # Get Summary
        api_response = api_instance.get_summary_transactions_summary_get(month=month, year=year)
        print("The response of TransactionsApi->get_summary_transactions_summary_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->get_summary_transactions_summary_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **month** | **int**|  | [optional] 
 **year** | **int**|  | [optional] 

### Return type

**object**

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

# **list_transactions_transactions_get**
> List[TransactionOut] list_transactions_transactions_get(month=month, year=year, category=category, transaction_type=transaction_type, search=search)

List Transactions

List all transactions with optional filters.

### Example


```python
import openapi_client
from openapi_client.models.transaction_out import TransactionOut
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
    api_instance = openapi_client.TransactionsApi(api_client)
    month = 56 # int |  (optional)
    year = 56 # int |  (optional)
    category = 'category_example' # str |  (optional)
    transaction_type = 'transaction_type_example' # str |  (optional)
    search = 'search_example' # str |  (optional)

    try:
        # List Transactions
        api_response = api_instance.list_transactions_transactions_get(month=month, year=year, category=category, transaction_type=transaction_type, search=search)
        print("The response of TransactionsApi->list_transactions_transactions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->list_transactions_transactions_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **month** | **int**|  | [optional] 
 **year** | **int**|  | [optional] 
 **category** | **str**|  | [optional] 
 **transaction_type** | **str**|  | [optional] 
 **search** | **str**|  | [optional] 

### Return type

[**List[TransactionOut]**](TransactionOut.md)

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

# **reclassify_transactions_transaction_id_reclassify_patch**
> TransactionOut reclassify_transactions_transaction_id_reclassify_patch(transaction_id, reclassify_request)

Reclassify

Manually override the auto-assigned category.

### Example


```python
import openapi_client
from openapi_client.models.reclassify_request import ReclassifyRequest
from openapi_client.models.transaction_out import TransactionOut
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
    api_instance = openapi_client.TransactionsApi(api_client)
    transaction_id = 56 # int | 
    reclassify_request = openapi_client.ReclassifyRequest() # ReclassifyRequest | 

    try:
        # Reclassify
        api_response = api_instance.reclassify_transactions_transaction_id_reclassify_patch(transaction_id, reclassify_request)
        print("The response of TransactionsApi->reclassify_transactions_transaction_id_reclassify_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->reclassify_transactions_transaction_id_reclassify_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 
 **reclassify_request** | [**ReclassifyRequest**](ReclassifyRequest.md)|  | 

### Return type

[**TransactionOut**](TransactionOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

