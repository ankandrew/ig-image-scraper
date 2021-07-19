from pathlib import Path
from shutil import copyfile


class Logger:
    def __init__(self, out_file: str):
        self.path = Path(out_file)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.backup_path = self.path.parent / (self.path.stem + '-backup' + self.path.suffix)

    def log(self, img: set):
        # Before writing, backup if possible
        if self.path.exists():
            copyfile(self.path, self.backup_path)
        with open(self.path, 'w') as f_out:
            for i in img:
                f_out.write(f'{i}\n')
