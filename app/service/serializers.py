from rest_framework import serializers

from app.service.models import Program, Borrower, Application
from app.utils.mixins import iin_check


class ApplicationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('status', 'reject_reason')

    def to_representation(self, instance):
        data = super(ApplicationModelSerializer, self).to_representation(
            instance
        )
        if not data['reject_reason']:
            del data['reject_reason']
        return data


class BorrowerAgeAndSumValidateSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    sum = serializers.FloatField()

    def validate(self, attrs):
        sum = attrs.get('sum')
        program = attrs.get('program')
        age = attrs.get('age')
        errors = {}
        if sum > program.max_sum or sum < program.min_sum:
            errors["error"] = "Заявка не подходит по сумме"
        if age > program.max_age or age < program.min_age:
            errors["error"] = "Заемщик не подходит по возрасту"
        return errors


class EnterpreneurshipValidateSerializer(serializers.Serializer):
    iin = serializers.CharField()

    def validate(self, attrs):
        errors = {}
        if iin_check(attrs.get('iin')):
            errors['error'] = "иин является ИП"
        return errors


class BlackListValidateSerializer(serializers.Serializer):
    borrower = serializers.PrimaryKeyRelatedField(queryset=Borrower.objects.all())

    def validate(self, attrs):
        errors = {}
        borrower = attrs.get('borrower')
        if borrower.blacklist_set.exists():
            errors['error'] = "Заемщик в черном списке"
        return errors


class ApplicationCreateSerializer(serializers.Serializer):
    iin = serializers.CharField(max_length=12)
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    sum = serializers.FloatField()

    def create(self, validated_data):
        data = validated_data
        iin = data.get('iin')
        program = data.get('program')
        sum = data.get('sum')
        status = Application.SUCCESS
        reason = ''
        borrower = Borrower.objects.get_or_create(iin=iin)[0]
        data['age'] = borrower.age
        data['borrower'] = borrower.id
        data['program'] = program.id
        age_sum_ser = BorrowerAgeAndSumValidateSerializer(data=data)
        age_sum_ser.is_valid()
        if age_sum_ser.validated_data:
            error = age_sum_ser.validated_data.get('error')
            status = Application.FAILURE
            reason = error
        enterpreneurship_ser = EnterpreneurshipValidateSerializer(data=data)
        enterpreneurship_ser.is_valid()
        if enterpreneurship_ser.validated_data:
            error = enterpreneurship_ser.validated_data.get('error')
            status = Application.FAILURE
            reason = error
        blacklist_ser = BlackListValidateSerializer(data=data)
        blacklist_ser.is_valid()
        if blacklist_ser.validated_data:
            error = blacklist_ser.validated_data.get('error')
            status = Application.FAILURE
            reason = error
        return Application.objects.create(
            program=program,
            borrower=borrower,
            sum=sum,
            status=status,
            reject_reason=reason
        )

    def to_representation(self, instance):
        return ApplicationModelSerializer(instance).data
