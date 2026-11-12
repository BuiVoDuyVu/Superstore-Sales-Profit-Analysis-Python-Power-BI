"""Download the selected Superstore CSV mirror for educational analysis.

Original example dataset: Tableau Sample - Superstore.
Mirror: https://gist.github.com/SharmaAshwini/8bd642f6c46792a9c40c8ccad60391e9
"""
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]
DEST = BASE / "data" / "raw" / "Sample_Superstore.csv"
SOURCE_PAGE = "https://gist.github.com/SharmaAshwini/8bd642f6c46792a9c40c8ccad60391e9"
RAW_URL = (
    "https://gist.githubusercontent.com/SharmaAshwini/"
    "8bd642f6c46792a9c40c8ccad60391e9/raw/"
    "4fd45d58a0a81c69814d270d7658f5e2a2d81154/Sample_Superstore.csv"
)


def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        print(f"Tệp đã tồn tại: {DEST}")
        return
    try:
        req = Request(RAW_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=25) as resp:
            contents = resp.read()
        if not contents.lstrip().startswith(b"Row ID,"):
            raise ValueError("Nội dung tải về không phải định dạng CSV mong đợi.")
        if contents.count(b"\n") < 9000:
            raise ValueError("Dữ liệu chưa đầy đủ, thiếu số dòng mong đợi.")
        DEST.write_bytes(contents)
        print(f"Đã tải dữ liệu: {DEST.name}, {len(contents):,} bytes")
    except Exception as exc:
        print("Không tải tự động được:", exc)
        print("Cách thủ công: mở", SOURCE_PAGE)
        print("Chọn Raw hoặc Download ZIP, lưu CSV thành:", DEST)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
