#!/usr/bin/python
import sys
import apt

pkg_name = "relsandbox"

cache = apt.cache.Cache(apt.progress.text.OpProgress())
pkg = cache.get(pkg_name, None)

if not pkg:
    print pkg_name + " is not available in the apt repositories configured on this machine"
    sys.exit(1)

install_versions = []

if pkg.is_installed:
    print pkg_name + " already installed, upgrading"

    install = False
    for version in reversed(pkg.versions):
        if not install:
            if version == pkg.installed:
                install = True
            continue

        install_versions.append(version)
else:
    print pkg_name + " not installed, installing"
    install_versions.append(pkg.candidate)


for version in install_versions:
    print "Installing version " + str(version) + " of " + pkg_name
    pkg.candidate = version

    pkg.mark_install()
    try:
        cache.commit()
    except Exception, arg:
        print "Package installation failed [{err}]".format(err=str(arg))
        sys.exit(1)
