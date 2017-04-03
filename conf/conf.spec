[develop]
python_ver = string(default='3.4')
venv_cmd = string(default='pyvenv-3.4')
build_dir = string(default='build')
venv_dir = string(default='build/venv')
path_dir = string(default='build/venv/bin')
dist_dir = string(default='dist')
print_pre = string(default='**** FLUIDAsserts: ')
print_pos = string(default='.')

[logging]
version = integer(min=1, max=1, default=1)
