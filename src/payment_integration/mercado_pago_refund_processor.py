from .refund_processor import RefundProcessor


class MercadoPagoRefundProcessor(RefundProcessor):
    def refund(self, amount: float) -> str:
        return f"mercado_pago:refunded:{amount:.2f}"
