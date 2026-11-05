#!/usr/bin/env python3
"""Build and package the lightweight GEO Citation Lab viewer."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import posixpath
import re
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import quote


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "dist" / "viewer"
DEFAULT_PACKAGE_DIR = REPO_ROOT / "dist" / "release"
MANIFEST_PATH = REPO_ROOT / "deploy" / "manifest.json"
PAPER_DIR = REPO_ROOT / "02-papers"
PAPER_CSV = PAPER_DIR / "00_资料说明" / "论文清单.csv"
LOCAL_PAPER_PDF = (
    "./02-papers/04_AI搜索实证/"
    "04_AI搜索实证_Chinese_Language_Generative_Search_Engines_Citation_Study.pdf"
)
REMOTE_PAPER_PDF = (
    "https://arxiv.org/pdf/2607.15771v1"
)
RELEASE_ASSET_NAME = "geo-citation-lab-viewer.zip"
VIEWER_CHECKSUMS_NAME = "geo-citation-lab-files.sha256"
LEGACY_DIRECTORIES = {
    "01-geo-experiment-data-report": "01-experiments",
    "02-geo-aeo-ai-search-papers": "02-papers",
    "03-cn-geo-citation-dataset": "03-datasets",
}
RELEASE_FILENAMES = set(
    json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["release_assets"]
)
if RELEASE_ASSET_NAME not in RELEASE_FILENAMES:
    raise ValueError(f"{RELEASE_ASSET_NAME} is missing from release_assets")


def _assert_replaceable_output(output: Path) -> None:
    resolved = output.resolve()
    if resolved == Path(resolved.anchor) or resolved == REPO_ROOT.resolve():
        raise ValueError(f"Unsafe viewer output path: {resolved}")

    if output.exists():
        dist_root = (REPO_ROOT / "dist").resolve()
        if dist_root not in resolved.parents:
            raise ValueError(
                "Refusing to replace an existing directory outside the repository dist folder: "
                f"{resolved}"
            )


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _javascript_string_literal(value: str) -> str:
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _build_root_index(target: Path) -> None:
    html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
    if LOCAL_PAPER_PDF not in html:
        raise RuntimeError("Root index paper link marker was not found")
    html = html.replace(LOCAL_PAPER_PDF, REMOTE_PAPER_PDF)
    _write_text(target / "index.html", html)


def _build_paper_catalog(target: Path) -> None:
    html = (PAPER_DIR / "index.html").read_text(encoding="utf-8")
    csv_text = PAPER_CSV.read_text(encoding="utf-8")
    script_marker = "<script>\nconst CSV_PATH ="
    if html.count(script_marker) != 1:
        raise RuntimeError("Paper catalog script marker must occur exactly once")

    viewer_config = (
        "<script>\n"
        f"window.GEO_VIEWER_CSV = {_javascript_string_literal(csv_text)};\n"
        "window.GEO_VIEWER_USE_SOURCE_PDF_URLS = true;\n"
        "</script>\n\n"
    )
    html = html.replace(script_marker, viewer_config + script_marker)
    html = html.replace(
        'href="./README.md"',
        'href="https://github.com/yaojingang/GEOLab/blob/main/'
        '02-papers/README.md"',
    )
    html = html.replace(
        'href="./00_资料说明/checksums.sha256"',
        'href="https://github.com/yaojingang/GEOLab/blob/main/'
        '02-papers/00_资料说明/checksums.sha256"',
    )

    paper_target = target / "02-papers"
    _write_text(paper_target / "index.html", html)
    _copy_file(PAPER_CSV, paper_target / "00_资料说明" / PAPER_CSV.name)


def _write_viewer_checksums(target: Path) -> None:
    lines: list[str] = []
    for source in sorted(path for path in target.rglob("*") if path.is_file()):
        relative = source.relative_to(target).as_posix()
        if "\n" in relative or "\r" in relative or "\\" in relative:
            raise ValueError(f"Unsupported viewer path: {relative!r}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        lines.append(f"{digest}  {relative}")
    _write_text(target / VIEWER_CHECKSUMS_NAME, "\n".join(lines) + "\n")


def _build_interactive_guides(target: Path) -> None:
    source_dir = PAPER_DIR / "interactive-guides"
    guide_target = target / "02-papers" / "interactive-guides"
    with PAPER_CSV.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    pdf_sources = {
        f'../{row["分类"]}/{row["文件名"]}': row["URL"]
        for row in rows if row["文件名"]
    }

    def shared_asset(content: str, suffix: str) -> str:
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
        relative = f"_assets/pgs-{digest}.{suffix}"
        _write_text(guide_target / relative, content)
        return relative

    for source in sorted(source_dir.glob("*.html")):
        html = source.read_text(encoding="utf-8")
        for relative, original_url in pdf_sources.items():
            html = html.replace(relative, original_url)
        css = re.search(
            r"/\* ===== PGS core v2\.0.*?/\* ===== PGS core end ===== \*/",
            html, re.S,
        )
        if css:
            # Course-specific CSS, including SVG fragment URLs, stays inline.
            if "url(" in css.group():
                raise ValueError(f"Shared core CSS has a relative URL: {source.name}")
            asset = shared_asset(css.group(), "css")
            html = html[:css.start()] + (
                f'</style><link rel="stylesheet" href="{asset}"><style>'
            ) + html[css.end():]
        runtime = re.search(
            r"/\* ===== PGS core runtime v2\.0.*?"
            r"(?=/\*\s*(?:=====\s*)?PAPER CONTENT runtime)",
            html, re.S,
        )
        if runtime:
            asset = shared_asset(runtime.group(), "js")
            # Classic scripts execute in the original order and share global bindings.
            html = html[:runtime.start()] + (
                f'</script><script src="{asset}"></script><script>\n'
            ) + html[runtime.end():]
        _write_text(guide_target / source.name, html)
    _copy_file(source_dir / "README.md", guide_target / "README.md")
    _copy_file(source_dir / "论文互动解读页规范.md", guide_target / "论文互动解读页规范.md")


def _build_legacy_routes(target: Path) -> None:
    for old, new in LEGACY_DIRECTORIES.items():
        for source in sorted((target / new).rglob("*")):
            if not source.is_file():
                continue
            # Learning pages were introduced under the canonical paper directory.
            if source.relative_to(target / new).parts[0] == "interactive-guides":
                continue
            legacy = target / old / source.relative_to(target / new)
            if source.suffix != ".html":
                _copy_file(source, legacy)
                continue
            destination = quote(posixpath.relpath(
                source.relative_to(target).as_posix(),
                legacy.parent.relative_to(target).as_posix(),
            ), safe="/")
            _write_text(legacy, (
                '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8">\n'
                '<meta name="robots" content="noindex">\n'
                f'<link rel="canonical" href="{destination}">\n'
                f'<meta http-equiv="refresh" content="0;url={destination}">\n'
                '<title>GEOLab · 页面已迁移</title>\n<script>\n'
                f'const destination = {_javascript_string_literal(destination)};\n'
                'location.replace(destination + location.search + location.hash);\n'
                '</script></head><body><p>此页面已迁移。'
                f'<a href="{destination}">打开新地址</a></p></body></html>\n'
            ))


def build_viewer(output: Path) -> Path:
    output = output.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    _assert_replaceable_output(output)

    with tempfile.TemporaryDirectory(
        prefix="geo-citation-lab-viewer-", dir=output.parent
    ) as temporary:
        stage = Path(temporary) / "viewer"
        stage.mkdir()

        _build_root_index(stage)
        _build_paper_catalog(stage)
        _build_interactive_guides(stage)
        _copy_file(REPO_ROOT / ".nojekyll", stage / ".nojekyll")
        _copy_file(
            REPO_ROOT
            / "01-experiments"
            / "04-repet"
            / "final_report.html",
            stage
            / "01-experiments"
            / "04-repet"
            / "final_report.html",
        )
        _copy_file(
            REPO_ROOT
            / "03-datasets"
            / "reports"
            / "final"
            / "CN-GEO_多维数据分析报告.html",
            stage
            / "03-datasets"
            / "reports"
            / "final"
            / "CN-GEO_多维数据分析报告.html",
        )
        _copy_file(MANIFEST_PATH, stage / "geo-citation-lab-manifest.json")
        _copy_file(
            REPO_ROOT / "THIRD_PARTY_NOTICES.md",
            stage / "THIRD_PARTY_NOTICES.md",
        )
        for license_name in ("LICENSE", "LICENSE-CODE", "LICENSE-CONTENT"):
            _copy_file(REPO_ROOT / license_name, stage / license_name)
        _build_legacy_routes(stage)
        _write_viewer_checksums(stage)

        if output.exists():
            shutil.rmtree(output)
        stage.replace(output)

    return output


def _write_deterministic_zip(viewer: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as bundle:
        for source in sorted(path for path in viewer.rglob("*") if path.is_file()):
            relative = source.relative_to(viewer).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            bundle.writestr(info, source.read_bytes(), compresslevel=9)


def _assert_safe_package_dir(package_dir: Path) -> None:
    resolved = package_dir.resolve()
    if resolved == Path(resolved.anchor) or resolved == REPO_ROOT.resolve():
        raise ValueError(f"Unsafe release asset directory: {resolved}")
    if package_dir.is_symlink():
        raise ValueError(f"Release asset directory cannot be a symlink: {package_dir}")

    dist_root = (REPO_ROOT / "dist").resolve()
    for name in RELEASE_FILENAMES:
        target = package_dir / name
        if target.is_symlink():
            raise ValueError(f"Release asset target cannot be a symlink: {target}")
        if target.exists() and dist_root not in resolved.parents:
            raise ValueError(
                "Refusing to replace existing release assets outside the repository dist folder: "
                f"{target}"
            )


def package_viewer(viewer: Path, package_dir: Path) -> dict[str, Path]:
    package_dir = package_dir.expanduser()
    _assert_safe_package_dir(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)
    archive = package_dir / RELEASE_ASSET_NAME
    checksum = package_dir / f"{RELEASE_ASSET_NAME}.sha256"
    release_manifest = package_dir / "geo-citation-lab-manifest.json"

    _write_deterministic_zip(viewer, archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    _copy_file(MANIFEST_PATH, release_manifest)
    _copy_file(REPO_ROOT / "scripts" / "install.sh", package_dir / "install.sh")
    _copy_file(REPO_ROOT / "scripts" / "install.ps1", package_dir / "install.ps1")

    return {
        "archive": archive,
        "checksum": checksum,
        "manifest": release_manifest,
        "shell_installer": package_dir / "install.sh",
        "powershell_installer": package_dir / "install.ps1",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the lightweight GEO Citation Lab viewer."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Viewer output directory. Existing directories are replaced only under dist/.",
    )
    parser.add_argument(
        "--package",
        action="store_true",
        help="Create release assets after building the viewer.",
    )
    parser.add_argument(
        "--package-dir",
        type=Path,
        default=DEFAULT_PACKAGE_DIR,
        help="Release asset output directory.",
    )
    args = parser.parse_args()

    viewer = build_viewer(args.output)
    total_bytes = sum(path.stat().st_size for path in viewer.rglob("*") if path.is_file())
    print(f"viewer_path={viewer.resolve()}")
    print(f"viewer_uncompressed_bytes={total_bytes}")

    if args.package:
        assets = package_viewer(viewer, args.package_dir)
        for name, path in assets.items():
            print(f"{name}={path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
