"""Build a portable public source archive and static hosting output."""
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'docs/close-gtm-decision-lab.zip'

def package():
    allowed_dirs={'src','models','tests','analysis','docs','.github'}
    allowed_root={'README.md','LICENSE','Makefile','requirements.txt','dbt_project.yml','profiles.yml','.gitignore'}
    files=[p for p in ROOT.rglob('*') if p.is_file() and (
        (p.relative_to(ROOT).parts[0] in allowed_dirs and '__pycache__' not in p.parts)
        or p.relative_to(ROOT).as_posix() in allowed_root)
        and p.suffix not in {'.zip','.pyc'}]
    with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            info=zipfile.ZipInfo('close-gtm-decision-lab/'+p.relative_to(ROOT).as_posix(),date_time=(2026,11,20,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,p.read_bytes())
    out=ROOT/'dist'; out.mkdir(exist_ok=True)
    for p in (ROOT/'docs').iterdir():
        if p.is_file(): shutil.copy2(p,out/p.name)
    print(f'Packaged {len(files)} source files; archive {ARCHIVE.stat().st_size:,} bytes.')

if __name__=='__main__': package()
