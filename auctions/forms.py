from decimal import Decimal
from django import forms


class BidForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
        label="قيمة المزايدة",
        widget=forms.NumberInput(
            attrs={
                "class": "w-full p-3 rounded-xl border border-dateBrown/30 bg-white text-dateBrown "
                         "placeholder-dateBrown/40 focus:border-dateBrown focus:ring-2 "
                         "focus:ring-palmGold outline-none",
                "step": "0.01"
            }
        ),
    )