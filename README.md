# DiskANN

[![DiskANN Main](https://github.com/microsoft/DiskANN/actions/workflows/push-test.yml/badge.svg?branch=main)](https://github.com/microsoft/DiskANN/actions/workflows/push-test.yml)
[![PyPI version](https://img.shields.io/pypi/v/diskannpy.svg)](https://pypi.org/project/diskannpy/)
[![Downloads shield](https://pepy.tech/badge/diskannpy)](https://pepy.tech/project/diskannpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![DiskANN Paper](https://img.shields.io/badge/Paper-NeurIPS%3A_DiskANN-blue)](https://papers.nips.cc/paper/9527-rand-nsg-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node.pdf)
[![DiskANN Paper](https://img.shields.io/badge/Paper-Arxiv%3A_Fresh--DiskANN-blue)](https://arxiv.org/abs/2105.09613)
[![DiskANN Paper](https://img.shields.io/badge/Paper-Filtered--DiskANN-blue)](https://harsha-simhadri.org/pubs/Filtered-DiskANN23.pdf)


DiskANN is a suite of scalable, accurate and cost-effective approximate nearest neighbor search algorithms for large-scale vector search that support real-time changes and simple filters.
This code is based on ideas from the [DiskANN](https://papers.nips.cc/paper/9527-rand-nsg-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node.pdf), [Fresh-DiskANN](https://arxiv.org/abs/2105.09613) and the [Filtered-DiskANN](https://harsha-simhadri.org/pubs/Filtered-DiskANN23.pdf) papers with further improvements. 
This code forked off from [code for NSG](https://github.com/ZJULearning/nsg) algorithm.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

See [guidelines](CONTRIBUTING.md) for contributing to this project.

## Linux build:

Install the following packages through apt-get

```bash
sudo apt install make cmake g++ libaio-dev libgoogle-perftools-dev clang-format libboost-all-dev
```

### Install Intel MKL
#### Ubuntu 20.04 or newer
```bash
sudo apt install libmkl-full-dev
```

#### Earlier versions of Ubuntu
Install Intel MKL either by downloading the [oneAPI MKL installer](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html) or using [apt](https://software.intel.com/en-us/articles/installing-intel-free-libs-and-python-apt-repo) (we tested with build 2019.4-070 and 2022.1.2.146).

```
# OneAPI MKL Installer
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18487/l_BaseKit_p_2022.1.2.146.sh
sudo sh l_BaseKit_p_2022.1.2.146.sh -a --components intel.oneapi.lin.mkl.devel --action install --eula accept -s
```

### Build
```bash
mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j 
```

## Windows build:

The Windows version has been tested with Enterprise editions of Visual Studio 2022, 2019 and 2017. It should work with the Community and Professional editions as well without any changes. 

**Prerequisites:**

* CMake 3.15+ (available in VisualStudio 2019+ or from https://cmake.org)
* NuGet.exe (install from https://www.nuget.org/downloads)
    * The build script will use NuGet to get MKL, OpenMP and Boost packages.
* DiskANN git repository checked out together with submodules. To check out submodules after git clone:
```
git submodule init
git submodule update
```

* Environment variables: 
    * [optional] If you would like to override the Boost library listed in windows/packages.config.in, set BOOST_ROOT to your Boost folder.

**Build steps:**
* Open the "x64 Native Tools Command Prompt for VS 2019" (or corresponding version) and change to DiskANN folder
* Create a "build" directory inside it
* Change to the "build" directory and run
```
cmake ..
```
OR for Visual Studio 2017 and earlier:
```
<full-path-to-installed-cmake>\cmake ..
```
**This will create a diskann.sln solution**. Now you can:

- Open it from VisualStudio and build either Release or Debug configuration.
- `<full-path-to-installed-cmake>\cmake --build build`
- Use MSBuild:
```
msbuild.exe diskann.sln /m /nologo /t:Build /p:Configuration="Release" /property:Platform="x64"
```

* This will also build gperftools submodule for libtcmalloc_minimal dependency.
* Generated binaries are stored in the x64/Release or x64/Debug directories.

## Usage:

### Quick Start Guide

Follow these steps to run the diversity-enabled DiskANN algorithm:

#### 1. Download and Prepare Dataset

First, create a data directory and download the SIFT dataset:

```bash
mkdir data
cd data
wget ftp://ftp.irisa.fr/local/texmex/corpus/siftsmall.tar.gz
tar -xf siftsmall.tar.gz
cd ..
```

Convert the dataset from `.fvecs` format to `.bin` format:

```bash
./build/apps/utils/fvecs_to_bin float data/siftsmall/siftsmall_base.fvecs data/siftsmall/siftsmall_base.fbin
./build/apps/utils/fvecs_to_bin float data/siftsmall/siftsmall_query.fvecs data/siftsmall/siftsmall_query.fbin
```

#### 2. Generate Seller File

Generate a seller file for diversity-aware search:

```bash
python generate_skewed_seller.py --num_vectors 10000 --output_file siftsmall_skewed_sellers.txt
```

#### 3. Compute Ground Truth

Compute the diverse ground truth for evaluation:

```bash
./build/apps/utils/compute_diverse_groundtruth --data_type float --dist_fn l2 \
  --base_file data/siftsmall/siftsmall_base.fbin \
  --query_file data/siftsmall/siftsmall_query.fbin \
  --seller_file siftsmall_skewed_sellers.txt \
  --gt_file siftsmall_skewed_diverse_gt.bin \
  --K 10 --KperSeller 1
```

#### 4. Build Index

Build the diversity-enabled memory index:

```bash
./build/apps/build_memory_index --data_type float --dist_fn l2 \
  --data_path data/siftsmall/siftsmall_base.fbin \
  --index_path_prefix siftsmall_skewed_diverse \
  --max_degree 16 --Lbuild 32 --alpha 1.2 --num_threads 8 \
  --seller_file siftsmall_skewed_sellers.txt --NumDiverse 10
```

#### 5. Search Index

Perform diverse search on the built index:

```bash
./build/apps/search_memory_index --data_type float --dist_fn l2 \
  --index_path_prefix siftsmall_skewed_diverse \
  --query_file data/siftsmall/siftsmall_query.fbin \
  --gt_file siftsmall_skewed_diverse_gt.bin \
  -K 10 -L 20 30 40 50 60 70 80 90 100 --num_threads 8 \
  --result_path search_results.txt --diverse_search true \
  --seller_file siftsmall_skewed_sellers.txt --max_K_per_seller 1
```

The output I ran on my laptop with siftsmall:
```
  Ls         QPS     Avg dist cmps  Mean Latency (mus)   99.9 Latency   Recall@10
=================================================================================
  11    48938.04            179.60               67.73         533.30       70.10
  20   206910.82            250.37               35.14          72.60       75.50
  30   168548.79            319.22               43.49         108.80       78.90
  40   180929.98            383.70               41.13         149.60       80.60
  50   108178.28            450.52               69.47         395.30       82.10
  60   126502.21            516.67               59.16         133.10       83.30
  70   108213.40            585.01               69.51         248.60       85.20
  80   104876.77            648.10               71.76         420.50       86.40
  90    96683.75            713.31               78.56         531.80       87.60
 100    93379.40            774.87               80.61         384.00       89.60
```

#### Complete Example

For a complete working example, see the commands in `sift_test.sh`.

### Advanced Usage

For more detailed documentation on other features:

- [Commandline interface for building and search SSD based indices](workflows/SSD_index.md)  
- [Commandline interface for building and search in memory indices](workflows/in_memory_index.md) 
- [Commandline examples for using in-memory streaming indices](workflows/dynamic_index.md)
- [Commandline interface for building and search in memory indices with label data and filters](workflows/filtered_in_memory.md)
- [Commandline interface for building and search SSD based indices with label data and filters](workflows/filtered_ssd_index.md)
- [diskannpy - DiskANN as a python extension module](python/README.md)

Please cite this software in your work as:

```
@misc{diskann-github,
   author = {Simhadri, Harsha Vardhan and Krishnaswamy, Ravishankar and Srinivasa, Gopal and Subramanya, Suhas Jayaram and Antonijevic, Andrija and Pryce, Dax and Kaczynski, David and Williams, Shane and Gollapudi, Siddarth and Sivashankar, Varun and Karia, Neel and Singh, Aditi and Jaiswal, Shikhar and Mahapatro, Neelam and Adams, Philip and Tower, Bryan and Patel, Yash}},
   title = {{DiskANN: Graph-structured Indices for Scalable, Fast, Fresh and Filtered Approximate Nearest Neighbor Search}},
   url = {https://github.com/Microsoft/DiskANN},
   version = {0.6.1},
   year = {2023}
}
```
