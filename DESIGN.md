# ABVX Lab Design Context

Use this file before changing public Lab pages. It is a compact design contract, not a full brand book.

## Design Read

Reading this as: a technical public hub for agent-workflow tools, with a restrained product-sheet language, leaning toward dense developer documentation plus lightweight control-plane UI.

## Visual Language

- quiet, technical, source-backed;
- product names and tool routes should be visible early;
- pages should feel operational rather than decorative;
- avoid SaaS hero gloss, fake app-window chrome, and generic AI gradient identity.

## Typography And Density

- keep copy scan-friendly and compact;
- use headings for navigation, not marketing drama;
- preserve readable line lengths in tool pages and README-derived copy;
- dense tables/ledgers are acceptable when they serve comparison or status review.

## Layout Rhythm

- home page: core stack first, then ledger/control-plane, then supporting tools;
- tool pages: product-sheet structure with clear one-liner, links, capabilities, boundary, and commands;
- repeated cards are acceptable for comparable tools, but avoid making unrelated sections use the same skeleton without a content reason.

## Motion

- default to static;
- use motion only for navigation feedback or state change;
- respect reduced-motion; decorative reveal motion is not a requirement.

## Deterministic Detector Rules

Flag these as review findings when visible in code, screenshots, or rendered pages:

- nested cards or page sections styled as floating cards;
- purple-blue gradient identity without product-specific reason;
- decorative glass/blur that hides tool meaning;
- gray text on colored backgrounds with weak contrast;
- clipped tool names, buttons, table cells, or repo rows at mobile width;
- skipped heading levels or missing visible focus;
- repeated section skeletons across distinct content roles.

## Waivers

Use this format when a detector rule is intentionally allowed:

```text
Rule: <detector rule>
Where: <file/section>
Reason: design-system rule | legacy constraint | owner direction | documented exception
Recheck trigger: <when to revisit>
```

Current standing waivers:

- Comparable tool cards may share a repeated card structure because the page is a catalog. Recheck if cards become the default layout for non-catalog sections.
- Read-only status and repo tables may stay dense because scan speed matters more than landing-page spaciousness. Recheck if mobile clipping appears.
