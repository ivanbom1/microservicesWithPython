# Module 3 — Reflection

**Team name**: _______________
**Branch**: `module-03/<team-name>`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:*

A single entry point exists to decouple clients from the internal service. Without a gateway, client needs to:
know hostname and port or each service, hardcode the endpoints, manage error responses for each service individually.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?


> *Your answer:*

They're treated differently because of their role in the request:

VALIDATE_USER() (retry + fail hard): This is a business rule. An activity cannot exist without a valid user. If this call fails, the request must fail immediately—the activity must not be saved. Retry once because network glitches shouldn't reject a valid user. If it still fails, the user genuinely doesn't exist or user-service is down; either way, reject.

FETCH_GAME (graceful null fallback): This is enrichment only. The activity is valid and should be saved regardless. Game data is nice-to-have metadata. If game-service is slow or down, return the activity with "game": null and let the client see a partial response rather than fail the entire request.

Consequences:

Missing user -> activity creation rejected
Missing game -> activity created, but game details are null

---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:*

Systemic risk of chaining synchronous calls. This architecture creates a dependency chain all three services must be up and responsive simultaneously. The overall latency is the sum of all three calls.

---

*Keep this file. You will refer back to it during the oral presentation.*
