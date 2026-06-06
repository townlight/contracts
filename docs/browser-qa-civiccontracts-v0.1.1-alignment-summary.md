# CivicContracts v0.1.1 Browser QA

Date: 2026-04-28

Scope:

- `docs/index.html` landing page after v0.1.1 / civiccore v1.2.0 alignment.
- Generated public UI from `civiccontracts.public_ui.render_public_lookup_page()`.

Evidence:

- `browser-qa-civiccontracts-v0.1.1-alignment-desktop.png` - docs landing page at 1440px.
- `browser-qa-civiccontracts-v0.1.1-alignment-mobile.png` - docs landing page at 390px.
- `browser-qa-civiccontracts-public-ui-v0.1.1-desktop.png` - public UI at 1440px.
- `browser-qa-civiccontracts-public-ui-v0.1.1-mobile.png` - public UI at 390px.

Findings:

- Version labels show v0.1.1.
- CivicCore dependency language shows the published `civiccore v1.2.0` release wheel.
- Public-facing capability boundary remains honest: no legal interpretation, renewal approval, contract execution, legal advice, live LLM calls, live contract management platforms, or contract system-of-record replacement.
- Mobile screenshots render without right-edge clipping.
