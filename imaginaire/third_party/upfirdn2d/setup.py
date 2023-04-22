# flake8: noqa
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os


cuda_version = os.getenv('CUDA_VERSION')
print(f'CUDA_VERSION: {cuda_version}')

nvcc_args = [
    '-gencode',
    'arch=compute_70,code=sm_70',
    '-gencode',
    'arch=compute_75,code=sm_75',
]
if cuda_version is not None and cuda_version >= '11.0':
    nvcc_args.extend(('-gencode', 'arch=compute_80,code=sm_80'))
nvcc_args.extend(('-Xcompiler', '-Wall', '-std=c++14'))
setup(
    name='upfirdn2d_cuda',
    py_modules=['upfirdn2d'],
    ext_modules=[
        CUDAExtension('upfirdn2d_cuda', [
            './src/upfirdn2d_cuda.cc',
            './src/upfirdn2d_cuda_kernel.cu'
        ], extra_compile_args={'cxx': ['-Wall', '-std=c++14'],
                               'nvcc': nvcc_args})
    ],
    cmdclass={
        'build_ext': BuildExtension
    })
