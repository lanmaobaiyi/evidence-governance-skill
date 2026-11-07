"""Build a deterministic ZIP with the required single top-level skill folder."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_FOLDER = "evidence-governance"


def build(output: Path) -> tuple[int, str]:
    output = output.resolve()
    files = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.resolve() != output
        and ".git" not in path.parts
        and path.suffix.lower() not in {".zip", ".sha256"}
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in files:
            relative = source.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"{SKILL_FOLDER}/{relative}", (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("ZIP CRC check failed")
        names = archive.namelist()
        if not names or any(not name.startswith(f"{SKILL_FOLDER}/") for name in names):
            raise RuntimeError("ZIP must contain one top-level evidence-governance/ folder")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return len(files), digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT.parent / "evidence-governance-skill.zip")
    args = parser.parse_args()
    count, digest = build(args.output.resolve())
    print(f"OK: files={count}; output={args.output.resolve()}; sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



