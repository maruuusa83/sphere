# coding: utf-8
# author: Daichi Teruya
from distutils.core import setup, Extension
import subprocess
import os

module = Extension('PyStitcher',
                   ['./src/PyStitcher.cpp'],
                   extra_compile_args=[
                        '-std=c++11',
                        '-I/usr/include/opencv'
                   ],
                   extra_link_args=[ # 必要なOpenCVライブラリが増えたらここへ
                        '-Wl,-R/usr/lib',
                        '/usr/lib/libopencv_core.so',
                        '/usr/lib/libopencv_imgcodecs.so',
                        '/usr/lib/libopencv_stitching.so'
                   ]
                   );

setup(name='PyStitcher',
      version='0.1.0',
      ext_modules=[module]
      );

