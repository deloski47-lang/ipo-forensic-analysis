---
title: IPO Forensic Analysis Engine — UI/UX Design Specification
document_id: DESIGN-IPO-001
version: 1.1
status: Design baseline updated; exact 21st.dev hero component remains product-owner-selected
last_updated: 29 October 2026
canonical_source: Markdown in GitHub
scope: Indian Mainboard IPOs only; local-first; single-user; manual-first; ₹0 budget
---

# IPO Forensic Analysis Engine
## UI/UX Design Specification

> **Purpose:** Define the visual system, page layout, information hierarchy, reusable interface components, interaction patterns, transitions and accessibility rules for the IPO Forensic Analysis Engine. This document follows the approved PRD, the application-flow specification and the proposed Technical Design. It is a build specification for the non-hero application experience, not an invented marketing page or a replacement for the product owner's chosen hero code.

**Important ownership decision:** The hero section is intentionally unspecified. The product owner will supply the source code/design for that section later. Do not design, implement, animate, resize, rewrite, or make assumptions about its layout until that source is provided. This specification does define the rest of the application UI and a consistent motion system for non-hero screens.

---

## 1. Design goals and product character

The product should feel like a **modern, premium financial research workspace**: calm, precise, responsive and confident without becoming promotional or visually noisy. It is for examining evidence, contradictions, financial statements and conditional listing-day scenarios—not for gamifying trading or promising gains.

### 1.1 Design goals

1. **Trust before spectacle.** Sources, periods, units, timestamps, uncertainty and calculation lineage must be easy to inspect.
2. **Editorial, light and refined.** Use the specified near-white background and sage-green palette with strong dark typography, clean spacing and restrained borders.
3. **Modern motion, not distracting motion.** The app should feel fluid and intentional through fast state transitions, shared-layout movement where useful, crisp hover/focus feedback, well-behaved drawers/dialogs and tasteful data reveals.
4. **Dense information, clear hierarchy.** Financial tables need room to breathe without turning every row into a floating card.
5. **Progressive disclosure.** Show the decision-relevant summary first and allow the user to open provenance, calculation details and methodology when needed.
6. **Honest states.** Missing, unverified, conflicting, stale, invalid, not-applicable, blocked and failed states must look different and remain explicit.
7. **Accessible by default.** Keyboard, focus, text contrast, screen-reader status messages and reduced motion are design requirements, not late polish.
8. **Local-first and zero-budget.** The UI must not imply cloud sync, subscriptions, login, billing or a mandatory API. Manual workflows remain first-class.

### 1.2 Visual personality

Use these qualities as the design filter:

- Refined and contemporary, similar to a well-crafted financial research product.
- Strong typography and consistent alignment.
- Quiet sage accents, dark ink text and generous near-white negative space.
- Subtle depth through borders, layered surfaces and restrained shadows—not glass effects on every component.
- Motion with a clear purpose: continuity, feedback, hierarchy or orientation.
- No stock-market neon, casino-style red/green flashes, glowing charts, oversized gradients, excessive blur, noisy parallax, or ornamental animation around every number.
- No fabricated dashboard metrics, fake IPO names or decorative chart data in production UI.

---

## 2. Hero section — source fixed; component choice reserved for the product owner

### Source website: [21st.dev](https://21st.dev/) (referred to as “21.dev” by the product owner)

**Decision recorded:** The hero section will be sourced from a selected hero component on 21st.dev. The product owner will choose the exact component and provide its component page/link or copied code. The exact component URL is not yet known and must not be guessed by Claude or another coding agent.

The individual components in the 21st.dev registry can have their own dependencies and licence/usage terms. Before integrating the chosen component, inspect its actual source page, author, licence/usage conditions, required packages, assets and external requests. Use only a component that can be used within the **₹0 total project budget**. Do not purchase premium templates, paid copies, credits or subscriptions. Browsing/free copy limits and plan descriptions may change; do not assume an unlimited free allowance or sign up for a paid tier.

