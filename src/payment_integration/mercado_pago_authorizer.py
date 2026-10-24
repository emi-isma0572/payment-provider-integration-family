from .payment_authorizer import PaymentAuthorizer


class MercadoPagoAuthorizer(PaymentAuthorizer):
    def authorize(self, amount: float) -> str:
        return f"mercado_pago:authorized:{amount:.2f}"
