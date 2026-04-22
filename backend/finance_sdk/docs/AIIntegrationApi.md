# openapi_client.AIIntegrationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**chat_assistant_ai_chat_post**](AIIntegrationApi.md#chat_assistant_ai_chat_post) | **POST** /ai/chat | Chat Assistant
[**chat_assistant_ai_chatbot_query_post**](AIIntegrationApi.md#chat_assistant_ai_chatbot_query_post) | **POST** /ai/chatbot/query | Chat Assistant
[**parse_receipt_ai_receipt_post**](AIIntegrationApi.md#parse_receipt_ai_receipt_post) | **POST** /ai/receipt | Parse Receipt


# **chat_assistant_ai_chat_post**
> object chat_assistant_ai_chat_post(chat_request)

Chat Assistant

NLP Financial Assistant.
Provides context-aware insights based on user transactions for a specific period.

### Example


```python
import openapi_client
from openapi_client.models.chat_request import ChatRequest
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
    api_instance = openapi_client.AIIntegrationApi(api_client)
    chat_request = openapi_client.ChatRequest() # ChatRequest | 

    try:
        # Chat Assistant
        api_response = api_instance.chat_assistant_ai_chat_post(chat_request)
        print("The response of AIIntegrationApi->chat_assistant_ai_chat_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AIIntegrationApi->chat_assistant_ai_chat_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  | 

### Return type

**object**

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

# **chat_assistant_ai_chatbot_query_post**
> object chat_assistant_ai_chatbot_query_post(chat_request)

Chat Assistant

NLP Financial Assistant.
Provides context-aware insights based on user transactions for a specific period.

### Example


```python
import openapi_client
from openapi_client.models.chat_request import ChatRequest
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
    api_instance = openapi_client.AIIntegrationApi(api_client)
    chat_request = openapi_client.ChatRequest() # ChatRequest | 

    try:
        # Chat Assistant
        api_response = api_instance.chat_assistant_ai_chatbot_query_post(chat_request)
        print("The response of AIIntegrationApi->chat_assistant_ai_chatbot_query_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AIIntegrationApi->chat_assistant_ai_chatbot_query_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_request** | [**ChatRequest**](ChatRequest.md)|  | 

### Return type

**object**

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

# **parse_receipt_ai_receipt_post**
> object parse_receipt_ai_receipt_post(file)

Parse Receipt

Receipt OCR that extracts transaction amount and description.
Uses local EasyOCR (Tensor-based) as primary, with Gemini as fallback.

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
    api_instance = openapi_client.AIIntegrationApi(api_client)
    file = 'file_example' # str | 

    try:
        # Parse Receipt
        api_response = api_instance.parse_receipt_ai_receipt_post(file)
        print("The response of AIIntegrationApi->parse_receipt_ai_receipt_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AIIntegrationApi->parse_receipt_ai_receipt_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **str**|  | 

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

