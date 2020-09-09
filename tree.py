import os
import sys


class Tree():
    mode_descriptions = {
        'df': 'Directory First',
        'do': 'Directory Only',
        'ff': 'File First',
        'od': 'Ordered'
    }

    def __init__(self, path, indent=4, mode='ff', sparse=True, dtail='/'):
        self.sparse = sparse
        self.dtail = dtail
        self.space = ' ' * indent
        self.line = '─' * indent

        self.traverses = {
            'df': self.df,
            'do': self.do,
            'ff': self.ff,
            'od': self.od
        }

        self.chmod(mode)
        self.generate(path)

    def write(self, filename):
        with open(filename, 'w+', encoding='utf-8') as fd:
            fd.write('mode: %s\n' % self.mode_descriptions[self.mode])
            fd.write('\n')
            fd.write(self.tree)

    def print(self):
        print(self.tree)

    def chmod(self, mode):
        assert mode in self.traverses
        self.traverse = self.traverses[mode]
        self.mode = mode

    def generate(self, path):
        path = os.path.abspath(path)
        assert os.path.isdir(path)
        self.tree = path + '\n'
        self.traverse(path, '')

    def get_dirs_files(self, dirpath):
        dirs, files = [], []
        for leaf in os.listdir(dirpath):
            path = os.path.join(dirpath, leaf)
            if os.path.isfile(path):
                files.append(leaf)
            else:
                dirs.append((leaf, path))

        return dirs, files

    def add_dirs(self, dirs, prefix, fprefix, dprefix, recursive):
        for dirname, path in dirs[:-1]:
            self.tree += dprefix + dirname + self.dtail + '\n'
            recursive(path, fprefix)

        dirname, path = dirs[-1]
        fprefix = prefix + ' ' + self.space
        dprefix = prefix + '└' + self.line
        self.tree += dprefix + dirname + self.dtail + '\n'
        recursive(path, fprefix)

    def add_files(self, files, fprefix):
        for file in files:
            self.tree += fprefix + file + '\n'
        if self.sparse and files:
            self.tree += fprefix.rstrip() + '\n'

    def df(self, dirpath, prefix):
        dirs, files = self.get_dirs_files(dirpath)
        if dirs:
            fprefix = prefix + '│' + self.space
            dprefix = prefix + '├' + self.line
            self.add_dirs(dirs, prefix, fprefix, dprefix, self.df)
            self.add_files(files, prefix + ' ' + self.space)

        else:
            self.add_files(files, prefix + self.space)

    def do(self, dirpath, prefix):
        dirs = []
        for leaf in os.listdir(dirpath):
            path = os.path.join(dirpath, leaf)
            if os.path.isdir(path):
                dirs.append((leaf, path))
        if dirs:
            fprefix = prefix + '│' + self.space
            dprefix = prefix + '├' + self.line
            self.add_dirs(dirs, prefix, fprefix, dprefix, self.do)

    def ff(self, dirpath, prefix):
        dirs, files = self.get_dirs_files(dirpath)
        if dirs:
            fprefix = prefix + '│' + self.space
            dprefix = prefix + '├' + self.line
            self.add_files(files, fprefix)
            self.add_dirs(dirs, prefix, fprefix, dprefix, self.ff)
        else:
            self.add_files(files, prefix + self.space)

    def od(self, dirpath, prefix):
        leaves = sorted(os.listdir(dirpath))
        if not leaves:
            return
        for leaf in leaves[:-1]:
            path = os.path.join(dirpath, leaf)
            if os.path.isfile(path):
                fprefix = prefix + '│' + self.space
                dprefix = prefix + '├' + self.line
                self.tree += dprefix + leaf + '\n'
            if os.path.isdir(path):
                fprefix = prefix + '│' + self.space
                dprefix = prefix + '├' + self.line
                self.tree += dprefix + leaf + self.dtail + '\n'
                self.od(path, fprefix)

        leaf = leaves[-1]
        path = os.path.join(dirpath, leaf)
        fprefix = prefix + ' ' + self.space
        dprefix = prefix + '└' + self.line
        if os.path.isfile(path):
            self.tree += dprefix + leaf + '\n'
        if os.path.isdir(path):
            self.tree += dprefix + leaf + self.dtail + '\n'
            self.od(path, fprefix)


if __name__ == '__main__':
    args = sys.argv[1:]
    narg = len(args)
    opts = {}

    tree = Tree('.', indent=4, mode='ff', sparse=False, dtail='/')
    tree.write('test.tr')
    # tree.print()
    # tree = Tree(args[0], **opts)
    # tree.print()

