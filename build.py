
from conan.packager import ConanMultiPackager

def main():
    """
    Main function.
    """
    builder = ConanMultiPackager(username="osechet", channel="stable")
    builder.add_common_builds()
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["arch"] != "x86_64":
            continue

        filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()

if __name__ == "__main__":
    main()
