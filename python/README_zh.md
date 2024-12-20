# MoFA for Dora-RS

在这个分支里，我们介绍建立在Dora-RS上的MoFA框架。

## Getting started

### 1. 安装

1. 克隆此项目切换到指定分支:

```sh
git clone <repository-url>  
```

**示例**:

```sh
git clone git@github.com:moxin-org/mofa.git && cd mofa
```

2. 使用Python 3.10或以上环境：

- 如果出现环境版本不匹配，请使用conda重新安装此环境。例如：

```sh
conda create -n py310 python=3.10.12 -y
```

3. 项目环境部署

- 安装环境的依赖：

```sh
cd python && pip3 install -r requirements.txt && pip3 install -e .

```

安装完毕之后，可以使用`mofa --help`命令查看Cli帮助信息

4. Rust和Dora-RS安装

由于底层的Dora-RS计算框架基于Rust语言开发，请你访问下面的页面，根据你的操作系统安装Rust环境：

```sh
https://www.rust-lang.org/tools/install
```
然后安装 `cargo install dora-cli --locked`


5. 运行 berkeley-hackathon
详情查看 [berkeley-hackathon.md](berkeley-hackathon/shopping_agents/README.md)