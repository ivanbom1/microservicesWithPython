## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: **\*\***\_\_\_**\*\***
**Branch**: `module-01/<team-name>` 
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> _Your answer:_

Developer: each service has a single responsibility and a clear boundary — you know exactly where the logging code lives, what it owns, and what it doesn't touch. Adding a new feature to logging-service doesn't require reading auth or game code first.

Deployment team: services can be scaled independently — if activity-service is under heavy load, you spin up more instances of just that service without touching the others. You can also roll back one service without rolling back the entire system.

User: if logging-service crashes, they can still browse games and log in — only activity tracking is affected, not the whole experience.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> _Your answer:_

activity-service -> logging-service.

The line exists because consent and legal compliance is a separate concern from tracking what users do. Activity-service records events; logging-service decides whether it's even legal to store them.
If merged: changing GDPR consent logic means touching the same codebase as activity tracking. One team owns legal compliance, another owns product analytics and merging them forces two teams to work in the same service. And this is a bad practice because they would be stepping on each other's changes, causing merge conflicts, and needing to coordinate deployments for unrelated reasons, etc.


---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> _Your answer:_

Debugging. In a monolith, a failed request has one stack trace in one place. In this system, a request touches the gateway, auth-service, activity-service, and RabbitMQ before anything is logged — if something breaks, the error could be anywhere across five separate logs.

---

_Keep this file. You will refer back to it during the oral presentation._