**Current terms check (29 October 2026):** 21st.dev's published Marketplace Terms (last updated 20 July 2026) state that components/materials belong to their respective authors and/or 21st Labs, restrict redistribution, and require a clear, visible link to the original component page when copying/redistributing a component to another medium. They also restrict reuse of marketplace previews/media and structured metadata without permission. Therefore, when a selected component is lawfully reusable in this project, preserve the author's attribution and include a clear, visible link near the hero or in a directly discoverable credits area to the exact original component page. Do not copy 21st.dev's screenshots, demo videos, thumbnails, preview layouts or unrelated site assets. If the chosen component's author licence or the terms applicable to the intended use are unclear, do not integrate it until clarified. References: [21st.dev Terms of Service](https://21st.dev/terms) and [21st.dev Plans & Pricing](https://21st.dev/plans).

The hero must retain its selected source's intended look and motion as far as compatible with our product constraints, then be integrated into our design tokens and application structure without copying unrelated site-wide styles or scripts. The rest of the application must not be redesigned to imitate the source website.

Until the owner supplies the exact component:

- Do not invent hero copy, headline, illustration, dashboard preview, CTA placement, background, height, responsive layout, scroll behaviour or animation.
- Do not decide whether the supplied hero belongs to a separate intro/landing view, the case-list screen, or another location until the actual code/context is provided.
- Do not create a fake hero as a placeholder that accidentally becomes the final design.
- Do not import a website's entire global stylesheet or global JavaScript just to get the hero effect.
- When the supplied code arrives, isolate the hero styles, scripts, components and assets from the rest of the application. Preserve the intended design, but check dependencies, licence/attribution requirements, responsive behaviour, accessibility, performance, and conflicts with the app's global tokens.
- The supplied hero may have its own animation sequence. Do not force it into the non-hero transition timing in this document without reviewing the actual source.
- The hero must not introduce paid dependencies, analytics, external trackers, remote databases or a required cloud service.
- Any external assets/font requests must have a fallback; the local-first app's core workflow cannot depend on the hero's remote assets loading.
- Do not alter the global app-shell navigation or page-transition contract to imitate the source website if that breaks the established application flow.

**Integration gate:** once the product owner supplies the exact 21st.dev component URL or code and identifies its intended screen, review it in isolation, record the author/source/licence, list its dependencies/assets/network requests, check compatibility with React and the existing motion package, adapt only what is necessary, and test responsiveness, accessibility, reduced motion and performance. Add the visible link to the exact original component page and author credit required by the applicable 21st.dev terms. If any required feature needs a paid component, subscription, AI credit, API or private package, stop and ask the owner rather than incur a cost; choose a compatible free component only with the owner's direction. Record the actual component URL and resulting dependency decision here in place. Until then, do not select or implement the hero on the owner's behalf.

---

## 3. Brand tokens — fixed by the product owner

The following palette and typography are provided decisions. Preserve the values exactly unless the product owner explicitly changes them.

### 3.1 Exact colour palette

| Token | Value | Intended use |
|---|---|---|
| Text / ink | #10130c | Main text, headings, labels, icons and high-contrast outlines. |
| Background | #fcfdfb | Main page background and primary light canvas. |
| Primary | #8ea06d | Primary action surfaces, selected states, key decorative accents and restrained emphasis. |
| Secondary | #b3ccb1 | Soft supporting surfaces, pale section fills, subtle borders and secondary decorative accents. |
| Accent | #87b18c | Small accents, selected indicators, fine chart highlights and restrained emphasis. |

Required CSS variables:

~~~css
:root {
  --text: #10130c;
  --background: #fcfdfb;
  --primary: #8ea06d;
  --secondary: #b3ccb1;
  --accent: #87b18c;
}
~~~

Do not substitute a blue fintech palette, dark dashboard theme or another green palette. Additional *supporting* tokens for surfaces, borders, focus, motion and semantic statuses may be introduced only to implement the system consistently; they must not replace or silently modify these five brand values.

### 3.2 Colour use and contrast

**The five palette values are fixed exactly as supplied by the product owner. Do not change them in the name of accessibility.** Preserve the tokens, and make accessible component choices around them.

The dark text on the near-white background has approximately 18.37:1 contrast. Dark text on primary, secondary and accent filled surfaces also exceeds 4.5:1. However, primary (#8ea06d), secondary (#b3ccb1) and accent (#87b18c) do not achieve 4.5:1 as text directly on the near-white background.

Therefore:

- Use #10130c as the default text colour on the light canvas.
- Use dark text on primary/secondary/accent filled surfaces.
- Do not use the light green tokens as small body text on #fcfdfb.
- Do not communicate success, warning, conflict or danger solely through one shade of green.
- Use text labels/icons alongside semantic status styling.
- Use a high-contrast dark outline for keyboard focus when a sage outline alone is insufficient.
- Before release, test actual text/surface combinations rather than assuming the palette is accessible from hue alone.
- Preserve the palette while adding contrast-safe component treatments.

WCAG 2.2 AA requires at least 4.5:1 contrast for normal text and 3:1 for large text in the relevant text-contrast criterion. The actual rendered colour pair is what matters, including labels, placeholders, disabled controls that are still meaningful, charts and hover/focus text.

### 3.3 Supporting surface and shape tokens

The exact base colours stay fixed. Additional neutral surface/border tokens may be derived for consistency. The first implementation should keep them very close to the given palette and avoid introducing unrelated brand colours.

Recommended semantic token names:

- --surface: default component surface.
- --surface-soft: subtle secondary area.
- --border: quiet boundary for cards/tables/forms.
- --border-strong: more visible boundary for selected or active elements.
- --focus-ring: high-contrast focus indicator.
- --shadow-soft: subtle elevation for overlays.
- --success, --warning, --danger, --info: status-specific tokens selected with contrast checks.

Do not invent an additional marketing gradient as a foundational token. Do not hard-code the same hex values in dozens of components; define them once in the theme.

### 3.4 Surface hierarchy

Use four levels at most:

1. **Page canvas:** #fcfdfb.
2. **Primary surface:** same or near-white, normally separated with a fine border.
3. **Soft surface:** a restrained sage-tinted fill for selected rows, metadata groups, filters or quiet callouts.
4. **Overlay surface:** a clearly bounded popover, dialog, drawer or menu, with a soft shadow only when it improves layering.

Cards should not be the answer to every layout problem. Use cards for a coherent group of information or a distinct action; use aligned sections/tables for large sets of financial data.

---

## 4. Typography system — fixed by the product owner

### 4.1 Font family and weights

Use Afacad Flux for body and headings:
- Body weight: 400.
- Headings h1–h5 weight: 700.
- Body fallback: sans-serif/system stack so the app remains readable if the web font is unavailable.

The product owner supplied this Google Fonts import:

~~~css
@import url('https://fonts.googleapis.com/css?family=Afacad%20Flux:700|Afacad%20Flux:400');
~~~

Preserve Afacad Flux as the selected font. For implementation, a stylesheet link with suitable preconnect behaviour and `display=swap` may be preferable to a blocking CSS import, but do not silently substitute the family. Because the app is local-first, the UI must remain usable when Google Fonts cannot be fetched: fall back cleanly and never block application startup on the font request. Do not make core app functionality depend on Google Fonts being online.

### 4.2 Exact base type scale

The supplied values are the base scale and should be retained:

~~~css
html {
  font-size: 100%; /* 16px */
}

body {
  font-family: 'Afacad Flux', sans-serif;
  font-weight: 400;
}

h1, h2, h3, h4, h5 {
  font-family: 'Afacad Flux', sans-serif;
  font-weight: 700;
}

h1 { font-size: 3.366rem; } /* 53.92px */
h2 { font-size: 2.525rem; } /* 40.32px */
h3 { font-size: 1.894rem; } /* 30.24px */
h4 { font-size: 1.421rem; } /* 22.72px */
h5 { font-size: 1.066rem; } /* 17.12px */
small { font-size: 0.600rem; } /* 9.6px */
~~~

The app may use a component-specific responsive scale at narrower breakpoints, but the base values above are the chosen type scale. Do not reset them to arbitrary framework defaults without review.

### 4.3 Data-heavy application typography

The global scale is not a reason to render critical financial information too small.

- Use the chosen heading levels to establish hierarchy, not as a mandate to use a 54px title on every internal screen.
- Internal page titles usually use a compact application-heading treatment; large H1 sizing can be reserved for the owner-controlled hero or major page-intro area once its role is settled.
- Financial values should use consistent numeric alignment and readable size.
- Use tabular numerals where supported for prices, percentages, shares, dates and counts.
- Units, periods, currency, status and sign must remain visible; do not rely on a number alone.
- The provided small token is 9.6px, which is too small for essential data, validation errors, source timestamps or status text. Preserve the token, but restrict it to nonessential microcopy/decorative metadata; important UI content should normally be at least 12px (0.75rem) and should still pass contrast/readability checks.
- Avoid using all-caps for long labels. All-caps may be used sparingly for short category labels.
- Don't italicize whole result tables or use font weight alone to convey evidence confidence.

### 4.4 Numeric display conventions

Financial values should look consistent across pages:
- Align number columns by decimal point or right edge where practical.
- Use consistent precision within a table for the same metric.
- Keep minus signs and percentage signs visible.
- Pair figures with unit/currency and period, inline or in an adjacent column/header.
- Do not animate numerical values by counting from zero to the final amount; this can resemble live trading data and mislead users.
- When highlighting a calculation, visually distinguish calculated value from raw source value and scenario assumption.

---

## 5. Application shell and non-hero page structure

This design covers the application shell and the user journeys in app-flow.md. It does not invent the hero section.

### 5.1 Shell layout

Recommended layout for the research workspace:

- **Application navigation:** a compact sidebar or responsive navigation rail for Cases, with secondary navigation available inside a selected case.
- **Top context bar:** current case/issue identity and explicit identity status once inside a case; minimal app-level utilities only.
- **Main content area:** page title, concise contextual explanation, primary action, content sections and relevant state messages.
- **Optional contextual panel/drawer:** used for evidence details, source locators, calculation traces or a finding's detail when opening it inline improves continuity.
- **Responsive navigation:** collapse the sidebar into a menu/compact rail on narrow viewports; do not compress dense financial tables until unreadable.

The shell must look like a focused research application, not a public marketing SaaS with pricing, profile, login, billing or cloud-sync navigation.

### 5.2 Navigation map

The following screen names/routes come from the application-flow specification and should remain aligned with it:

| Screen | Route pattern | Visual/interaction priority |
|---|---|---|
| Cases / Home | /cases | Saved case list, create action, clear empty/error state. |
| Create case | /cases/new | Minimal form, identity clarification and validation. |
| Case overview | /cases/{caseId} | Identity, evidence/review status, readiness and latest saved run. |
| Evidence | /cases/{caseId}/evidence | Evidence inventory, metadata, upload/manual registration. |
| Facts & Review | /cases/{caseId}/facts | Data table, candidate review, conflict resolution, validation. |
| Analysis & Findings | /cases/{caseId}/analysis | Preflight checklist, run action, result/failure states. |
| Scenarios | /cases/{caseId}/scenarios | Assumptions, return results, cost/input limitations. |
| Saved run | /cases/{caseId}/runs/{runId} | Historical snapshot, results, findings and provenance. |
| Report | /cases/{caseId}/reports/{reportId} | Preview, sources, limitations, export and history. |
| Settings | /settings | Essential local-data/backup guidance only, if implemented. |

These are frontend routes, not API endpoint declarations. Stable identifiers belong in route paths; never use issuer display name as the only route identity.

### 5.3 Page framing

Internal pages should consistently use:
1. A clear page title.
2. A short explanation of the page's job, only when it adds context.
3. A primary action where one exists.
4. Summary/readiness/state information relevant to the current task.
5. The core content (table, form, findings, report or evidence list).
6. Secondary details, provenance and advanced controls revealed on demand.

Avoid repeating large page introductions and oversized hero-like titles on every internal route. Leave actual hero design to the owner.

### 5.4 Width and spacing

- Use a centered content area for detail/report screens while allowing evidence and financial tables to use wider space.
- Keep consistent horizontal gutters and vertical spacing across screens.
- Group related fields; avoid one card per individual form input.
- Use whitespace to separate concepts, not to waste the entire viewport.
- Prefer a consistent spacing scale (e.g. 4/8/12/16/24/32/40px) and shared CSS variables/components.
- Use subtle dividers for long research sections; avoid nested cards and heavy outlines everywhere.
- Sticky elements are permitted only when they aid navigation or context and do not conceal focused content on smaller viewports.

---

## 6. Reusable component design

Components should be named for their domain purpose, not their visual appearance alone. Visual styles must be centralized and consistent.

### 6.1 Core shared components

- AppShell
- PrimaryNavigation / CaseNavigation
- PageHeader (not the hero section)
- Breadcrumbs or back-to-case link where useful
- PrimaryButton / SecondaryButton / IconButton
- TextField / NumberField / DateField / SelectField / TextArea
- FormField with label, description and error
- StatusBadge with text label
- InlineAlert / ErrorPanel / EmptyState
- LoadingIndicator / Skeleton
- DataTable / NumericCell / UnitLabel
- EvidenceRow / EvidenceDetails
- SourceCitation / SourceLocator
- AcquisitionStatusPanel / SourceAcquisitionRow / RefreshSourcesAction
- FactReviewPanel / CandidateDecisionControls
- ConflictComparison
- ReadinessChecklist
- FindingRow / FindingDetails
- FormulaTrace
- ScenarioInput / ScenarioComparison
- ReportPreview / ReportActions
- ConfirmDialog
- Drawer / Popover / Tooltip
- Toast/StatusAnnouncer
- DataQualitySummary

Do not make these fully generic before there is a real use case. Build a reusable component after a second use or when consistent behaviour is critical.

### 6.2 Buttons

**Primary button**
- Use primary sage (#8ea06d) with dark text (#10130c).
- One clear primary action per major page region.
- Use a modest radius; avoid pill-shaped controls everywhere.
- Hover: slightly stronger border/brightness and a tiny translate or shadow change, not a scale explosion.
- Active: short press feedback (subtle scale or inset) with a rapid return.
- Disabled: visibly unavailable and accompanied by a reason when the reason is not obvious.
- Busy/loading: show progress and prevent duplicate submission where appropriate; retain an accessible label.

**Secondary button**
- Neutral/near-white surface, strong text and a clear border.
- Use for navigation, cancel and alternate actions.
- Destructive actions must not look like ordinary secondary actions.

**Icon button**
- Use only when the icon meaning is predictable; otherwise add a text label or tooltip.
- Provide a minimum practical touch target around 44px where possible.
- Always define accessible name and focus style.

### 6.3 Forms

- Labels must remain visible; placeholder text is not the label.
- Provide units, period and source context near financial inputs.
- Validate inline and at the form level.
- Preserve values when validation or a network/local API request fails.
- Use explicit Save/Accept/Resolve actions for consequential changes.
- Don't auto-save accepted facts or conflict resolutions invisibly.
- Explain why an action is blocked.
- Use confirmation dialogs for destructive/irreversible actions, not for every routine save.
- Do not introduce a multi-step wizard for a task that can be completed clearly on one screen.

### 6.4 Status badges and alerts

Status should use a text label and, where useful, a supporting icon. Colour is additional reinforcement.

Required conceptual statuses include: Ready, Needs attention, Blocked, Missing, Not applicable, Unverified/Review required, Conflicting, Stale, Failed and Saved.

Rules:
- Never display “Saved” before persistence confirms success.
- Never use green to imply that all evidence is trustworthy.
- Warnings and errors should explain their impact and the next action.
- A missing optional input is different from an invalid required input.
- A report's data-quality status must remain visible in exported form too.
- Semantic colors and focus indicators require contrast checks.

### 6.5 Cards, tables and findings

**Cards**
- Use for coherent summaries, readiness groups, distinct result groups or scenario panels.
- Avoid nested card stacks.
- Avoid making every metric a large floating tile.

**Tables**
- Mainboard IPO evidence and financial research will use dense tabular information. Use clear column headers, units, periods and numeric alignment.
- Preserve table row identity and don't animate every row when sorting/filtering a large dataset.
- Row hover should be subtle.
- Selected row should have a clear background and a non-colour-only state.
- Important row action should be discoverable without making every row jump on hover.
- On narrow screens, let tables scroll horizontally or switch to a deliberate stacked row view; do not squash numbers into unreadable columns.
- Maintain header/context when sticky, and ensure sticky elements do not obscure keyboard focus.

**Findings**
- Show severity/relevance as a reasoned label, not a decorative arbitrary score.
- Allow progressive disclosure: short conclusion, why it triggered, inputs/evidence, alternative explanations and unresolved status.
- Show counter-evidence instead of visually burying it.
- Do not present allegations or hypotheses with the same visual treatment as verified disclosures.

### 6.6 Evidence and source citations

- A source link/locator should look interactive and clearly open the registered source/detail.
- If the original file is local, open the local evidence preview or metadata view; don't fabricate an external URL.
- Display source title, publisher/type, date/period and page/section locator when available.
- Unknown page/time fields should be clearly unavailable, not populated with a guessed value.
- Make it possible to get back to the same fact/finding/run after inspecting evidence.
- Do not use colour alone to distinguish official vs unofficial sources; include text such as “Official filing” or “Unofficial observation”.

### 6.7 Drawers, dialogs and overlays

Use a drawer when the user needs to inspect details and return to the underlying table without losing context. Use a dialog for a focused decision that needs acknowledgement.

- Opening moves focus into the overlay.
- Closing returns focus to the triggering element.
- Escape closes non-destructive overlays where appropriate.
- Destructive confirmation names the specific action and consequence.
- Overlay entrance and exit are fast and unobtrusive.
- Background interaction is prevented when modal semantics require it.
- Don't rely on hover alone for primary actions; it will not exist on touch devices.
- Avoid large translucent frosted-glass overlays that reduce text contrast.

---

## 7. Motion system — modern, polished, purposeful

### 7.1 Motion direction

The desired motion is modern and premium, with an intentional sense of continuity. The “sexy” quality should come from confident easing, smooth shared movement, careful timing and small tactile responses—not from constant animation.

Use:
- Fast, precise feedback on interaction.
- Short crossfades and small directional movement between route content.
- Shared-layout continuity when an item visibly moves into a details view.
- Spring motion for small, interruptible layout/selection changes, with low bounce.
- Short, controlled modal/drawer motion.
- Subtle staged reveal when a page first appears, only for a small number of meaningful elements.
- Data visualizations that reveal the existing data without implying the values themselves are changing.

Do not use:
- Long full-screen transitions that delay task completion.
- Heavy parallax or scroll-jacking.
- Continuous floating, pulsing, shimmering or glowing on all controls.
- Bouncy movement on serious financial warnings.
- Rotating numbers, spinning logos, exaggerated overshoot or giant scaling.
- Animations that make users wait to click or keyboard-navigate.
- A different animation style on every component.

### 7.2 Recommended implementation approach

**Recommended baseline:** CSS transitions for simple hover/focus/active states, plus **Motion for React** (npm package: motion; imports from motion/react) for route/content presence, shared layout and complex state changes where CSS alone would be awkward.

This is a recommended dependency, not something already installed or tested. During the scaffold, confirm its React compatibility, pin a compatible version in the lockfile, and keep the imported feature set small. Use only the free/open-source `motion` package under its MIT license. Do not use Motion+, `motion-plus`, Motion UI from the private registry, premium APIs, paid examples or paid editor/audit features. Do not add GSAP or a second animation library on top unless a concrete requirement demonstrates a need.

The hero selected from 21st.dev may itself import `framer-motion`, `motion`, or another library. Do not blindly install a second motion system. Inspect the actual component first: prefer adapting it to the existing open-source motion dependency when this preserves the chosen effect and is technically sound. If a separate dependency is genuinely required to preserve the selected hero behaviour, verify its cost/licence/compatibility, explain the trade-off and document the decision before adding it. No paid Motion+ feature or other paid dependency may be introduced.

Native CSS View Transitions may be evaluated later as progressive enhancement, but do not build two competing route-transition systems or animate the same component with both Motion and View Transitions. The initial MVP should have one predictable motion implementation that can be disabled/reduced and tested.

### 7.3 Timing tokens

These are initial design tokens to calibrate during implementation:

| Token | Duration | Use |
|---|---:|---|
| --motion-instant | 80–120ms | Press feedback, checkbox/toggle response, tiny active state. |
| --motion-fast | 120–180ms | Hover, focus decoration, tooltip, badge/state change. |
| --motion-standard | 180–260ms | Small drawers, route content, drop-down/open-close interactions. |
| --motion-emphasis | 260–360ms | Shared layout movement, selected panels, compact dialog entry. |
| --motion-reveal | 400–650ms | A one-time chart/path reveal or a deliberate visual moment, not normal form actions. |

Normal interactions should generally stay in the instant/fast/standard ranges. Emphasis/reveal durations must never delay access to the actual content. Stagger delays should be small (roughly 20–35ms) and restricted to a short list; don't stagger an entire long evidence table.

### 7.4 Easing and feel

- For opacity and small positional transitions, use a smooth ease-out/ease-in-out curve.
- Use modest spring motion only when the user changes a selection, reorders/expands layout or follows a shared element.
- Prefer low bounce and short settling time.
- Use a quicker exit than entry so closing a panel feels responsive.
- Ensure transitions are interruptible where practical.
- Never ease a progress indicator in a way that falsely implies backend work is progressing when it has not reported progress.

Exact Motion transition objects and easing constants should be defined in one shared animation/token module or theme, not copy-pasted into dozens of components.

### 7.5 Transition catalogue

| Interaction | Expected motion | Design constraints |
|---|---|---|
| Route/content change | Current content fades out quickly; next content fades in with about 6–10px of vertical movement over 180–260ms. | Keep shell/navigation stable; no full-screen zoom. Respect reduced motion. |
| Case row to case detail | The selected case/context may use a shared-layout highlight or short fade. | Don't animate the entire case list and page simultaneously. Keep URLs/history correct. |
| Sidebar/current navigation | Active marker/underline moves or fades smoothly; label remains crisp. | No sliding full sidebar on every click. Active state also uses semantics/contrast. |
| Button hover | Small change in border, surface, shadow or 1–2px vertical position over 120–180ms. | No 1.1x scale on primary actions; support touch devices. |
| Button active | Brief subtle pressed state over 80–120ms. | Must not alter hit target or delay activation. |
| Dropdown/popover | Fade and small translate (about 4px) over 120–180ms. | Correct focus, Escape and outside-click behaviour. |
| Dialog | Fade in with subtle scale from about 0.98 to 1 over 160–220ms. | Avoid large zoom; focus management is mandatory. |
| Drawer | Small horizontal entry (about 8–14px) plus fade over 180–240ms. | Width and direction adapt on mobile; do not animate the whole page. |
| Tabs | Active underline/background moves smoothly; content crossfade only if it improves continuity. | Preserve focus/ARIA semantics and do not reload data merely to animate. |
| Accordion/details | Content height/opacity transition with a clear disclosure icon state. | Must still be usable if animation is skipped; avoid animating huge content blocks. |
| Toast/status message | Short fade/translate. | Do not automatically dismiss important data-loss/security errors before the user can read them. |
| Loading skeleton | Quiet shimmer only while genuinely loading. | Stop when load completes; use static skeleton under reduced motion; never use a fake progress percentage. |
| Chart entrance | Reveal chart line/area once, with axes and labels stable. | No random data, no animated values from zero, no visual suggestion of live price changes. |
| Table sort/filter | A brief row reflow or simple content update. | For large lists, prioritize immediate correct data over choreography. |
| Candidate accepted/rejected | Subtle status transition and local row update after server-confirmed save. | Do not animate the state as accepted before persistence succeeds. |
| Conflict resolved | Clear status change after saved resolution; details remain discoverable. | Never animate conflicting values away or hide history. |
| Report export | Progress/success state based on actual operation result. | Don't show success confetti; do not claim generated before file exists. |

### 7.6 The animation must tell the truth

Motion cannot imply the application has completed a calculation, saved a fact or generated a report when it hasn't. Start/finish states must follow actual application state.

- A save animation begins when save starts and resolves only on confirmed success/failure.
- A new finding can fade in after the saved run returns, not before the backend result exists.
- Don't animate financial numbers as if they were live ticker prices.
- Don't auto-run analysis because a screen transition completed.
- If a route loads slowly, show a real loading state and allow cancellation/back navigation where technically safe.
- Animation failure must never prevent access to underlying content or keyboard interaction.

### 7.7 Reduced motion

Respect the operating system/browser prefers-reduced-motion preference throughout the site. Under reduced motion:
- Remove large positional travel, parallax and scale-based entrances.
- Replace complex transitions with a short opacity change or immediate state switch.
- Disable nonessential chart drawing/reveal and skeleton shimmer.
- Do not use spring/bounce animation.
- Keep status and focus changes clearly visible without motion.
- Ensure every interaction works when animation is instantly skipped.

The app must not require the user to find a hidden setting to make OS-level reduced motion work.

### 7.8 Performance rules

- Prefer transform and opacity animation where practical.
- Avoid repeatedly animating layout-heavy properties across large tables.
- Avoid reading layout and writing layout in a loop during animation.
- Don't mount a heavy motion wrapper around every table cell/number.
- Use shared layout transitions only where continuity helps comprehension.
- Respect lower-power devices and browser fallback behaviour.
- Test on representative browsers/screen sizes after implementation.
- No animation may block typing, saving, navigation, focus or scrolling.
- Use the browser's native scroll behaviour; do not hijack wheel/touch scroll.

---

## 8. Responsive behaviour

The app is a data-heavy desktop-oriented research workspace, but it must remain usable on tablet and mobile.

### 8.1 Breakpoint strategy

Use the project's chosen CSS breakpoints consistently rather than sprinkling ad hoc media queries. A practical starting point is:
- Mobile: below 640px.
- Tablet: 640–1023px.
- Desktop: 1024px and above.
- Wide workspace: 1280px and above.

These values are recommended starting points, not hard device guarantees; validate against real content.

### 8.2 Desktop

- Persistent navigation rail/sidebar.
- Wide, readable evidence/financial tables.
- Optional side detail panel for provenance/finding detail.
- Multiple-column layout only when it aids comparison.
- Keep a clear main-content column and avoid stretching paragraph text across the entire ultrawide screen.

### 8.3 Tablet

- Compact/collapsible navigation.
- Reduce multi-column cards before reducing text size.
- Keep form labels and numeric units visible.
- Use drawers for detail where a permanent panel would squeeze content.

### 8.4 Mobile

- Collapsible navigation.
- Single-column form and case summary.
- Buttons should have useful touch targets and sufficient spacing.
- Tables can scroll horizontally or present designed row cards; don't squeeze key financial columns to fit.
- Use full-width or near-full-width modal/drawer patterns for important workflows where appropriate.
- Preserve source and date context in stacked data rows.
- Avoid hover-only information/action.
- Do not hide critical warnings, conflict state or provenance just to simplify the layout.

### 8.5 Zoom and long content

- Support browser zoom and text resizing.
- Prevent navigation or sticky bars from covering focused inputs.
- Allow long source URLs and document titles to wrap/break safely.
- Ensure dialogs remain usable on short viewports and on-screen keyboards.
- Avoid fixed heights that clip validation errors, citations or tables.

---

## 9. Page-by-page visual direction

This section describes the non-hero visuals. Exact wireframes can be added after the product owner reviews this baseline.

### 9.1 Cases / Home

Visual goal: quick orientation, not a trading dashboard.

- A concise page header and clearly separated “New IPO case” action.
- A clean saved-case list/table with issue identity, current task/status, latest run and recent update where genuinely known.
- An empty state that guides the user to create a case without fictitious sample numbers.
- Show data/storage error distinctly from an empty case list.
- Use one or two summary items only if they help the next action.
- Do not use decorative market ticker strips or fake real-time metrics.

The owner-controlled hero region remains undefined and should not be filled by an invented banner.

### 9.2 Create case

- Focused form with one clear primary action.
- Optional identifiers/issue details should not overwhelm the initial name field.
- Identity status is explicit after save.
- If Mainboard status is uncertain, present a review state rather than silently assume it.
- If an SME IPO is identified, explain the scope boundary and stop the supported analysis path.
- No required network search or source API.

### 9.3 Case overview

- Present issuer/issue identity and status at top of the workspace.
- Show a clear source-acquisition summary after identity resolution: attempted sources, returned signal categories, last attempt/refresh, timestamps/freshness, partial coverage, blocked/unavailable sources and actionable retry/manual fallback.
- Show next steps through an actionable readiness summary.
- Use distinct counts/status summaries for facts needing review, conflicts and missing evidence only when those counts are actually known.
- Keep prior run/report information clearly tied to that run.
- No arbitrary “health score” or unsupported confidence percent.
- Warnings link to the page where they can be resolved.

### 9.4 Evidence inventory

- Favour a readable table with title, source/type, known date/period, review status and locator/file status.
- Show an Add Evidence action.
- Put detailed metadata in a drawer/details panel to avoid a huge default table.
- Distinguish local source file from external URL and user-supplied note.
- Provide file parse errors without hiding that the original might still have been preserved.
- Use the original file's registered identity, not just its filename.

### 9.5 Facts & Review

- Prioritize “Needs review” and “Conflicting” queues.
- Use stable table columns for fact/value/unit/period/source/status.
- Put Accept, Correct, Reject and Mark unresolved actions next to the appropriate candidate.
- Keep raw extracted text and source locator accessible.
- Conflict view must compare all competing values and evidence side-by-side without automatically choosing one.
- Status actions are server-confirmed; motion occurs only after saved state returns.
- Ensure long tables and validation messages remain understandable at mobile widths.

### 9.6 Analysis readiness

- Use an explicit preflight checklist before the run action.
- Display blockers and qualified/partial conditions separately.
- Show information cutoff and relevant freshness limitations.
- Show acquisition status for critical signal families (subscription by category, GMP, company/offer facts and relevant event/context inputs) separately from calculation readiness. A source failure is not a zero and a non-attempted source is not a successful refresh.
- The primary “Run analysis” action is enabled only when required gates pass according to the approved policy; backend validation remains authoritative. Qualified partial analysis must state which signal relationships could not run and why.
- For a blocked action, explain why and link to the resolution screen.
- Don't present a 0–100 completeness ring unless its definition is explicitly approved and meaningful.

### 9.7 Findings/results

- Each finding has a clear short title, a status/severity label with reason, and an expandable explanation.
- Display the relationship tested, values/periods used, supporting evidence, alternative explanations and unresolved questions.
- Allow source/calc detail inspection without losing the current run context.
- Separate verified facts from interpretation and hypothesis.
- Keep metric cards compact and contextual; tables are preferred for many related indicators.
- No animated “score reveal” or glowing red/green flash.

### 9.8 Scenarios

- Make user-entered assumptions visually distinct from observed evidence.
- Use a compact form for scenario label, reference issue price, scenario/exit price or approved alternative input, quantity and any cost assumptions supported by the implementation.
- Compare scenarios in a table or adjacent panels; do not force a chart when a table is clearer.
- Gross return and net return must be explicitly named and visually distinguished.
- Missing costs must be visible; do not show a guessed net return.
- Scenario price is not labeled “predicted price” without a separately validated methodology.

### 9.9 Report preview and history

- Prioritize reading and auditability over dashboard decoration.
- Use typographic hierarchy for sections, findings, methodology and source lists.
- Provide a sticky or easily discoverable report actions area only if it does not obscure content.
- Show run ID/cutoff/date and whether the case has changed since the saved run.
- Material claim/source links and formula traces must be accessible.
- Report export button reflects the formats actually implemented.
- When export fails, keep preview/run accessible and show the real failure.

### 9.10 Settings/local data

- Keep the page small and operational.
- No login, billing, team, cloud-sync or subscription settings.
- Backup/restore controls must state exactly what they do and require explicit confirmation for overwrite/restore.
- The acquisition status panel is a core product component; show connector-level details only for approved/enabled connectors and never imply universal coverage.
- Do not expose saved API secrets in plain text.

---

## 10. Motion implementation examples (non-hero only)

These examples are implementation patterns, not a demand to animate every screen. The hero's motion remains owner-controlled.

### 10.1 CSS micro-interaction tokens

~~~css
:root {
  --motion-instant: 100ms;
  --motion-fast: 150ms;
  --motion-standard: 220ms;
  --motion-emphasis: 320ms;
  --ease-ui: cubic-bezier(0.2, 0.8, 0.2, 1);
  --ease-ui-in: cubic-bezier(0.4, 0, 1, 1);
}

.button {
  transition:
    background-color var(--motion-fast) var(--ease-ui),
    border-color var(--motion-fast) var(--ease-ui),
    box-shadow var(--motion-fast) var(--ease-ui),
    transform var(--motion-instant) var(--ease-ui);
}

.button:hover {
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
~~~

The reduced-motion example is a baseline illustration. Review animation-specific behaviour as well: JavaScript-driven transitions, chart reveals and Motion animations must honour reduced motion too. CSS alone cannot disable every JavaScript animation automatically.

### 10.2 React Motion usage pattern

For a non-hero content region, Motion can provide a short presence transition. Use a stable key tied to the screen/route, and ensure that the router preserves correct history/focus behaviour.

~~~tsx
import type { ReactNode } from "react";
import { AnimatePresence, motion, MotionConfig } from "motion/react";

type AppPageTransitionProps = {
  pageKey: string;
  children: ReactNode;
};

const pageVariants = {
  initial: { opacity: 0, y: 8 },
  enter: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -4 },
};

export function AppPageTransition({ pageKey, children }: AppPageTransitionProps) {
  return (
    <MotionConfig reducedMotion="user">
      <AnimatePresence mode="wait" initial={false}>
        <motion.main
          key={pageKey}
          variants={pageVariants}
          initial="initial"
          animate="enter"
          exit="exit"
          transition={{ duration: 0.22, ease: [0.2, 0.8, 0.2, 1] }}
        >
          {children}
        </motion.main>
      </AnimatePresence>
    </MotionConfig>
  );
}
~~~

This pattern is illustrative and must be integrated with the actual router, TypeScript types and accessibility behaviour. Do not wrap the entire application repeatedly in nested MotionConfig/AnimatePresence components. Decide one root location and test route changes. Motion's reduced-motion setting should be validated with the current package release.

### 10.3 Shared-layout transition

Use shared layout only when it improves spatial continuity—for example, moving the active navigation marker or expanding a selected finding into details. Do not assign shared IDs to repeated items with ambiguous identity or to every table cell.

### 10.4 Route transition rules

- Stable app shell remains visible; the page content transitions.
- Route transition must not reset scroll/focus unpredictably.
- Respect browser back/forward history.
- If route changes while saving, ensure the save finishes or the user is warned about unsaved work.
- If the route transition library cannot preserve the accessibility/focus requirements in a screen, use a simpler immediate change.
- Skip or simplify transitions for rapid repeated navigation and reduced-motion users.

---

## 11. Accessibility and trustworthy data presentation

### 11.1 Accessibility requirements

- Visible labels for every form input.
- Correct semantic headings, button/link roles, field descriptions and table headers.
- Keyboard navigation across all main actions, menus, dialogs and review controls.
- Visible, high-contrast focus style that is not removed.
- Validation errors associated with inputs and summarized where needed.
- Save/run/export status messages announced accessibly.
- Status meaning communicated by text/icon as well as colour.
- Appropriate focus management when opening/closing drawers and dialogs.
- Content remains readable at zoom and narrow widths.
- Reduced-motion preference respected by CSS and JavaScript animation.
- Do not require hover for a core action.
- Avoid flashing, large zooms, repeated pulse animations or parallax as core interaction.

### 11.2 Trust presentation

The interface must make these concepts visibly distinct:
- Verified/cross-checked fact.
- User-entered unverified observation.
- Extraction candidate awaiting review.
- Calculated result.
- Rule-generated finding.
- Interpretation/hypothesis.
- Scenario assumption.
- Unknown, missing, invalid, conflicting, stale, unavailable or not applicable.

A green accent must not imply a fact has been verified. Verification state comes from the data model and validation path, not visual style.

### 11.3 Chart design

Charts are secondary to the evidence table and explanatory text.

- Only plot actual registered/calculated data.
- Include labels, units, time basis and source/cutoff where appropriate.
- Preserve missing gaps; don't connect or interpolate them unless an explicit visible method is approved.
- Avoid red/green alone to encode all positive/negative states.
- Do not use decorative 3D, misleading truncated axes or animation that implies a price is live.
- Provide accessible data table/text summary for important chart content.
- Chart line reveal is allowed only if it reveals existing data without changing numeric values or hiding caveats.

---

## 12. Responsive and motion QA matrix

Before a flow is accepted, test the actual interface at minimum:

| Dimension | Checks |
|---|---|
| Desktop width (e.g. 1440px) | Sidebar, main content width, long tables, selected detail panel, route transitions. |
| Laptop width (e.g. 1024–1280px) | No cramped tables/cards; navigation remains clear. |
| Tablet width (e.g. 768px) | Navigation collapse, filters, forms, drawers. |
| Mobile width (e.g. 360–430px) | Touch targets, single-column forms, horizontal data tables, evidence locators, dialogs and keyboard. |
| Zoom | 200% zoom with no clipped action, inaccessible form or overlapped sticky content. |
| Reduced motion enabled | No large page travel, spring/bounce, shimmer loop or nonessential chart draw. |
| Keyboard-only | Focus order, visible focus, dialog return focus, tab state and errors. |
| Loading/slow response | No fake progress, duplicate submits or saved claims before confirmation. |
| API/storage failure | Error state is distinct from empty data; form values are preserved where safe. |
| Font unavailable/offline | Fallback remains readable and layout doesn't collapse. |
| Long issuer/source/document labels | Text wraps without pushing action controls offscreen. |
| Long tables | Sort/filter is correct; no excessive per-row animation. |

---

## 13. Design acceptance criteria

The design system is ready for implementation when:

1. The five owner-supplied colour values and Afacad Flux type scale are preserved in shared tokens.
2. Supporting tokens do not replace the brand palette.
3. The hero section is explicitly reserved and no invented hero UI is included.
4. The application shell follows the app-flow route map and remains local-first/single-user.
5. Every screen has clear loading, empty, success, failure, validation and relevant partial/conflict states.
6. Reusable components and page spacing are specified well enough to avoid different styles being invented on every screen.
7. Table, number, source, status and evidence visual rules preserve financial clarity and traceability.
8. The non-hero motion system uses one consistent timing/easing vocabulary.
9. The recommended animation approach is validated in the scaffold and pinned only after compatibility checks.
10. OS reduced-motion preference is respected across CSS and JavaScript animations.
11. Keyboard focus, dialog focus, contrast, status labels and responsive layout are tested.
12. No animation conceals missing data, changes a number, fakes progress or claims save/export success before confirmation.
13. No paid asset, paid UI kit, paid animation library or required external runtime service is introduced.
14. The user can complete the local/manual fallback workflow even without internet or remote fonts; when online, the interface clearly surfaces approved source-acquisition attempts and does not imply a source was checked if retrieval failed.
15. The case overview and analysis preflight make acquisition coverage/freshness visible, with distinct attempted/succeeded/partial/unavailable/blocked states.
16. The findings/results presentation supports interconnected comparisons across company/offer fundamentals, valuation, QIB/NII/retail subscription, GMP and relevant company/market events while preserving provenance and contrary evidence.

---

## 14. Open design decisions

These are intentionally left open rather than invented:

| Decision | State | Why it remains open |
|---|---|---|
| Hero layout, content, position and copied animation | **Reserved for product owner** | Owner will provide source/design code later. |
| Whether hero belongs to a separate intro view or the Cases/Home route | Open | Do not infer the route role until the owner supplies the hero context. |
| Final page wireframes and screenshot-based spacing | Later design pass | The component/layout system is defined first; wireframes should follow this baseline. |
| Exact semantic status colours | Requires contrast review | Preserve base palette and choose accessible status treatment during implementation. |
| Exact supporting neutral/border tokens | Recommended to define in theme | Must remain consistent with the palette. |
| Motion package/version | Recommended: Motion for React; validate and pin during scaffold | Check React compatibility and reduced-motion behaviour in the actual app. |
| Browser View Transitions | Deferred/progressive enhancement only | Avoid competing transition systems until the base system is tested. |
| Responsive breakpoints | Suggested starting values; validate against content | Actual table/form layouts determine final breakpoints. |
| Font offline strategy | Fallback required; local font packaging not yet approved | Preserve font choice but don't make online font loading required. |
| Actual report/export component layout | Depends on supported output and report model | Must not claim an unimplemented export format. |

---

## 15. Implementation guidance and coding-agent rules

Any agent building the UI must:

1. Read `AGENTS.md`, `docs/app-flow.md`, the approved PRD and `docs/TECHNICAL_DESIGN.md` before implementing UI.
2. In Claude Code, use Anthropic's verified **Frontend Design** plugin/skill for frontend and UI/UX work: https://claude.com/plugins/frontend-design. Invoke/apply it before planning or implementing visual UI, and use its design-planning and critique workflow for hierarchy, layout, interaction and motion. If unavailable, do not claim it was used; notify the product owner and request that it be enabled before frontend implementation proceeds.
3. The Frontend Design skill is an assistant, not the authority for product requirements. It must follow this design document, `app-flow.md` and approved constraints. It must not alter the exact palette/type choices, invent the hero, add paid dependencies or expand scope.
4. Treat this file as the design baseline for non-hero screens and interactions.
5. Preserve the exact owner-provided palette and typography unless the owner changes them.
6. Do not implement a hero until the product owner provides the exact 21st.dev component URL/code and intended placement.
7. Review the selected component's author, licence and terms before integration. Use no paid component/plan/credit. Add a clear visible link back to the exact original component page and preserve attribution as required. Never copy marketplace previews/media or import a whole website's global styles.
8. Keep CSS variables and motion tokens centralized; avoid per-component hard-coded animation timings.
9. Use CSS transitions for simple states and the agreed free/open-source Motion package for complex movement; do not add competing animation libraries casually. Do not use Motion+ or private paid packages.
10. Respect reduced motion, keyboard access and high-contrast focus.
11. Do not animate fake numbers, pretend loading progress or unpersisted state.
12. Keep financial values, units, dates, status and provenance legible.
13. Use real application data only; placeholder examples must be clearly marked in development and never passed off as real IPO data.
14. Do not introduce paid fonts/assets, analytics, external trackers or required online services.
15. Implement and test screen states, not only the happy path.
16. If a desired hero/transition dependency conflicts with local-first operation, accessibility, performance, licence terms or the zero budget, explain the specific conflict and request a decision rather than silently weakening a constraint.
17. Update this canonical `design.md` in place when approved design decisions change; do not create numbered/dated duplicate versions.

---

## 16. References

Official documentation used to inform the recommended motion/accessibility implementation. Recheck current details during implementation:

- 21st.dev component registry (hero source; exact component is to be selected by the product owner): https://21st.dev/
- Anthropic-verified Frontend Design plugin/skill for Claude Code: https://claude.com/plugins/frontend-design
- Motion for React installation and React/Vite setup: https://motion.dev/docs/react-installation
- Motion package source and MIT license (use the open-source package only; do not use paid Motion+ features): https://github.com/motiondivision/motion
- Motion for React layout animations and shared layout transitions: https://motion.dev/docs/react-layout-animations
- Motion for React exit/presence transitions: https://motion.dev/docs/react-animate-presence
- MDN — View Transition API concepts and browser behaviour: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- MDN — prefers-reduced-motion: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion
- W3C WAI — WCAG 2.2 contrast minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

These references support implementation choices; they do not mean the animation package has already been installed or the app has passed accessibility/runtime tests.

---

## 17. Current recommendation

Use the specified palette and Afacad Flux typography as the shared design foundation. Build a light, precise, premium research workspace with readable data tables, evidence-first status treatments and consistent, tasteful non-hero motion.

**The hero source is 21st.dev; the exact component remains for the product owner to choose.** Once its URL/code is supplied, review its licence/dependencies and integrate it as an isolated component rather than allowing copied styles or animation scripts to destabilize the entire UI.

**Claude Code UI/UX implementation rule:** use the Anthropic-verified Frontend Design skill/plugin for frontend planning, implementation and critique. Do not claim the skill ran unless it was actually available and applied.

The next design step is to review this specification and then produce the screen-level wireframes or visual references for the non-hero workspace. Do not start the Data Contract solely because the design document is complete; follow the established order and finalize contracts before implementing dependent API flows.
