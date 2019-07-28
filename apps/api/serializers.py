import decimal

from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import AccountBalance, Transfer


class BalanceSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="account")

    class Meta:
        model = AccountBalance
        exclude = ["account"]
        extra_kwargs = {"currency": {"read_only": True}}


class TransferCreateSerializer(serializers.Serializer):
    from_account = serializers.CharField()
    to_account = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        fields = ("from_account", "amount", "to_account")

    def create(self, validated_data):
        prim_account = validated_data.pop("from_account")
        sec_account = validated_data.pop("to_account")
        amount = validated_data.pop("amount")

        if decimal.Decimal(amount) < decimal.Decimal("0.0"):
            raise ValidationError("amount can't be negative")

        with transaction.atomic():
            # Lock accounts' balance row, preventing anyone else from changing the balance

            prim_acc_ins = AccountBalance.objects.select_for_update().filter(
                account=prim_account
            )
            AccountBalance.objects.select_for_update().filter(account=sec_account)

            # Update the account's total and add a Transfer row atomically
            prim_acc_ins = AccountBalance.objects.get(account=prim_account)
            prim_acc_ins.balance = prim_acc_ins.balance - decimal.Decimal(amount)
            prim_acc_ins.full_clean()
            prim_acc_ins.save()

            sec_acc_ins = AccountBalance.objects.get(account=sec_account)
            sec_acc_ins.balance = sec_acc_ins.balance + decimal.Decimal(amount)
            sec_acc_ins.save()

            timestamp = timezone.now()
            t1 = Transfer.objects.create(
                primary_account=prim_acc_ins,
                secondary_account=sec_acc_ins,
                amount=amount,
                direction="outgoing",
                timestamp=timestamp,
            )

            Transfer.objects.create(
                primary_account=sec_acc_ins,
                secondary_account=prim_acc_ins,
                amount=amount,
                direction="incoming",
                timestamp=timestamp,
            )
            return t1


class TransferListSerializer(serializers.ModelSerializer):
    account = serializers.CharField(source="primary_account.account")

    class Meta:
        model = Transfer
        exclude = ["primary_account", "id", "secondary_account"]
        read_only_fields = ["timestamp", "direction"]

    def to_representation(self, obj):
        seco_account_type = serializers.CharField(source="secondary_account.account")
        if obj.direction == "outgoing":
            self.fields["to_account"] = seco_account_type
            self.fields.pop("from_account", None)
        else:
            self.fields["from_account"] = seco_account_type
            self.fields.pop("to_account", None)

        try:
            del self._readable_fields  # Clear the cache
        except AttributeError:
            pass
        return super().to_representation(obj)
