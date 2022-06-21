from rest_framework import serializers
# files 是 app 的名字
from publicSubmits import models


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FilesModel
        fields = '__all__'