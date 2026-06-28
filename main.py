#!/bin/env python3
import os
import shutil
import subprocess


class Builder:
    def __init__(self):
        self.apt_packages = ['libasound2-dev', 'libavcodec-dev', 'libcap-dev', 'libdrm-dev', 'libglib2.0-dev',
                             'libgtk-4-dev', 'libgudev-1.0-dev', 'libopenxr-dev', 'libportal-dev', 'libsqlite3-dev',
                             'libwebkitgtk-6.0-dev']

    def execute(self, command: list) -> int:
        ret = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return ret.returncode

    def launch(self):
        for f in [self.install_packages]:
            try:
                f()
            except Exception as e:
                print(f"\033[31m [Failed] {f.__name__}: {e} \033[0m")

    def install_packages(self):
        assert shutil.which("apt"), "apt is missing."
        if os.getuid() == 0:
            self.execute(['apt', 'install', *self.apt_packages])
        else:
            assert shutil.which("sudo"), "sudo missing."
            self.execute(["sudo", 'apt', 'install', *self.apt_packages])


if __name__ == "__main__":
    builder = Builder()
    builder.launch()
