from conan.packager import ConanMultiPackager
import copy

def main():
    """
    Main function.
    """

    builder = ConanMultiPackager(username="osechet", channel="stable")
    builder.add_common_builds()
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["compiler"] == "Visual Studio":
            if settings["compiler.runtime"] == "MT" or settings["compiler.runtime"] == "MTd":
                # Ignore MT runtime
                continue
        if settings["arch"] != "x86_64":
            continue

        new_options = copy.copy(options)
        new_options["Qt:xmlpatterns"] = True

        filtered_builds.append([settings, new_options, env_vars, build_requires])
        filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()

if __name__ == "__main__":
    main()
