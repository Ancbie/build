#!/bin/env python3
import os
import shutil
import subprocess
from shutil import which


class Builder:
    def __init__(self):
        self.apt_packages = ['libasound2-dev', 'libavcodec-dev', 'libcap-dev', 'libdrm-dev', 'libglib2.0-dev',
                             'libgtk-4-dev', 'libgudev-1.0-dev', 'libopenxr-dev', 'libportal-dev', 'libsqlite3-dev',
                             'libwebkitgtk-6.0-dev', "make", 'meson']
        self.source_dirs = ["wolfssl", 'atl', 'art', "bionic", "libopensles", "atl-gui"]

    def execute(self, command: list, working_dir:str|None=None, shell:bool=False) -> int:
        if command[0] == 'sudo':
            pwd = os.getcwd()
            if working_dir:
                os.chdir(working_dir)
            ret = os.system(f"pkexec {command[1]} "+" ".join(command[2:]))
            os.chdir(pwd)
            return ret
        ret = subprocess.Popen(command, cwd=working_dir, stderr=subprocess.STDOUT, shell=shell)
        ret.wait()
        assert ret.returncode == 0, f'Run {command} failed.'
        return ret.returncode

    def launch(self):
        for f in [self.install_packages, self.check_source_code, self.build_wolfssl, self.build_art, self.build_meson_projects]:
            try:
                print(f"\033[33m[Running] {f.__name__}\033[0m")
                f()
            except Exception as e:
                print(f"\033[31m[Failed] {f.__name__}: {e}\033[0m")
                break

    def install_packages(self):
        assert shutil.which("apt"), "apt is missing."
        if os.getuid() == 0:
            self.execute(['apt', 'install', *self.apt_packages])
        else:
            self.execute(["sudo", 'apt', 'install', *self.apt_packages])

    def check_source_code(self):
        for i in self.source_dirs:
            assert os.path.exists(i), "%s is not exist." % i

    def build_wolfssl(self):
        assert which("autoreconf"), "autoreconf missing"
        working_path = os.path.realpath("wolfssl")
        self.execute(['autoreconf', '-i'], working_dir=working_path)
        self.execute(["sh","./configure", "--enable-shared", "--disable-opensslall", "--disable-opensslextra", "--enable-aescbc-length-checks", "--enable-curve25519", "--enable-ed25519", "--enable-ed25519-stream", "--enable-oldtls","--enable-base64encode","--enable-tlsx","--enable-scrypt", "--disable-examples", "--enable-crl", "--enable-jni", "--enable-sessioncerts"],working_dir=working_path)
        self.execute(['make'], working_dir=working_path)
        self.execute(['sudo', 'make', 'install'], working_dir=working_path)
    def build_meson_projects(self):
        for i in ['atl', "bionic", 'libopensles']:
            self.build_meson(i)
    def build_meson(self, project_name:str):
        working_path = os.path.realpath(project_name)
        self.execute(["meson", "setup", "builddir"], working_dir=working_path)
        working_path = os.path.realpath(os.path.join(working_path, 'builddir'))
        self.execute(['meson', 'compile'], working_dir=working_path)
        self.execute(['sudo','meson', 'install'], working_dir=working_path)

    def build_art(self):
        working_path = os.path.realpath('art')
        self.execute(['make', "____LIBDIR=lib"], working_dir=working_path)
        self.execute(["sudo",'make', "____LIBDIR=lib", "install"], working_dir=working_path)

if __name__ == "__main__":
    builder = Builder()
    builder.launch()
