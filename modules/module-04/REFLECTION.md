# Module 4 — Reflection

**Team name**: _______________
**Branch**: `module-04/<team-name>`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> *Your answer:*

Activity service finishes its job instantly saving the activity and publishing the message. It doesn't slow down under load because notification delays don't affect it. Thus if notification-service is down, activity-service doesn't fail or need retry logic, it just publishes and moves on.

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> *Your answer:*

HTTP for notifications will lead to bonding notification service with the activity service and result in activity service slowdowns or fails if notification service crashes.

Broker solves both, slowdowns and possible failure of activity service because of notifications. Activity never waits, notification service crash message is being held until the service is up again.

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> *Your answer:*

Users simply never receive the notification. No error, no retry and no indication anything went wrong. They might assume the feature is broken, or never know at all :(

As a developer, nothing in your logs shows a failure at the activity-service level (it published successfully and moved on). The failure is somewhere downstream, silent, unless you specifically built visibility into the notification-service (f.e. implement/integrate a monitoring tool).

---

*Keep this file. You will refer back to it during the oral presentation.*
