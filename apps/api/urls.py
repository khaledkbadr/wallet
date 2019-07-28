# POST /transers
#   body: {from: <account_id>, to: <account_id>, amount: <>}

# GET /transers
# GET /balances
# POST /balances (create a balance)
# ASSUMPTION: no deposits or withdrawls happen

from django.urls import path

from .views import BalanceListCreate, TransferListCreate

urlpatterns = [
    path("balances/", BalanceListCreate.as_view()),
    path("transfers/", TransferListCreate.as_view()),
]
