# Truthful TDD Examples

## Tautological oracle

```ts
// Bad: expected repeats the implementation's algorithm.
const items = [{ price: 10 }, { price: 5 }];
const expected = items.reduce((sum, item) => sum + item.price, 0);
expect(calculateTotal(items)).toBe(expected);

// Good: the requirement's worked example is independent and inspectable.
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
```

If both production and test accidentally skip the last item, the first test can agree with the bug. The second can disagree.

## Default-value false positive

```ts
// Bad: zero can pass even if insert ignores the supplied value.
map.insert("key", 0);
expect(map.get("key")).toBe(0);

// Good: key and value are distinct, non-default values.
map.insert("account-17", 42);
expect(map.get("account-17")).toBe(42);
```

## Change detector disguised as a unit test

```ts
// Bad: mirrors internal choreography and breaks under harmless refactoring.
processor.run(work);
expect(first.process).toHaveBeenCalledWith(work);
expect(second.process).toHaveBeenCalledWith(work);

// Good: observes the public result the choreography exists to produce.
const result = processor.run(work);
expect(result.completedSteps).toEqual(["validated", "persisted"]);
```

If ordering is itself a public safety contract, assert the externally visible ordering at the event, transaction, or output seam—not private method sequence.

## Vertical UI slice

```ts
// Bad: bypasses whether the button is disabled, hidden, or wired correctly.
await controller.handleBuyClick(product);
expect(payment.charge).toHaveBeenCalled();

// Good: the UI is the public seam.
render(<PurchasePage product={product} />);
await user.click(screen.getByRole("button", { name: "Buy" }));
expect(await screen.findByText("Purchase confirmed")).toBeVisible();
```

Prefer a real in-process purchase service backed by an ephemeral database. If charging a real provider is destructive, replace only the owned payment adapter and cover that adapter against the provider sandbox separately.

## Narrow boundary mock

```ts
// Acceptable: induce a rare transport failure at an owned external boundary.
const paymentGateway: PaymentGateway = {
  charge: async () => { throw new TimeoutError(); },
};

const result = await checkout(cart, paymentGateway);
expect(result).toEqual({ status: "retryable", reason: "payment-timeout" });
```

The mock contains no protocol logic and the assertion observes checkout behavior. Separate contract tests must still prove the real gateway adapter maps provider timeouts to `TimeoutError`.

## A vertical cycle

For “a suspended user cannot create an order”:

1. **Seam:** `POST /orders` with the real route, auth policy, service, and ephemeral database.
2. **Red:** create a suspended user and valid cart; expect `403` plus no retrievable order. Observe the current incorrect success.
3. **Green:** add the smallest policy enforcement that makes the route test pass.
4. **Refactor:** clarify policy placement while the route test remains green.
5. **Next slice:** test the active-user success behavior separately.

Mocking the policy service would turn the test into a claim about the mock. Calling a private `canOrder()` helper would bypass the route's identity, middleware, and persistence wiring.
