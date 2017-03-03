from conan.packager import ConanMultiPackager
from conans.tools import os_info
import os, platform

username = os.getenv('CONAN_USERNAME', 'cpace6')
os.environ['CONAN_USERNAME'] = username
channel = os.getenv('CONAN_CHANNEL', 'stable')
os.environ['CONAN_CHANNEL'] = channel
log_run = os.getenv('CONAN_LOG_RUN_TO_FILE', '1')
os.environ['CONAN_LOG_RUN_TO_FILE'] = log_run

def get_builds_with_options(builder):
    builds = []
    for settings, options in builder.builds:
        builds.append([settings, {'benchmark:enable_lto':True}])
        builds.append([settings, {'benchmark:enable_lto':False}])
    return builds
    

if __name__ == "__main__":
    builder = ConanMultiPackager(
        gcc_versions=['5.4', '6.2'],
        #apple_clang_versions=['8.0'],
        visual_versions=['14'],
        archs=['x86_64']     #, 'x86'],
        use_docker=False,
        upload=False,
        username=username,
        channel=channel,
        reference='Qt/5.7.0',
    )
    builder.add_common_builds()    # TODO: what does pure_c=False argument do?
    builder.builds = get_builds_with_options(builder)
    builder.run()
