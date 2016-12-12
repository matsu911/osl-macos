# -*- mode: python -*-

def options(ctx):
    ctx.load('compiler_cxx')

def configure(ctx):
    ctx.load('compiler_cxx')
    ctx.check_cfg(package='python', args='--libs --cflags', uselib_store='PYTHON')
    ctx.env.append_value('CXXFLAGS', ['-std=c++14', '-stdlib=libc++', '-O3'])

def build(ctx):
    ctx.shlib(source=ctx.path.ant_glob('core/osl/**/*.cc'),
              includes=['core'],
              lib=['boost_filesystem',
                   'boost_serialization',
                   'boost_system',
                   'boost_iostreams'],
              defines=['OSL_HOME="."'],
              target='osl-core')
    ctx.shlib(source=ctx.path.ant_glob(['std/osl/*.cc',
                                        'std/osl/hash/**/*.cc',
                                        'std/osl/checkmate/**/*.cc',
                                        'std/osl/effect_util/**/*.cc']),
              includes=['core', 'std'],
              use=['osl-core'],
              lib=['iconv',
                   'boost_filesystem',
                   'boost_system',
                   'boost_date_time'],
              target='osl-std')
    ctx.shlib(source=ctx.path.ant_glob('full/osl/misc/**/*.cc'),
              includes=['core', 'std', 'full'],
              use=['osl-core'],
              target='osl-full')
    env = ctx.env.derive()
    env.update({'cxxshlib_PATTERN': "%s.so"})
    ctx.shlib(source=ctx.path.ant_glob('python/**/*.cc'),
              env=env,
              includes=['core', 'std', 'full'],
              use=['osl-core', 'PYTHON'],
              lib=['boost_python'],
              target='hello_ext')
    ctx.program(source='sample/checkmate/dfpnstat.cc',
                use=['osl-core', 'osl-std', 'osl-full'],
                includes=['core', 'std', 'full'],
                target='dfpnstat')
