from pathlib import Path
S=(Path(__file__).parents[1]/"contracts"/"contract.py").read_text()
def test_iterative_lifecycle():
 for x in ("def open_watch(","def scan(","def patch(","NEEDS_PATCH","ESCALATED","CLEARED"):assert x in S
def test_bounded_scan():
 for x in ("complete coverage vector required","ordered indexes required","CLEAR","THIN","MISSING"):assert x in S
def test_patch_guard():
 for x in ("only owner may patch","patch unavailable","int(x.scans)>=3"):assert x in S
def test_no_remote_fixture():assert "nondet.web" not in S and "raw.githubusercontent" not in S

