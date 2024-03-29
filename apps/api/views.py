from rest_framework import generics, status
from rest_framework.response import Response


from . import serializers
from .models import AccountBalance, Transfer


class BalanceListCreate(generics.ListCreateAPIView):
    """List and create AccountBalance"""

    queryset = AccountBalance.objects.all()
    serializer_class = serializers.BalanceSerializer


class TransferListCreate(generics.ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = serializers.TransferListSerializer

    def create(self, request, *args, **kwargs):
        """Create double entry bookkeeping

        """
        write_serializer = serializers.TransferCreateSerializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        if (
            write_serializer.validated_data["from_account"]
            != write_serializer.validated_data["to_account"]
        ):
            self.perform_create(write_serializer)
        content = {"message": "Transfer has finished successfully"}
        return Response(content, status=status.HTTP_201_CREATED)
