# openapi_client.SavingsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_to_saving_goal_savings_goal_id_add_patch**](SavingsApi.md#add_to_saving_goal_savings_goal_id_add_patch) | **PATCH** /savings/{goal_id}/add | Add To Saving Goal
[**create_saving_goal_savings_post**](SavingsApi.md#create_saving_goal_savings_post) | **POST** /savings/ | Create Saving Goal
[**deposit_to_savings_savings_deposit_post**](SavingsApi.md#deposit_to_savings_savings_deposit_post) | **POST** /savings/deposit | Deposit To Savings
[**get_savings_balance_savings_balance_get**](SavingsApi.md#get_savings_balance_savings_balance_get) | **GET** /savings/balance | Get Savings Balance
[**get_savings_history_savings_history_get**](SavingsApi.md#get_savings_history_savings_history_get) | **GET** /savings/history | Get Savings History
[**list_saving_goals_savings_get**](SavingsApi.md#list_saving_goals_savings_get) | **GET** /savings/ | List Saving Goals
[**withdraw_from_savings_savings_withdraw_post**](SavingsApi.md#withdraw_from_savings_savings_withdraw_post) | **POST** /savings/withdraw | Withdraw From Savings


# **add_to_saving_goal_savings_goal_id_add_patch**
> SavingGoalOut add_to_saving_goal_savings_goal_id_add_patch(goal_id, saving_goal_add)

Add To Saving Goal

### Example


```python
import openapi_client
from openapi_client.models.saving_goal_add import SavingGoalAdd
from openapi_client.models.saving_goal_out import SavingGoalOut
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
    api_instance = openapi_client.SavingsApi(api_client)
    goal_id = 56 # int | 
    saving_goal_add = openapi_client.SavingGoalAdd() # SavingGoalAdd | 

    try:
        # Add To Saving Goal
        api_response = api_instance.add_to_saving_goal_savings_goal_id_add_patch(goal_id, saving_goal_add)
        print("The response of SavingsApi->add_to_saving_goal_savings_goal_id_add_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavingsApi->add_to_saving_goal_savings_goal_id_add_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **goal_id** | **int**|  | 
 **saving_goal_add** | [**SavingGoalAdd**](SavingGoalAdd.md)|  | 

### Return type

[**SavingGoalOut**](SavingGoalOut.md)

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

# **create_saving_goal_savings_post**
> SavingGoalOut create_saving_goal_savings_post(saving_goal_create)

Create Saving Goal

### Example


```python
import openapi_client
from openapi_client.models.saving_goal_create import SavingGoalCreate
from openapi_client.models.saving_goal_out import SavingGoalOut
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
    api_instance = openapi_client.SavingsApi(api_client)
    saving_goal_create = openapi_client.SavingGoalCreate() # SavingGoalCreate | 

    try:
        # Create Saving Goal
        api_response = api_instance.create_saving_goal_savings_post(saving_goal_create)
        print("The response of SavingsApi->create_saving_goal_savings_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavingsApi->create_saving_goal_savings_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **saving_goal_create** | [**SavingGoalCreate**](SavingGoalCreate.md)|  | 

### Return type

[**SavingGoalOut**](SavingGoalOut.md)

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

# **deposit_to_savings_savings_deposit_post**
> SavingsTransactionOut deposit_to_savings_savings_deposit_post(savings_transaction_create)

Deposit To Savings

### Example


```python
import openapi_client
from openapi_client.models.savings_transaction_create import SavingsTransactionCreate
from openapi_client.models.savings_transaction_out import SavingsTransactionOut
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
    api_instance = openapi_client.SavingsApi(api_client)
    savings_transaction_create = openapi_client.SavingsTransactionCreate() # SavingsTransactionCreate | 

    try:
        # Deposit To Savings
        api_response = api_instance.deposit_to_savings_savings_deposit_post(savings_transaction_create)
        print("The response of SavingsApi->deposit_to_savings_savings_deposit_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavingsApi->deposit_to_savings_savings_deposit_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **savings_transaction_create** | [**SavingsTransactionCreate**](SavingsTransactionCreate.md)|  | 

### Return type

[**SavingsTransactionOut**](SavingsTransactionOut.md)

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

# **get_savings_balance_savings_balance_get**
> SavingsBalanceOut get_savings_balance_savings_balance_get()

Get Savings Balance

### Example


```python
import openapi_client
from openapi_client.models.savings_balance_out import SavingsBalanceOut
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
    api_instance = openapi_client.SavingsApi(api_client)

    try:
        # Get Savings Balance
        api_response = api_instance.get_savings_balance_savings_balance_get()
        print("The response of SavingsApi->get_savings_balance_savings_balance_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavingsApi->get_savings_balance_savings_balance_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**SavingsBalanceOut**](SavingsBalanceOut.md)

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

# **get_savings_history_savings_history_get**
> List[SavingsTransactionOut] get_savings_history_savings_history_get()

Get Savings History

### Example


```python
import openapi_client
from openapi_client.models.savings_transaction_out import SavingsTransactionOut
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
    api_instance = openapi_client.SavingsApi(api_client)

    try:
        # Get Savings History
        api_response = api_instance.get_savings_history_savings_history_get()
        print("The response of SavingsApi->get_savings_history_savings_history_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavingsApi->get_savings_history_savings_history_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[SavingsTransactionOut]**](SavingsTransactionOut.md)

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

# **list_saving_goals_savings_get**
> List[SavingGoalOut] list_saving_goals_savings_get()

List Saving Goals

### Example


```python
import openapi_client
from openapi_client.models.saving_goal_out import SavingGoalOut
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
    api_instance = openapi_client.SavingsApi(api_client)

    try:
        # List Saving Goals
        api_response = api_instance.list_saving_goals_savings_get()
        print("The response of SavingsApi->list_saving_goals_savings_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavingsApi->list_saving_goals_savings_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[SavingGoalOut]**](SavingGoalOut.md)

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

# **withdraw_from_savings_savings_withdraw_post**
> SavingsTransactionOut withdraw_from_savings_savings_withdraw_post(savings_transaction_create)

Withdraw From Savings

### Example


```python
import openapi_client
from openapi_client.models.savings_transaction_create import SavingsTransactionCreate
from openapi_client.models.savings_transaction_out import SavingsTransactionOut
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
    api_instance = openapi_client.SavingsApi(api_client)
    savings_transaction_create = openapi_client.SavingsTransactionCreate() # SavingsTransactionCreate | 

    try:
        # Withdraw From Savings
        api_response = api_instance.withdraw_from_savings_savings_withdraw_post(savings_transaction_create)
        print("The response of SavingsApi->withdraw_from_savings_savings_withdraw_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavingsApi->withdraw_from_savings_savings_withdraw_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **savings_transaction_create** | [**SavingsTransactionCreate**](SavingsTransactionCreate.md)|  | 

### Return type

[**SavingsTransactionOut**](SavingsTransactionOut.md)

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

