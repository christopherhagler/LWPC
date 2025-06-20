#!/usr/bin/env python
import sys
from pathlib import Path


def create_input_files():
    TEMPLATE = """\
    file-mds   ../LWPCv21/output/
    file-lwf   ../LWPCv21/output/
    file-grd   ../LWPCv21/output/
    case-id    Tuskegee 5-Element Receiving Array
    tx         path
    tx-data    OMEGA-D
    ionosphere homogeneous table {profile}
    range-max  1000
    receivers  32.469 -85.718   32.469 -85.668
    +receivers 32.469 -85.609   32.469 -85.566   32.469 -85.587
    mc-options full-wave 0 true
    lwflds
    print-mds  0
    print-swg  2
    print-wf   2
    print-lwf  2
    print-mc   1
    start
    quit
    """

    PRF_DIR = Path(__file__).resolve().parent / 'LWPCv21/Profile/ionosphere'
    OUT_DIR = Path(__file__).resolve().parent / 'LWPCv21/non_uniform'

    if not PRF_DIR.exists():
        print(f"❌ PRF directory {PRF_DIR!r} does not exist.", file=sys.stderr)
        sys.exit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for prf_path in PRF_DIR.glob('*.prf'):
        inf_text = TEMPLATE.format(profile=prf_path)

        inf_path = OUT_DIR / f"{prf_path.stem}.inf"
        inf_path.write_text(inf_text)
        print(f"✔️  Wrote {inf_path}")


def main():
    create_input_files()


if __name__ == "__main__":
    main()
