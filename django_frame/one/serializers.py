from rest_framework import serializers

from one.models import BookInfo


class BookInfoModelSerializers(serializers.ModelSerializer):
    class Meta:
        # 要序列化或者反序列化的模型类
        model = BookInfo
        # 把所有的字段都展示
        # fields = ['id', 'btitle'] 展示指定字段
        fields = "__all__"


def about_django(value):
    if "django" not in value.lower():
        raise serializers.ValidationError("book name is not include Django")


class BookInfoSerializer(serializers.Serializer):
    """book serializers"""
    id = serializers.IntegerField(label="ID", read_only=True)
    # btitle = serializers.CharField(label='名称', max_length=20, validators=[about_django])
    btitle = serializers.CharField(label='名称', max_length=20, )
    bpub_date = serializers.DateField(label="public date", required=False)
    bread = serializers.IntegerField(label="reads", required=False)
    bcomment = serializers.IntegerField(label="comments",required=False)
    image = serializers.ImageField(label="image", required=False)
    heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)

    """self def validate"""
    def validate_btitle(self,value):
        if "f" not in value.lower():
            raise serializers.ValidationError("book name not include f")
        return value

    # todo create and update for save


class HeroInfoSerializer(serializers.Serializer):
    GENDER_CHOICES = (
        (0,"MALE"),
        (1,"FEMALE")
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    hname = serializers.CharField(label='名字', max_length=20)
    hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)
    # 此字段将被序列化为关联对象的主键
    # hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
    # 此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）,hbook return name
    # hbook = serializers.StringRelatedField(label='图书', read_only=True)
    # 使用关联对象的序列化器,could get all hbook info
    hbook = BookInfoSerializer()

