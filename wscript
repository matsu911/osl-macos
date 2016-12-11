# -*- mode: python -*-

def options(ctx):
    ctx.load('compiler_cxx')

def configure(ctx):
    ctx.load('compiler_cxx')

def build(ctx):
    ctx.shlib(source=ctx.path.ant_glob('core/osl/**/*.cc'),
              cxxflags=['-std=c++14', '-stdlib=libc++'],
              includes=['core'],
              lib=['boost_filesystem',
                   'boost_serialization',
                   'boost_system',
                   'boost_iostreams'],
              defines=['OSL_HOME="."'],
              target='osl-core')
    ctx.shlib(source=ctx.path.ant_glob('std/osl/**/*.cc'),
              cxxflags=['-std=c++14', '-stdlib=libc++'],
              includes=['core', 'std'],
              use=['osl-core'],
              lib=['iconv',
                   'boost_filesystem',
                   'boost_system',
                   'boost_date_time'],
              target='osl-std')
    ctx.shlib(source=ctx.path.ant_glob('full/osl/misc/**/*.cc'),
              cxxflags=['-std=c++14', '-stdlib=libc++'],
              includes=['core', 'std', 'full'],
              use=['osl-core'],
              target='osl-full')
    ctx.program(source='sample/checkmate/dfpnstat.cc',
                use=['osl-core', 'osl-std', 'osl-full'],
                includes=['core', 'std', 'full'],
                cxxflags=['-std=c++14', '-stdlib=libc++'],
                target='dfpnstat')
