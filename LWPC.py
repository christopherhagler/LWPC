#!/usr/bin/env python
import shutil
import subprocess
import sys
from pathlib import Path

PRF_DIR = Path(__file__).resolve().parent / 'LWPCv21/Profile/ionosphere'
INP_DIR = Path(__file__).resolve().parent / 'LWPCv21/non_uniform'


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

    if not PRF_DIR.exists():
        print(f"❌ PRF directory {PRF_DIR!r} does not exist.", file=sys.stderr)
        sys.exit(1)
    INP_DIR.mkdir(parents=True, exist_ok=True)

    for prf_path in PRF_DIR.glob('*.prf'):
        prf_file = f"../LWPCv21/Profile/ionosphere/{prf_path.name}"
        inf_text = TEMPLATE.format(profile=prf_file)

        inf_path = INP_DIR / f"{prf_path.stem}.inp"
        inf_path.write_text(inf_text)
        print(f"✔️  Wrote {inf_path}")


def run_lwpc_and_archive_logs():
    script_dir = Path(__file__).resolve().parent
    lwpc_bin = script_dir.parent / "LWPC" / "build" / "lwpc.bin"
    lwpcv21_dir = script_dir.parent / "LWPC" / "LWPCv21"
    log_dir = lwpcv21_dir / "log"
    build_dir = script_dir.parent / "LWPC" / "build"

    # Sanity checks
    if not INP_DIR.exists():
        sys.exit(f"❌ Input directory not found: {INP_DIR}")
    if not lwpc_bin.exists():
        sys.exit(f"❌ LWPC executable not found: {lwpc_bin}")
    if not lwpcv21_dir.exists():
        sys.exit(f"❌ LWPCv21 directory not found: {lwpcv21_dir}")

    # Run LWPC for each .inp file
    for inp_path in sorted(INP_DIR.glob("*.inp")):
        print(f"→ Running LWPC on {inp_path.name}")
        subprocess.run(
            [str(lwpc_bin),
             str("../LWPCv21/non_uniform/" + inp_path.name.split('.')[0])],
            cwd=str(build_dir),
            check=True
        )

    # Archive .log files
    log_dir.mkdir(parents=True, exist_ok=True)
    for log_file in INP_DIR.glob("*.log"):
        print(f"Moving {log_file.name} → {log_dir.name}/")
        shutil.move(str(log_file), str(log_dir / log_file.name))

    print(f"✅ All .log files moved into: {log_dir}")


def main():
    create_input_files()
    run_lwpc_and_archive_logs()


if __name__ == "__main__":
    main()
