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

    def execute(self, command: list) -> int:
        ret = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return ret.returncode

    def launch(self):
        for f in [self.install_packages, self.check_source_code, self.build_wolfssl, self.build_art, ]:
            try:
                f()
            except Exception as e:
                print(f"\033[31m [Failed] {f.__name__}: {e} \033[0m")
                break

    def install_packages(self):
        assert shutil.which("apt"), "apt is missing."
        if os.getuid() == 0:
            self.execute(['apt', 'install', *self.apt_packages])
        else:
            assert shutil.which("pkexec"), "pkexec missing."
            self.execute(["pkexec", 'apt', 'install', *self.apt_packages])

    def check_source_code(self):
        for i in self.source_dirs:
            assert os.path.exists(i), "%s is not exist." % i

    def build_wolfssl(self):
        assert which("autoreconf"), "autoreconf missing"
        pwd = os.getcwd()
        os.chdir('wolfssl')
        self.execute(['autoreconf', '-i'])
        self.execute(["./configure", "--enable-shared", "--disable-opensslall", "--disable-opensslextra", "--enable-aescbc-length-checks", "--enable-curve25519", "--enable-ed25519", "--enable-ed25519-stream", "--enable-oldtls","--enable-base64encode","--enable-tlsx","--enable-scrypt", "--disable-examples", "--enable-crl", "--enable-jni", "--enable-sessioncerts"])
        self.execute(['make'])
        self.execute(['pkexec', 'make', 'install'])
        os.chdir(pwd)
    def build_meson_projects(self):
        for i in ['atl', "bionic", 'libopensles']:
            self.build_meson(i)
    def build_meson(self, project_name:str):
        pwd = os.getcwd()
        os.chdir(project_name)
        self.execute(["meson", "setup", "builddir"])
        os.chdir("bionic/builddir")
        self.execute(['meson', 'compile'])
        self.execute(['pkexec','meson', 'install'])
        os.chdir(pwd)

    def build_art(self):
        pwd = os.getcwd()
        os.chdir('art')
        self.execute(['make', "____LIBDIR=lib"])
        self.execute(["pkexec",'make', "____LIBDIR=lib", "install"])
        os.chdir(pwd)

if __name__ == "__main__":
    builder = Builder()
    builder.launch()
