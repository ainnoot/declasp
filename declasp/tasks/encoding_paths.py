from pathlib import Path

ENCODING_FOLDER = Path(__file__).parent / "encodings"
DECLARE_ENCODING = ENCODING_FOLDER / "declare.lp"
CONFORMANCE_CHECKING_ENCODING = ENCODING_FOLDER / "conformance_checking.lp"
QUERY_CHECKING_ENCODING = ENCODING_FOLDER / "query_checking.lp"
SATISFIABILITY_ENCODING = ENCODING_FOLDER / "satisfiability.lp"
