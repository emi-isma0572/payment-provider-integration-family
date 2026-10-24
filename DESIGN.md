# Design Notes — Payment Provider Integration Family

## 1. Product roles Checkout actually needs

| Role (contract)          | Responsibility                               | Concrete products                                   |
|--------------------------|----------------------------------------------|-----------------------------------------------------|
| `PaymentAuthorizer`      | Authorize (reserve) an amount                | Stripe / Adyen / MercadoPago `Authorizer`           |
| `RefundProcessor`        | Refund an amount                             | Stripe / Adyen / MercadoPago `RefundProcessor`      |
| `WebhookVerifier`        | Validate that a webhook comes from provider  | Stripe / Adyen / MercadoPago `WebhookVerifier`      |

## 2. Chosen pattern: Abstract Factory

`PaymentProviderFactory` is the single creation contract for a whole family:

```
PaymentProviderFactory (ABC)
 ├─ create_authorizer()        -> PaymentAuthorizer
 ├─ create_refund_processor()  -> RefundProcessor
 └─ create_webhook_verifier()  -> WebhookVerifier

StripePaymentFactory · AdyenPaymentFactory · MercadoPagoPaymentFactory
```

**Why not Factory Method?** Factory Method creates *one* product through a
subclass hook. Here Checkout needs *three related products* that must always
come from the same provider. Using three separate factory methods would let a
caller combine a Stripe authorizer with an Adyen webhook verifier. Abstract
Factory makes the family the unit of creation, so consistency is guaranteed by
construction.

## 3. Who selects the concrete family?

`PaymentProviderSelector` (composition root) maps a configuration value such as
`"mercado_pago"` to a factory object. It is the **only** class that knows all
providers. `CheckoutService` receives the factory through its constructor
(dependency injection) and only imports `PaymentProviderFactory`.

```python
factory = PaymentProviderSelector().factory_for("mercado_pago")
checkout = CheckoutService(factory)
```

## 4. Defense questions

- **What varies?** The provider: Stripe, Adyen, Mercado Pago (and future ones).
  Each provider changes *all three* capabilities at once.
- **What stays stable?** The checkout workflow (authorize → refund → verify
  webhook) and the three role contracts.
- **Why family-level?** The three products only make sense together: a Stripe
  webhook verifier cannot validate events for an Adyen payment. Choosing the
  provider is one decision that must produce a coherent set of objects.
- **Pattern & why:** Abstract Factory — one factory object per family, one
  creation boundary, no mixing, and new providers are added by extension (OCP)
  without editing `CheckoutService`.
- **Complexity cost:**
  - More classes/files: 4 contracts + 4 classes per provider (3 products + 1 factory).
  - Adding a provider = 4 new files + 1 line in the selector.
  - Adding a **new capability** (e.g. `create_payout_processor`) is expensive:
    the abstract factory and *every* concrete factory must change.
  - Extra indirection makes the flow harder to follow for small cases.

## 5. Tests

- `test_checkout_service.py` — behavior for all three families; a fake family
  proves Checkout only needs the contracts; an AST check proves
  `checkout_service.py` imports nothing but the abstract factory.
- `test_provider_factories.py` — each factory satisfies the contract and every
  product belongs to the same family; contracts cannot be instantiated.
- `test_payment_provider_selector.py` — name → family resolution, unsupported
  provider rejected, injected factories, end-to-end wiring.
