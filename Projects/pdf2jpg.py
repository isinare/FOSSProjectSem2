"""PDF to images conversion helpers (renamed to pdf2jpg).

Provides processing helpers and route registration for converting uploaded
PDF files into PNG images and returning them as a ZIP archive.
"""
from __future__ import annotations

import io
import os
import zipfile
import tempfile
from typing import List

from flask import (
    request,
    redirect,
    url_for,
    flash,
    send_file,
    send_from_directory,
)
from werkzeug.utils import secure_filename

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover - dependency errors
    fitz = None  # type: ignore


class PDFConversionError(Exception):
    """Raised when a PDF cannot be converted to images."""


def _ensure_fitz_available() -> None:
    if fitz is None:
        raise PDFConversionError("PyMuPDF (fitz) is not installed")


def _pdf_bytes_to_png_paths(pdf_bytes: bytes, out_dir: str) -> List[str]:
    _ensure_fitz_available()
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise PDFConversionError(f"Unable to open PDF: {exc}") from exc

    paths: List[str] = []
    for i in range(len(doc)):
        page = doc[i]
        try:
            pix = page.get_pixmap(alpha=False)
        except Exception as exc:
            doc.close()
            raise PDFConversionError(f"Failed rendering page {i}: {exc}") from exc

        filename = f"page_{i+1:03d}.png"
        path = os.path.join(out_dir, filename)
        try:
            pix.save(path)
        except Exception as exc:
            doc.close()
            raise PDFConversionError(f"Failed saving image {filename}: {exc}") from exc

        paths.append(path)

    doc.close()
    return paths


def _make_zip_from_paths(paths: List[str]) -> io.BytesIO:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in paths:
            zf.write(p, arcname=os.path.basename(p))
    buf.seek(0)
    return buf


def process_pdf_and_get_zip(pdf_bytes: bytes, output_name: str | None = None) -> io.BytesIO:
    _ensure_fitz_available()
    with tempfile.TemporaryDirectory() as td:
        paths = _pdf_bytes_to_png_paths(pdf_bytes, td)
        return _make_zip_from_paths(paths)


def register_pdf_routes(app) -> None:
    @app.route("/pdf2images", methods=["GET", "POST"])
    def pdf2images():
        if request.method == "GET":
            # serve static HTML form (no Jinja)
            return send_from_directory("static/html", "pdf2images.html")

        uploaded = request.files.get("pdf_file")
        if not uploaded or uploaded.filename == "":
            flash("No file uploaded", "error")
            return redirect(url_for("pdf2images"))

        filename = secure_filename(uploaded.filename)
        if not filename.lower().endswith(".pdf"):
            flash("Please upload a PDF file (.pdf)", "error")
            return redirect(url_for("pdf2images"))

        try:
            pdf_bytes = uploaded.read()
            zip_buf = process_pdf_and_get_zip(pdf_bytes, output_name=filename)
        except PDFConversionError as exc:
            flash(f"Conversion failed: {exc}", "error")
            return redirect(url_for("pdf2images"))
        except Exception as exc:
            flash(f"Unexpected error: {exc}", "error")
            return redirect(url_for("pdf2images"))

        download_name = f"{os.path.splitext(filename)[0]}_images.zip"
        zip_buf.seek(0)
        return send_file(
            zip_buf,
            mimetype="application/zip",
            as_attachment=True,
            download_name=download_name,
        )


__all__ = [
    "process_pdf_and_get_zip",
    "PDFConversionError",
    "register_pdf_routes",
]
