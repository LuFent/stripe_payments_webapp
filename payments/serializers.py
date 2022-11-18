from rest_framework import serializers

class AddToCartSerializer(serializers.Serializer):
   item_id = serializers.IntegerField()
