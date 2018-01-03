from conan.packager import ConanMultiPackager
import copy

def main():
    builder = ConanMultiPackager(username="osechet", archs = ["x86_64"])
    builder.add_common_builds(pure_c=False)
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["compiler"] == "Visual Studio":
            if settings["compiler.runtime"] == "MT" or settings["compiler.runtime"] == "MTd":
                # Ignore MT runtime
                continue

        new_options = copy.copy(options)
        new_options["Qt:xmlpatterns"] = True

        filtered_builds.append([settings, new_options, env_vars, build_requires])
        filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()

if __name__ == "__main__":
    main()
