# Upsilon — product design concept

A responsive front-end concept for a clearer founder–investor discovery experience. The project is plain HTML, CSS, and JavaScript; it has no build step or package dependencies.

## Preview

Open `index.html` directly in a browser, or run a local static server from this folder:

```powershell
python -m http.server 4173
```

Then visit `http://localhost:4173`.

## Screens

- `index.html` — responsive marketing landing page with distinct founder and investor entry points.
- `workspace.html` — founder match results, visible reasons, fit caveat, save states, and a prototype introduction action.
- `investor.html` — investor discovery with thesis-alignment reasons and independently verifiable profile signals.
- `onboarding.html` — four-step founder profile and criteria flow.
- `case-study.html` — heuristic audit, research hypotheses, identity and contrast rationale, before/after mapping, and component starter.
- `output/pdf/Upsilon_Product_Design_Case_Study.pdf` — concise, shareable case-study PDF.

## Notes for review

All investor/startup profiles and activity dates shown in the interactive demo are illustrative. Match labels describe visible criteria overlap; they are not investment recommendations. No real introductions are sent and there is no backend or persistent account state. The audit references the public site at `upsilonbyaks.com`; its annotated evidence panels are reconstructions, not captured source screenshots. The personas are hypotheses, not interview findings. The case study documents these limitations and a validation plan.

Lora and Open Sans are bundled locally under `assets/fonts` with their OFL licenses, so the prototype renders consistently without a network connection.
