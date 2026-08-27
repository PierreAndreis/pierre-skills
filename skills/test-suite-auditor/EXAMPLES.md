# Audit Examples

## Useful broad integration test

```ts
test("suspended users cannot create retrievable orders", async () => {
  const user = await db.users.create({ status: "suspended" });
  const response = await app.request("POST", "/orders", {
    as: user,
    body: validOrder,
  });

  expect(response.status).toBe(403);
  expect(await app.request("GET", "/orders", { as: user })).toHaveBody([]);
});
```

Verdict: `essential` or `useful`. It crosses identity, policy, route, service, and persistence. It prevents an unauthorized persisted order. A mutation that skips the suspension policy should make it red.

## Test that tests its mock

```ts
payment.charge.mockResolvedValue({ status: "paid" });
const result = await payment.charge(order);
expect(result.status).toBe("paid");
```

Verdict: `misleading`. It invokes the mock directly and proves only that the framework returns configured data. Delete it unless it is replaced by a real adapter contract test.

## Tautological expected value

```ts
const expected = rows.reduce((sum, row) => sum + row.amount, 0);
expect(calculateBalance(rows)).toBe(expected);
```

Verdict: usually `misleading`. If production also uses the same faulty reduction, the test agrees with the defect. Replace the oracle with an independently worked literal and non-default values.

## Predicted flake

```ts
await click("Save");
await sleep(1000);
expect(await text("Saved")).toBeVisible();
```

Verdict: usefulness depends on the product surface; flake risk is `high`. The fixed delay races slow environments and wastes time on fast ones. Wait for the actual saved state, network response, or durable record.

## Redundant mocked layers

Suppose five tests mock repository, policy, and mail collaborators separately, while one real route integration test exercises all three and catches the same mutations.

1. Add missing meaningful failure cases to the real route suite.
2. Prove the route suite fails when each protected behavior is broken.
3. Delete call-order assertions and mocked layer tests with no unique defect.
4. Keep a pure-function unit test only if dense policy logic has an independent input/output contract.

The result is fewer tests over a larger product surface, not less protection.

## E2E consolidation

Instead of separate E2E tests for each field on a checkout form:

- keep one successful checkout journey across UI, API, payment boundary, persistence, and order history;
- keep one materially different failure journey, such as declined payment with no persisted order;
- cover field permutations in a route or page integration table;
- delete E2E variants that add runtime without unique risk coverage.
