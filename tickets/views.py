import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
import pandas as pd
import django as Da
import tickets.serializers as ser
from rest_framework.permissions import IsAuthenticated
from urllib3.util.retry import Retry
from rest_framework import status
from datetime import datetime, timedelta
from rest_framework.decorators import api_view,permission_classes

BearerToken = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4ZjllYjNmNi02ZWZhLTRmZWYtODk1ZS1kMWJjNDRiYTQ4MWQiLCJqdGkiOiIyODE4NzYzY2VlM2MyNjRjNWY4OGI0ZjJiYjM0MWFkYzdkMDcxNGRhMDM5YzkxNzI4NzNiNTc5ODhlODMwZGE3NGM2ZTk0YTY0NmZjODliNiIsImlhdCI6MTcxNjk4NDMxMC43NTE4OTYsIm5iZiI6MTcxNjk4NDMxMC43NTE4OTYsImV4cCI6MTg3NDc1MDcxMC43MTcwNDIsInN1YiI6IjljMjhhNjllLTQ5MGYtNDc0OS1iNWYzLWY5YzBlNDNlZjAxZSIsInNjb3BlcyI6WyJnZW5lcmFsLnJlYWQiLCJvcGVyYXRpb25zLnJlYWQiLCJpbnZlbnRvcnkudHJhbnNhY3Rpb25zLnJlYWQiLCJjb3Vwb25zLnJlYWQiLCJjdXN0b21lcnMubGlzdCIsIm9yZGVycy5naWZ0X2NhcmRzLnJlYWQiLCJjdXN0b21lcnMuYWNjb3VudHMucmVhZCIsIm1lbnUuaW5ncmVkaWVudHMucmVhZCIsImludmVudG9yeS5zZXR0aW5ncy5yZWFkIiwiY3VzdG9tZXJzLmxveWFsdHkucmVhZCIsIm9yZGVycy5saXN0IiwidXNlcnMucmVhZCIsInJlc2VydmF0aW9ucy5saW1pdGVkLnJlYWQiXSwiYnVzaW5lc3MiOiI5YzI4YTY5ZS01ZTk4LTQ0ZGMtYTdjOS1kMzJlMzljNjFlNDYiLCJyZWZlcmVuY2UiOiIzODE3NDMifQ.GQUO-u0LRfH5fZ9xum4_ZolIjxuVLt4KSaz33rnzQS2lQTLMrspXm2LP_CjtGrGtdimthJDJt-YdtEtEjGMfJEeFdiHx3Rg6O7C71sISc9tULTutzGmE4jwjmUt1rbWM18Nr5Cfq1YEfKvWDxWZxhJ8TeAdJv9M7zaZVS8umdLNpyNdYSIzbuVdJNaed7rXaouUo-lj33CYOFzRVvdFh3lA8vHb7fJNSTXzppSPngoiyGzEDlVsVgcaukklb_c849IigjtPNqVafw8-WnM7ZylpNaUnmjXCibc1DfeZM-09P1g_UB8sLWdziMGVvfPQihW3v26Q7d7DqYEzHj2fsBDJxYIo4a3A310xfw_W6dECTwkPb_Qk0dAPlft9zK3qMQVon4nCJUXWwj9P05LaK5iaO_eDKYdXnl2jar5CRLzPJj4C2e41ZqxQ3HIRVWZysItTUUiA_igVhZx4RGPwIKQt_KlPkgV8WA1CdwixUHMPny4BxQBNo3hA47bXyYVM65UTHW1pMPxGk1NVL7gRRDLY39zCo3LMAPd230dC73gqCytuPysCKY7UlKevSM_ikMS8WVnCa8D2f-6i_v6f6QCQEoFAk1c3Tcsvy2u-05swrm4BwtoqZnSP6K47nLjGX0WRXBXn1iPB1DfpoDIapRxgy5gt0dUId2zwh7aKHp30"
BaseUrl = "https://api-sandbox.foodics.com/v5"
header= {"Authorization": BearerToken}  


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllOrdersView(self,request):
    url = f"{BaseUrl}/orders/"
    try:
        response = requests.get(url, headers=header,timeout=30)
        total_orders = response.json()["meta"]["total"]
        return Response({"Totle": total_orders} , status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
class GetAllcustomers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self ,request):
        url=f"{BaseUrl}/customers/"
        try:
            response= requests.get(url,headers=header,timeout=30).json()            
            return Response ({"Totale":response["meta"]["total"]}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred : {e}")
class GetTotleIncoming(APIView):
    permission_classes = [IsAuthenticated]


    def get(self,request):
        url = f"{BaseUrl}/orders/"
        try:
            response = requests.get(url, headers=header, timeout=30)
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            orders = data.get("data", [])
            df = pd.DataFrame(orders)
            columns_to_display = ["id", "created_at", "total_price", "reference", "check_number"]
            df_selected = df[columns_to_display]
            total_income = ser.CalculateSumOfIncoming.calc(data) 
            return Response({"total_income": total_income}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class GetIncomingWithfilter(APIView):
    permission_classes = [IsAuthenticated]
  
    def get(self, request, *args, **kwargs):
        try:
            days = self.kwargs['days']
            current_date = datetime.now()
            url = f"{BaseUrl}/orders?include=branch"
            response = requests.get(url, headers=header, timeout=30)
            response.raise_for_status()

            # Calculate the start date for the last 'days' days
            start_date = current_date - timedelta(days=days)

            data = response.json()["data"]
            
            # Filter orders created within the last 'days' days
            filtered_orders = [order for order in data if datetime.fromisoformat(order["created_at"]) >= start_date]
            
            # Create a dictionary containing the filtered orders
            parsed_response = {
                "data": filtered_orders
            }

            # Return the JSON response
            return JsonResponse(parsed_response)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return JsonResponse({"error": "An error occurred"}, status=500)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)
class GetTopBranches(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def fetch_filtered_orders(days):
        try:
            current_date = datetime.now()
            url = f"{BaseUrl}/orders?include=branch"
            response = requests.get(url, headers=header, timeout=30)
            response.raise_for_status()

            # Calculate the start date for the last 'days' days
            start_date = current_date - timedelta(days=days)

            data = response.json()["data"]
            
            # Filter orders created within the last 'days' days
            filtered_orders = [order for order in data if datetime.fromisoformat(order["created_at"]) >= start_date]
            
            return filtered_orders

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get(self, request, *args, **kwargs):
        try:
            days = kwargs['days']
            filtered_orders = self.fetch_filtered_orders(days)
            
            if filtered_orders is None:
                return JsonResponse({"error": "An error occurred"}, status=500)

            # Create DataFrame from orders data
            df = pd.DataFrame(filtered_orders) 

            # Extract branch information
            df['Branch_id'] = df['branch'].apply(lambda x: x['id'])    
            df['Branch_name'] = df['branch'].apply(lambda x: x['name'])
            
            # Group by branch and sum total prices
            grouped = df.groupby(['Branch_id', 'Branch_name']).agg({'total_price': 'sum'}).reset_index()
            # Sort by total price in descending order
            sorted_grouped = grouped.sort_values(by='total_price', ascending=False)

            # Convert grouped DataFrame to dictionary
            result = sorted_grouped.to_dict(orient='records')
            #return top five : df.loc[0,1,2,3,4]

            return JsonResponse({"data": result}, safe=False)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)
