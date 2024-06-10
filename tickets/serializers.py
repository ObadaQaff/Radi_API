from rest_framework import serializers
from tickets.models import User
from tickets.models import Get_Best_Seller
class userserializer (serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'



class Bestserializer (serializers.JSONBoundField):
    class meta:
        model = Get_Best_Seller 
        fields ='__all__'
class CalculateSumOfIncoming:
    @staticmethod
    def calc(data):
        # Assuming 'data' is the correct key; change this based on the actual response structure
        try:
            orders = data["data"]
            total_income = sum(order["total_price"] for order in orders)
            return total_income
        
        except KeyError:
            raise KeyError("Expected key 'data' not found in response")
