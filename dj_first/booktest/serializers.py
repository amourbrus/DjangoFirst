from rest_framework import serializers

from booktest.models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器   serializers """
    class Meta:
        model = BookInfo   # BookInfo
        fields = '__all__'