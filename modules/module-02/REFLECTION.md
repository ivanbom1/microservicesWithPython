# Module 2 — Reflection

**Team name**: _______________
**Branch**: `module-02/<team-name>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> *Your answer:*

First of all, on arrival of a new developer it is much easier to get into the project codebase, understand the architecture of whole app and certain features. Also layered structure helps to debug ongoing features.

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

> *Your answer:*

Game Service writes directly to users.created_at

The Game Service needs to query "users who joined during this game's launch window." Instead of asking UserService, it just reads — fine. But then a developer thinks: "I'll sync the user's created_at to match the game's launch date for reporting cohorts.

What breaks:
UserService uses created_at to calculate account age for rate limiting so that new accounts can't post more than 5 reviews/day. User 42's real account age was 3 days. After the write, UserService sees 14 months and the rate limit no longer applies. User 42 spams reviews. Result -> UserService never knew its data changed. No validation, no event, no cache invalidation. The invariant broke silently.

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

> *Your answer:*

Cost of all this structure is valuable time for possible unneeded layers. Simple systems with a few entities might be overwhelmed by all the layers where new features should be integrated. Add a new method and change 5 files is not efficient, and without a specific reason it wouldn't pay off.

The main point is to create a clean, understadable, SECURE, and isolated architecture to combine multiple services used by Game Manager. The tipping point is security and isolation. Game service which uses multiple individual services to exist as a Web App, has to ensure that they play as an orchestra, not a chamber blues improvisational band.
 

*Keep this file. You will refer back to it during the oral presentation.*
