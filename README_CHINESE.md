# MOFA-Shopping

**MOFA-Shopping** 是一个智能购物助手应用，旨在帮助用户从不同的电商平台上挑选商品并给出定制化的购物建议。通过利用先进的开源框架 **MOFA** 和 **dora-rs** 的 **dataflow** 技术，我们构建了一个高效、模块化且灵活的系统，可以智能地获取和分析用户需求，并为用户提供最佳的购物选择。

## 项目目标

我们的目标是解决当前电商平台购物时信息过载和选择困难的问题。 MOFA-Shopping通过智能的多Agent架构，连接多个数据源并自动化处理从网站获取商品信息的流程，减少用户的决策疲劳并提供个性化的购物建议。用户只需简单表达需求，MOFA-Shopping 会通过子Agent从不同平台获取商品数据，进行分析，并返回最合适的推荐。

## 技术架构

### 核心组件

1. **MOFA**

**MOFA** 是我们的基础框架，支持构建灵活的多Agent系统。我们在此框架上构建了整个购物推荐系统，确保各个子模块（如数据获取、分析等）可以高效地协同工作。

2. **dora-rs Dataflow**

为了在各个子模块之间实现高效、可扩展的数据流交互，我们使用了 **dora-rs** 的 **dataflow** 。通过数据流管理，我们能够确保从不同平台获取的数据能够顺畅地传递给主Agent进行分析，并最终给出建议。

3. **Streamlit UI: User-Friendly Interface for Shopping Assistance**

通过 **Streamlit**，用户可以在浏览器中与购物助手应用进行实时互动。Streamlit 提供了一个简洁而直观的前端界面，用户只需输入需求，系统便会通过与后端的连接，实时获取来自多个电商平台的商品信息，并将推荐结果动态展示给用户。Streamlit 的前后端分离设计使得用户体验更加流畅，所有的数据抓取与分析处理都在后台进行，而用户则通过交互式的界面轻松浏览推荐商品。通过输入框、按钮、筛选器等组件，用户能够快速调整需求并即时看到更新的推荐结果。

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

**克隆 MOFA-Shopping 项目**

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

### 运行


1. 首先进入到 `python/berkeley-hackathon/shopping_agents` 目录下
2. 在当前目录下创建一个文件 名字叫做`.env.secret`,结构如下

~~~
API_KEY=
~~~

3. 在当前目录下运行命令 `dora up && dora build shopping_dataflow.yml && dora start shopping_dataflow.yml --attach`
4. 在另外一个命令端下面运行 `hitl-agent`
5. 开启另外一个命令端,在命令行中使用`cd /mofa_berkeley_hackathon/python/berkeley-hackathon/ui && streamlit run socket_client.py` 可以看到你的页面打开了。 保证你的端口12345没有被占用，如果被占用了，使用`lsof -i :12345`来查看被占用的进程号，使用  kill -9 删除它

访问`http://localhost:8501`，开始使用MOFAagent

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
