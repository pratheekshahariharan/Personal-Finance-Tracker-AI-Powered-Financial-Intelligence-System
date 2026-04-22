# openapi_client.DashboardApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_pdf_report_report_pdf_get**](DashboardApi.md#download_pdf_report_report_pdf_get) | **GET** /report/pdf | Download Pdf Report
[**get_dashboard_dashboard_get**](DashboardApi.md#get_dashboard_dashboard_get) | **GET** /dashboard | Get Dashboard
[**get_gamification_stats_gamification_get**](DashboardApi.md#get_gamification_stats_gamification_get) | **GET** /gamification | Get Gamification Stats
[**get_optimization_advice_optimization_get**](DashboardApi.md#get_optimization_advice_optimization_get) | **GET** /optimization | Get Optimization Advice
[**import_transactions_csv_csv_import_post**](DashboardApi.md#import_transactions_csv_csv_import_post) | **POST** /csv/import | Import Transactions Csv


# **download_pdf_report_report_pdf_get**
> object download_pdf_report_report_pdf_get()

Download Pdf Report

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
    api_instance = openapi_client.DashboardApi(api_client)

    try:
        # Download Pdf Report
        api_response = api_instance.download_pdf_report_report_pdf_get()
        print("The response of DashboardApi->download_pdf_report_report_pdf_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DashboardApi->download_pdf_report_report_pdf_get: %s\n" % e)
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

# **get_dashboard_dashboard_get**
> DashboardOut get_dashboard_dashboard_get(month=month, year=year)

Get Dashboard

Return financial KPIs and recent activity.

### Example


```python
import openapi_client
from openapi_client.models.dashboard_out import DashboardOut
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
    api_instance = openapi_client.DashboardApi(api_client)
    month = 56 # int |  (optional)
    year = 56 # int |  (optional)

    try:
        # Get Dashboard
        api_response = api_instance.get_dashboard_dashboard_get(month=month, year=year)
        print("The response of DashboardApi->get_dashboard_dashboard_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DashboardApi->get_dashboard_dashboard_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **month** | **int**|  | [optional] 
 **year** | **int**|  | [optional] 

### Return type

[**DashboardOut**](DashboardOut.md)

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

# **get_gamification_stats_gamification_get**
> GamificationStatus get_gamification_stats_gamification_get()

Get Gamification Stats

### Example


```python
import openapi_client
from openapi_client.models.gamification_status import GamificationStatus
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
    api_instance = openapi_client.DashboardApi(api_client)

    try:
        # Get Gamification Stats
        api_response = api_instance.get_gamification_stats_gamification_get()
        print("The response of DashboardApi->get_gamification_stats_gamification_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DashboardApi->get_gamification_stats_gamification_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GamificationStatus**](GamificationStatus.md)

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

# **get_optimization_advice_optimization_get**
> List[OptimizationRecommendation] get_optimization_advice_optimization_get()

Get Optimization Advice

### Example


```python
import openapi_client
from openapi_client.models.optimization_recommendation import OptimizationRecommendation
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
    api_instance = openapi_client.DashboardApi(api_client)

    try:
        # Get Optimization Advice
        api_response = api_instance.get_optimization_advice_optimization_get()
        print("The response of DashboardApi->get_optimization_advice_optimization_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DashboardApi->get_optimization_advice_optimization_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[OptimizationRecommendation]**](OptimizationRecommendation.md)

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

# **import_transactions_csv_csv_import_post**
> object import_transactions_csv_csv_import_post(file, month=month, year=year)

Import Transactions Csv

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
    api_instance = openapi_client.DashboardApi(api_client)
    file = 'file_example' # str | 
    month = 56 # int |  (optional)
    year = 56 # int |  (optional)

    try:
        # Import Transactions Csv
        api_response = api_instance.import_transactions_csv_csv_import_post(file, month=month, year=year)
        print("The response of DashboardApi->import_transactions_csv_csv_import_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DashboardApi->import_transactions_csv_csv_import_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **str**|  | 
 **month** | **int**|  | [optional] 
 **year** | **int**|  | [optional] 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

