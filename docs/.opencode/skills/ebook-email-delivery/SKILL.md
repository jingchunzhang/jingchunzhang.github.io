---
name: ebook-email-delivery
description: Insert ebook-specific subscription forms into blog posts and deliver the matching download link automatically after signup.
version: 1.0.0
---

# Ebook Email Delivery

## Use this skill when
- A blog post needs an email subscription CTA.
- Each ebook subscriber must receive the correct download link automatically.
- The site is static and cannot rely on a custom backend by default.

## Recommended architecture
Default recommendation: **MailerLite** for a static GitHub Pages/Jekyll workflow.

Reason:
- embedded form works on static pages
- automation is available without building a custom backend first
- per-group or per-form automation can send ebook-specific download links

## Fixed business inputs
- Contact email: `contact@tangyou.space`
- Every ebook should have a unique identity, download URL, and associated signup entry point.

## Required funnel behavior
1. User sees an embedded form inside a blog post.
2. Form submission identifies the requested ebook.
3. Subscriber enters the correct group/tag/automation path.
4. Automation sends the matching ebook download URL.
5. Follow-up emails can promote:
   - the independent site
   - relevant affiliate offers
   - additional blog articles

## Implementation rules
- Use one of these mapping strategies:
  - one MailerLite group per ebook
  - one form per ebook
  - one hidden ebook identifier field that maps to different automations
- Keep form embed code reusable across articles.
- Store the final download URL alongside the ebook identifier.
- Use a sender identity based on your domain, not a free mailbox brand.

## Deliverables
- Form embed snippet or reusable include/component
- ebook identifier mapping strategy
- automation flow design
- welcome email copy with the correct download URL
- follow-up sequence suggestions for monetization

## Email copy requirements
- Email 1: deliver the requested ebook immediately.
- Email 2+: offer a related article, an independent-site solution, or an affiliate recommendation.
- Keep subject lines clear and low-spam.

## Domain and deliverability checklist
- Use `contact@tangyou.space` or another domain mailbox as the sender identity.
- Configure SPF, DKIM, and DMARC before scaling.
- Avoid misleading medical or income claims in email copy.
