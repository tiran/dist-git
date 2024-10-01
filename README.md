# dist-git

RPM spec files

- `fasttext`, https://github.com/PeterStaar-IBM/fastText fork
- `json-schema-validator`, https://github.com/pboettch/json-schema-validator
- `libpdfium`, https://pdfium.googlesource.com/pdfium for `pypdfium2`
- `llvm-aotrition`, MLIR build of LLVM for ROCm's aotriton
- `llvm-triton`, MLIR build of LLVM for Triton
- `mock-pandoc`, empty pandoc package

## COPR

[`copr-cli`](https://docs.pagure.org/copr.copr/user_documentation.html)

```shell
copr-cli add-package-distgit --distgit fedora --commit epel9 cheimes/deepsearch-glm --name cxxopts

copr-cli build-package --nowait cheimes/deepsearch-glm --name cxxopts
```

```shell
copr-cli add-package-scm --clone-url https://github.com/tiran/dist-git.git --commit main --type git --method rpkg cheimes/deepsearch-glm --subdir fasttext --spec fasttext.spec --name fasttext

copr-cli build-package --nowait cheimes/deepsearch-glm --name fasttext
```
