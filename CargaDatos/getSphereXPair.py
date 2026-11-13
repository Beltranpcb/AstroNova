"""
Obtiene dos imágenes reales de SPHEREx (IRSA) de la misma región del cielo,
descarga un cutout FITS de cada una y extrae sus metadatos.

Salida (carpeta ./spherex_data):
  - obs1.fits, obs2.fits        -> los dos archivos FITS
  - metadata.json / metadata.csv -> fechas, coordenadas, identificadores, cabeceras

Uso:
  python get_spherex_pair.py                      # región por defecto
  python get_spherex_pair.py --ra 276.0 --dec 65.0 --size 0.1
"""
import argparse
import csv
import json
from pathlib import Path

import pyvo
import requests
from astropy.io import fits
from astropy.time import Time

TAP_URL = "https://irsa.ipac.caltech.edu/TAP"
OUT = Path("spherex_data")


def find_observations(ra, dec, radius_deg=0.05, limit=200):
    """Observaciones SPHEREx (tabla spherex.obscore) que cubren el punto."""
    tap = pyvo.dal.TAPService(TAP_URL)
    adql = f"""
        SELECT TOP {limit} *
        FROM spherex.obscore
        WHERE CONTAINS(POINT('ICRS', {ra}, {dec}), s_region) = 1
          AND dataproduct_type = 'image'
        ORDER BY t_min
    """
    return tap.run_async(adql).to_table()


def pick_pair(tbl, band_tol_um=0.05):
    """Dos observaciones con banda parecida y la mayor separación temporal.
    Si no hay ninguna pareja con banda parecida, usa la mayor separación."""
    rows = list(tbl)
    best, best_dt = None, -1
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            same_band = abs(float(a["em_min"]) - float(b["em_min"])) * 1e6 < band_tol_um
            dt = abs(float(b["t_min"]) - float(a["t_min"]))
            score = dt + (1e6 if same_band else 0)  # prioriza misma banda
            if score > best_dt:
                best, best_dt = (a, b), score
    return best


def download_cutout(access_url, ra, dec, size_deg, dest):
    r = requests.get(
        access_url, params={"center": f"{ra},{dec}", "size": size_deg},
        timeout=300,
    )
    r.raise_for_status()
    dest.write_bytes(r.content)


def extract_metadata(row, fits_path, label):
    meta = {"label": label, "file": fits_path.name}
    for key in ("obs_id", "obs_publisher_did", "access_url", "s_ra", "s_dec",
                "t_min", "t_max", "em_min", "em_max", "instrument_name",
                "obs_collection", "calib_level"):
        if key in row.colnames:
            val = row[key]
            meta[key] = val.item() if hasattr(val, "item") else str(val)
    if "t_min" in meta:
        meta["date_obs_utc"] = Time(float(meta["t_min"]), format="mjd").isot
    with fits.open(fits_path) as hdul:
        meta["fits_extensions"] = [h.name for h in hdul]
        hdr0 = hdul[0].header
        meta["primary_header"] = {k: str(hdr0[k]) for k in hdr0 if k and k != "COMMENT"}
    return meta


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ra", type=float, default=276.0)
    p.add_argument("--dec", type=float, default=65.0)
    p.add_argument("--size", type=float, default=0.1, help="tamaño del cutout (grados)")
    args = p.parse_args()

    OUT.mkdir(exist_ok=True)
    tbl = find_observations(args.ra, args.dec)
    print(f"{len(tbl)} observaciones cubren RA={args.ra}, Dec={args.dec}")
    if len(tbl) < 2:
        raise SystemExit("Menos de 2 observaciones: prueba otra región.")

    a, b = pick_pair(tbl)
    metas = []
    for label, row in (("obs1", a), ("obs2", b)):
        dest = OUT / f"{label}.fits"
        download_cutout(str(row["access_url"]), args.ra, args.dec, args.size, dest)
        metas.append(extract_metadata(row, dest, label))
        print(f"{label}: {dest}  fecha={metas[-1].get('date_obs_utc')}")

    (OUT / "metadata.json").write_text(json.dumps(metas, indent=2, default=str))
    flat = [{k: v for k, v in m.items() if k not in ("primary_header", "fits_extensions")}
            for m in metas]
    with open(OUT / "metadata.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sorted({k for m in flat for k in m}))
        w.writeheader()
        w.writerows(flat)
    print("Listo. Revisa ./spherex_data/")


if __name__ == "__main__":
    main()