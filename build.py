from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(username="osechet", channel="testing")
    builder.add_common_builds()
    filtered_builds = []
    for settings, options in builder.builds:
        if settings["arch"] == "x86_64":
             filtered_builds.append([settings, options])
    builder.builds = filtered_builds
    builder.run()
