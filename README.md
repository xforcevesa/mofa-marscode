# MOFA-Shopping

**MOFA-Shopping** is an intelligent shopping assistant application designed to help users select products from different e-commerce platforms and provide personalized shopping recommendations. By leveraging the advanced open-source frameworks **MOFA** and **dora-rs**'s **dataflow** technology, we have built an efficient, modular, and flexible system that intelligently gathers and analyzes user needs to provide the best shopping options.

## Project Goals

Our goal is to solve the issues of information overload and choice paralysis that users face while shopping on e-commerce platforms. MOFA-Shopping uses an intelligent multi-Agent architecture to connect multiple data sources and automate the process of retrieving product information from websites, reducing decision fatigue and providing personalized shopping advice. Users only need to express their needs simply, and MOFA-Shopping will use sub-Agents to fetch product data from various platforms, analyze it, and return the most suitable recommendations.

## Technical Architecture

### Core Components

1. **MOFA**

**MOFA** is our core framework, supporting the construction of flexible multi-Agent systems. The entire shopping recommendation system is built on this framework, ensuring that various sub-modules (such as data acquisition, analysis, etc.) can work together efficiently.

2. **dora-rs Dataflow**

To achieve efficient and scalable data flow interactions between sub-modules, we use **dora-rs**'s **dataflow**. Through data flow management, we ensure that data retrieved from different platforms is smoothly passed to the main Agent for analysis and ultimately generates recommendations.

3. **Streamlit UI: User-Friendly Interface for Shopping Assistance**

With **Streamlit**, users can interact with the shopping assistant application in real-time via their browser. Streamlit provides a simple and intuitive front-end interface, allowing users to input their needs. The system then fetches product information from multiple e-commerce platforms in real-time via backend connections and dynamically displays the recommendation results to the user. Streamlit's front-end and back-end separation design ensures a smooth user experience, where all data fetching and analysis occur in the background while the user can easily browse the recommended products through an interactive interface. With components like input boxes, buttons, and filters, users can quickly adjust their needs and instantly see updated recommendations.

### Data Flow

1. **User Inputs a Requirement**: The user expresses their needs to the main Agent in natural language (e.g., "I need a high-performance Bluetooth headset").
2. **Main Agent Calls Sub-Agents**: Based on the user's needs, the main Agent assigns the task to the appropriate sub-Agent, which starts fetching relevant product data from various e-commerce sites (such as Amazon, worldmarket, balsamhill, etc.).
3. **Data Aggregation and Analysis**: The sub-Agent returns the fetched data to the main Agent, which cleans and analyzes the data, combining it with the user's needs to generate the most suitable list of recommendations.
4. **Feedback to the User**: Finally, the main Agent provides the recommendation results to the user, helping them make a purchase decision.

## Features

* **Modular Architecture**: Based on MOFA and dora-rs, the system has a highly modular design, making it easy to expand and integrate more sub-Agents to support more e-commerce platforms and product types.
* **Intelligent Analysis**: The main Agent is not just a data aggregator; it also deeply analyzes the user's preferences, purchase history, and other factors to provide the most accurate shopping suggestions.
* **Open Source**: We have decided to open-source MOFA-Shopping and welcome community contributions to improve the system and support more features.

## Usage

### Dependency Installation

#### Installing MOFA

**Clone the MOFA-Shopping Project**

Clone the project and switch to the main branch:

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">bash</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>copy</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">git clone https://github.com/chengzi0103/mofa_berkeley_hackathon.git && git checkout main
</code></div></div></pre>

Navigate to the project folder:

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">bash</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>copy</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">cd mofa_berkeley_hackathon
</code></div></div></pre>

Use Python 3.10 or later: If there is a version mismatch, reinstall the environment with conda. For example:

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">lua</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>copy</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-lua">conda create -n shopping-agent python=3.10
conda activate shopping-agent
</code></div></div></pre>

Install the environment dependencies:

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">bash</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>copy</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">cd python && pip3 install -r requirements.txt && pip3 install -e .
</code></div></div></pre>

Once installed, you can use the `mofa --help` command to view the CLI help information.

#### Installing dora-rs

Rust and Dora-RS Installation Since the underlying Dora-RS computation framework is developed in Rust, please visit the following page to install Rust based on your operating system: [https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)

Then, install Dora-RS:

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">css</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>copy</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-css">cargo install dora-cli --locked
</code></div></div></pre>

Since dora-rs is developed in Rust, please ensure that Rust is installed on your system.

### Running

1. First, navigate to the `python/berkeley-hackathon/shopping_agents` directory.
2. Create a file named `.env.secret` in this directory with the following structure:

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">makefile</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>copy</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-makefile">API_KEY=
</code></div></div></pre>

3. Run the command `dora up && dora build shopping_dataflow.yml && dora start shopping_dataflow.yml --attach` in the current directory.
4. In another terminal window, run `hitl-agent`.
5. In a separate terminal, use `cd /mofa_berkeley_hackathon/python/berkeley-hackathon/ui && streamlit run socket_client.py` to open the page. Make sure that port 12345 is not in use. If it is, use `lsof -i :12345` to find the process ID and kill it with `kill -9`.

Visit `http://localhost:8501` to start using MOFAagent.

## Future Outlook

* **Multi-Platform Support**: We plan to expand support for more e-commerce platforms, enabling the retrieval of more product data and providing users with a wider range of options.
* **Deep Learning Optimization**: We aim to optimize the product recommendation algorithm by incorporating deep learning techniques to make recommendations more intelligent.
* **Personalized Features**: Based on users' shopping history, preferences, and other factors, we aim to offer more personalized shopping suggestions.

## Contributing

We welcome contributions in any form, including but not limited to:

* Reporting bugs and suggesting features
* Submitting code optimizations or new features
* Writing documentation and tutorials

## License

MIT License. See [LICENSE]() for more details.
