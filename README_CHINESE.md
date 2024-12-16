# Shopping-Agent

**Shopping-Agent** 是一个智能购物助手应用，旨在帮助用户从不同的电商平台上挑选商品并给出定制化的购物建议。通过利用先进的开源框架 **MOFA** 和 **dora-rs** 的 **dataflow** 技术，我们构建了一个高效、模块化且灵活的系统，可以智能地获取和分析用户需求，并为用户提供最佳的购物选择。

## 项目目标

我们的目标是解决当前电商平台购物时信息过载和选择困难的问题。Shopping-Agent 通过智能的多Agent架构，连接多个数据源并自动化处理从网站获取商品信息的流程，减少用户的决策疲劳并提供个性化的购物建议。用户只需简单表达需求，Shopping-Agent 会通过子Agent从不同平台获取商品数据，进行分析，并返回最合适的推荐。

## 技术架构

### 核心组件

1. **MOFA**
   MOFA 是我们的基础框架，支持构建灵活的多Agent系统。我们在此框架上构建了整个购物推荐系统，确保各个子模块（如数据获取、分析等）可以高效地协同工作。
2. **dora-rs Dataflow**
   为了在各个子模块之间实现高效、可扩展的数据流交互，我们使用了 **dora-rs** 的 **dataflow** 。通过数据流管理，我们能够确保从不同平台获取的数据能够顺畅地传递给主Agent进行分析，并最终给出建议。
3. **Main Agent & Sub Agents**（UI）
   主Agent负责接收用户的需求，并通过调用多个子Agent来获取商品数据。每个子Agent负责从一个或多个特定网站抓取商品信息，例如价格、品牌、评价等。主Agent接收到所有子Agent的返回信息后，会根据用户的需求对数据进行分析，给出最终的购物建议。

### 数据流动

1. **用户输入需求**：用户通过自然语言向主Agent表达需求（例如，“我需要一款性价比高的蓝牙耳机”）。
2. **主Agent调用子Agent**：主Agent根据用户需求将任务分配给适当的子Agent，子Agent开始从多个电商网站（如Amazon、worldmarket、balsamhill等）抓取相关商品数据。
3. **数据聚合与分析**：子Agent将抓取到的数据返回主Agent，主Agent对数据进行清洗和分析，结合用户需求，得出最合适的推荐列表。
4. **反馈给用户**：最终，主Agent将推荐结果反馈给用户，帮助其做出购买决策。

## 特性

* **模块化架构**：基于MOFA和dora-rs，整个系统具有高度的模块化，能够轻松扩展和集成更多子Agent，以支持更多电商平台和商品类型。
* **智能分析**：主Agent不仅仅是数据聚合器，它还会结合用户的偏好、购买历史等信息进行深度分析，给出最精准的购物建议。
* **开源**：我们决定将Shopping-Agent开源，欢迎社区成员一起贡献代码，改进系统，支持更多功能。

## 使用方法

### 依赖安装

#### 安装 MOFA

**克隆 shopping-agent 项目**

克隆此项目并切换到指定分支:

```
git clone https://github.com/chengzi0103/mofa_berkeley_hackathon.git && git checkout main
```

进入项目文件夹：

```
cd mofa_berkeley_hackathon
```

使用Python 3.10或以上环境：
如果出现环境版本不匹配，请使用conda重新安装此环境。
例如：

```
conda create -n shopping-agent python=3.10
conda activate shopping-agent
```

安装环境的依赖：

```
cd python && pip3 install -r requirements.txt && pip3 install -e .
```

安装完毕之后，可以使用mofa --help命令查看Cli帮助信息

#### 安装 dora-rs

Rust和Dora-RS安装
由于底层的Dora-RS计算框架基于Rust语言开发，请访问下面的页面，根据你的操作系统安装Rust环境：
https://www.rust-lang.org/tools/install

然后安装 :

```
cargo install dora-cli --locked
```

dora-rs 基于 Rust 开发，请确保您的系统上已经安装了 Rust 环境。

### 配置

在使用Shopping-Agent之前，首先需要对configs目录下面的yml文件进行配置。

```
cp configs/example.yml configs/local.yml
```

大语言模型推理 API配置示例：

使用OpenaiAPI：

```
MODEL:
  MODEL_API_KEY:  
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
```

当然你也可以配置成为Ollama模型，或Moxin提供的本地开源大模型

使用Ollama示例:

```
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.1:11434
```

### 运行

1. 启动dataflow：
2. 启动UI：

用户可以通过命令行界面或API向主Agent发送需求，系统会自动处理并返回购物建议。

## 未来展望

* **多平台支持**：我们计划扩展更多电商平台的支持，能够抓取更多商品数据，给用户提供更丰富的选择。
* **深度学习优化**：通过引入深度学习技术优化商品推荐算法，使得推荐更加智能。
* **个性化功能**：根据用户的历史购物记录、偏好设置等信息，提供更加个性化的购物建议。

## 贡献

我们欢迎任何形式的贡献，包括但不限于：

* 提交bug报告和功能建议
* 提交代码优化或新功能实现
* 编写文档和教程

## License

MIT License. See [LICENSE]() for more details.
