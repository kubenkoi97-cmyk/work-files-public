"""Rebuild Stage113 from the published full Stage112 workbook and field patch.
Usage: python APPLY_STAGE113_PATCH.py Stage112.xlsx STAGE113_THIRD50_FIELD_PATCH.csv Stage113.xlsx
Requires artifact_tool; never use openpyxl for edits.
"""
import csv
import hashlib
import sys
from pathlib import Path
from artifact_tool import Blob, SpreadsheetFile

STAGE112_SHA256 = "18c9cfc70a12c9e907701e098a602a64e256cbdbc287665cd3c4a6c982e710fd"
if len(sys.argv) != 4:
    raise SystemExit("Usage: python APPLY_STAGE113_PATCH.py <Stage112.xlsx> <patch.csv> <Stage113.xlsx>")
source, patch_file, output = map(Path, sys.argv[1:])
if hashlib.sha256(source.read_bytes()).hexdigest() != STAGE112_SHA256:
    raise ValueError("Unexpected source workbook; patch refused.")
with patch_file.open(encoding="utf-8-sig", newline="") as stream:
    changes = list(csv.DictReader(stream))
assert len(changes) == 16
assert {int(r["excel_row"]) for r in changes} == set(range(117, 123)) | set(range(142, 152))
book = SpreadsheetFile.import_xlsx(Blob.load(str(source)))
sheet = book.worksheets.get_item("Наполнение MIXED")
for change in changes:
    row = int(change["excel_row"])
    assert change["column"] == "AT" and change["stage"] == "113"
    assert sheet.get_range(f"F{row}").values[0][0] == change["sku"], f"SKU mismatch row {row}"
    assert sheet.get_range(f"AT{row}").values[0][0] == change["old_value"], f"Original description mismatch row {row}"
    sheet.get_range(f"AT{row}").values = [[change["new_value"]]]
SpreadsheetFile.export_xlsx(book).save(str(output))
print("Rebuilt Stage113. Note: exporter byte SHA may differ across runs; verify 356×77 cell values.")
