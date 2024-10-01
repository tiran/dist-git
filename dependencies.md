# Dependency trees

## deepsearch-glm

```mermaid
---
title: deepsearch-glm build dependencies
---
flowchart LR
    ROOT{rhel9}
    cxxopts --> ROOT
    doctest --> ROOT
    fasttext --> ROOT
    fmt --> ROOT
    gperftools --> libunwind
    json --> doctest
    json-schema-validator --> json
    libunwind --> ROOT
    loguru --> ROOT
    sentencepiece --> gperftools
```

## libpdfium

```mermaid
---
title: libpdfium build dependencies
---
flowchart LR
    ROOT{rhel9}
    gn --> ROOT
    libpdfium --> gn
```

## OpenCV

```mermaid
---
title: OpenCV build dependencies
---
flowchart LR
    ROOT{rhel9}
    opencv --> gdal & gdcm & hdf5 & glog & python-beautifulsoup4
    opencv -. optional (bcond libmfx) .-> intel-mediasdk
    armadillo --> SuperLU & arpack & hdf5
    arpack --> ROOT
    cfitsio --> ROOT
    CharLS --> ROOT
    dcmtk --> ROOT
    freexl --> ROOT
    gdal --> CharLS & armadillo & cfitsio & freexl & geos & hdf & hdf5 & libdap & libgeotiff & libgta & libkml & libspatialite & netcdf & ogdi & proj & python-breathe & xerces-c
    gdcm --> dcmtk & gl2ps
    gl2ps --> ROOT
    geos --> ROOT
    gflags --> ROOT
    glog --> gflags
    gtest --> gflags
    hdf5 --> libaec
    hdf --> libaec
    intel-mediasdk --> gtest
    libaec --> ROOT
    libbsd --> libmd
    libdap --> ROOT
    libgeotiff --> proj
    libgta --> ROOT
    libkml --> gtest & uriparser
    libmd --> ROOT
    librttopo --> geos
    libspatialite --> freexl & geos & librttopo & minizip & proj
    metis --> ROOT
    minizip --> libbsd
    netcdf --> hdf & hdf5
    ogdi --> ROOT
    proj --> gtest
    python-beautifulsoup4 --> ROOT
    python-breathe --> ROOT
    SuperLU --> metis
    uriparser --> gtest
    xerces-c --> ROOT
```

## Base

```mermaid
---
title: Base dependencies
---
flowchart LR
    ROOT{rhel9}
    ccache --> ROOT
    gflags --> ROOT
    gperftools --> libunwind
    gtest --> gflags
    jemalloc --> ROOT
    libfabric --> ROOT
    libid3tag --> ROOT
    libsodium --> ROOT
    libunwind --> ROOT
    llvm14 --> python-recommonmark
    llvm-aotriton --> ROOT
    llvm-triton --> ROOT
    nvtop --> gtest
    openmpi --> ROOT
    openpgm --> ROOT
    opusfile --> ROOT
    python-CommonMark --> python-hypothesis
    python-hypothesis --> python-sortedcontainers
    python-recommonmark --> python-CommonMark
    python-sortedcontainers --> ROOT
    rapidjson --> gtest
    re2 --> gtest
    sox --> libid3tag & opusfule
    thrift --> ROOT
    xsimd --> gtest
    zeromq --> libsodium & libunwind & openpgm
```
