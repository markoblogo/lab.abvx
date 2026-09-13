# How To Test (AI)

<!-- AGENTSGEN:START section=how_to_test -->
- Project: `ABVX Lab`
- Stack profile: static

## Commands
- Fast check: `python3 scripts/verify_site.py`
- Full check: `python3 -m compileall -q scripts && python3 -m unittest discover -s tests -v && python3 scripts/verify_site.py`
- Tests: `python3 -m unittest discover -s tests -v`
- Lint: `python3 scripts/verify_site.py`
- Format: `(not detected)`

## Policy
- Run fast checks while editing.
- Run full checks before final output.
- Keep these commands synchronized with `.agentsgen.json` and `.github/workflows/ci.yml`.
<!-- AGENTSGEN:END section=how_to_test -->
