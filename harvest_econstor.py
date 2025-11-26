# harvest_econstor.py
import argparse
import json
import time
import re
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional

OAI_BASE = "https://www.econstor.eu/oai/request"
NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/"
}

# --- Heurísticas y utilidades ---
_re_ascii_term = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 \-–/&%\.]*[A-Za-z0-9%]$")
def is_english_keyword(s: str, multiword_only: bool) -> bool:
    if not s:
        return False
    s = s.strip()
    if len(s) < 3:
        return False
    if multiword_only and (" " not in s):
        return False
    if any(ch in s for ch in "äöüÄÖÜßñÑéáíóúÁÉÍÓÚçÇ"):
        return False
    return bool(_re_ascii_term.match(s))

def dedup_case_insensitive(items: List[str]) -> List[str]:
    seen, out = set(), []
    for x in items:
        k = x.lower().strip()
        if k not in seen:
            seen.add(k); out.append(x.strip())
    return out

def keyword_boundary_pattern(term: str) -> re.Pattern:
    t = re.escape(term.strip()).replace(r"\ ", r"\s+")
    return re.compile(rf"(?<!\w){t}(?!\w)", flags=re.IGNORECASE)

def filter_keywords_present_in_text(keywords: List[str], text: str) -> List[str]:
    present = []
    for kw in keywords:
        if keyword_boundary_pattern(kw).search(text):
            present.append(kw.strip())
    return dedup_case_insensitive(present)

def pick_english_text(nodes: List[ET.Element]) -> Optional[str]:
    """Elige el texto en inglés si hay idioma, si no, devuelve el más largo razonable."""
    best = None
    for n in nodes:
        t = (n.text or "").strip()
        if not t: 
            continue
        lang = (n.attrib.get("{http://www.w3.org/XML/1998/namespace}lang","") or "").lower()
        if lang in ("en","eng","en-us","en-gb") and len(t) >= 40:
            return t
        if len(t) >= 40:  # fallback: el más largo
            best = t if best is None or len(t) > len(best) else best
    return best

# --- OAI-PMH ---
def list_records(metadata_prefix="oai_dc", from_date=None, until_date=None, set_spec=None, sleep=0.4):
    """Generador de registros OAI con manejo de resumptionToken."""
    params = {"verb": "ListRecords", "metadataPrefix": metadata_prefix}
    if from_date: params["from"] = from_date
    if until_date: params["until"] = until_date
    if set_spec: params["set"] = set_spec

    token = None
    while True:
        if token:
            r = requests.get(OAI_BASE, params={"verb":"ListRecords","resumptionToken":token}, timeout=40)
        else:
            r = requests.get(OAI_BASE, params=params, timeout=40)
        r.raise_for_status()
        root = ET.fromstring(r.text)

        for rec in root.findall(".//oai:record", NS):
            yield rec

        rt = root.find(".//oai:resumptionToken", NS)
        token = (rt.text or "").strip() if rt is not None else None
        if not token:
            break
        time.sleep(sleep)

# --- Extracción de campos Dublin Core ---
def get_dc_list(meta, tag) -> List[ET.Element]:
    return meta.findall(f".//dc:{tag}", NS) + meta.findall(f".//dcterms:{tag}", NS)

def extract_fields(rec) -> Dict:
    header = rec.find("./oai:header", NS)
    if header is None or header.find("./oai:identifier", NS) is None:
        return {}
    identifier = (header.find("./oai:identifier", NS).text or "").strip()

    meta = rec.find("./oai:metadata", NS)
    if meta is None:
        return {"id": identifier}

    titles = get_dc_list(meta, "title")
    descs = get_dc_list(meta, "description") + get_dc_list(meta, "abstract")
    langs = get_dc_list(meta, "language")
    subs  = get_dc_list(meta, "subject")

    # idioma: acepta si algún dc:language es en/en-gb/eng o si el texto elegido lo está
    langs_txt = [ (n.text or "").strip().lower() for n in langs if (n.text or "").strip() ]
    lang_ok = any(l in ("en","eng","en-us","en-gb") for l in langs_txt) or not langs_txt

    title = pick_english_text(titles) or ((titles[0].text or "").strip() if titles else None)
    abstract = pick_english_text(descs)
    keywords = dedup_case_insensitive([(n.text or "").strip() for n in subs if (n.text or "").strip()])

    return {
        "id": identifier,
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "lang_ok": lang_ok
    }

# --- Pipeline principal ---
def harvest_econstor(out_path: str,
                     max_records: int = 8000,
                     min_text_chars: int = 150,
                     min_kws_present: int = 1,
                     multiword_only: bool = True,
                     require_kw_in_text: bool = True,
                     sleep: float = 0.4):
    out = Path(out_path)
    out.unlink(missing_ok=True)

    kept = 0
    stats = {"no_title":0,"lang_filtered":0,"short_text":0,"no_keywords":0,"no_kw_in_text":0,"min_kws":0}

    with out.open("w", encoding="utf-8") as f:
        for rec in list_records(metadata_prefix="oai_dc", sleep=sleep):
            fields = extract_fields(rec)
            title = fields.get("title")
            if not title:
                stats["no_title"] += 1
                continue
            if not fields.get("lang_ok", True):
                stats["lang_filtered"] += 1
                continue

            abstract = fields.get("abstract")
            text = title if not abstract else f"{title} — {abstract}"
            if len(text) < min_text_chars:
                stats["short_text"] += 1
                continue

            # keywords limpias (en inglés y multi-palabra si se exige)
            kws = [k for k in fields.get("keywords", []) if is_english_keyword(k, multiword_only)]
            kws = dedup_case_insensitive(kws)
            if not kws:
                stats["no_keywords"] += 1
                continue

            if require_kw_in_text:
                kws = filter_keywords_present_in_text(kws, text)
                if not kws:
                    stats["no_kw_in_text"] += 1
                    continue

            if len(kws) < min_kws_present:
                stats["min_kws"] += 1
                continue

            doc = {"doc_id": fields["id"], "text": text, "keywords": sorted(kws, key=str.lower)}
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
            kept += 1
            if kept >= max_records:
                break

    return kept, stats

def main():
    ap = argparse.ArgumentParser("EconStor OAI-PMH harvester → JSONL (text + keywords)")
    ap.add_argument("--out", default="econstor_finance_en.jsonl")
    ap.add_argument("--max-records", type=int, default=8000)
    ap.add_argument("--min-text-chars", type=int, default=150)
    ap.add_argument("--min-kws", type=int, default=1)
    ap.add_argument("--multiword-only", action="store_true")
    ap.add_argument("--no-require-kw-in-text", action="store_true", help="No exigir que las keywords aparezcan en el texto")
    ap.add_argument("--sleep", type=float, default=0.4, help="Delay entre requests (educado con el servidor)")
    args = ap.parse_args()

    kept, stats = harvest_econstor(
        out_path=args.out,
        max_records=args.max_records,
        min_text_chars=args.min_text_chars,
        min_kws_present=args.min_kws,
        multiword_only=args.multiword_only,
        require_kw_in_text=not args.no_require_kw_in_text,
        sleep=args.sleep,
    )

    print("\nResumen de descartes:")
    for k, v in stats.items():
        print(f"  - {k}: {v}")
    print(f"\n✅ Guardado {kept} documentos en {args.out}")

if __name__ == "__main__":
    main()