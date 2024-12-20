# MoFA for Dora-RS

In this branch, we introduce the MoFA framework built on Dora-RS.

## Getting Started

### 1. Installation

1. **Clone the Repository and Switch to the Specified Branch:**

   ```sh
   git clone <repository-url>
   ```

   **Example:**

   ```sh
   git clone git@github.com:moxin-org/mofa.git && cd mofa
   ```

2. **Ensure Python 3.10 or Higher is Installed:**

   - If you encounter a version mismatch, use `conda` to create a new environment. For example:

     ```sh
     conda create -n py310 python=3.10.12 -y
     ```

3. **Set Up the Project Environment:**

   - Install the required dependencies:

     ```sh
     cd python
     pip3 install -r requirements.txt
     pip3 install -e .
     ```

   - After installation, you can view the CLI help information using:

     ```sh
     mofa --help
     ```

4. **Install Rust and Dora-RS:**

   - Since the underlying Dora-RS computation framework is developed in Rust, install the Rust environment by visiting:

     ```sh
     https://www.rust-lang.org/tools/install
     ```

   - After installing Rust, install the Dora CLI tool:

     ```sh
     cargo install dora-cli --locked
     ```

5. **Run Berkeley-Hackathon:**

   - For detailed instructions, refer to [berkeley-hackathon.md](berkeley-hackathon/shopping_agents/README.md).

---

## Additional Notes

- **Environment Activation:**
  After creating the Conda environment, activate it using:

  ```sh
  conda activate py310
  ```

- **Verifying Installations:**
  - **Python Version:**

    ```sh
    python --version
    ```

    Ensure it returns Python 3.10.x or higher.

  - **Rust Installation:**

    ```sh
    rustc --version
    ```

    Ensure Rust is installed correctly.

  - **Dora CLI:**

    ```sh
    dora --version
    ```

    Verify that the Dora CLI is installed and accessible.

- **Troubleshooting:**
  - If you encounter issues during installation, ensure that all prerequisites are met and that your system meets the necessary requirements.
  - For Rust-related issues, refer to the [Rust installation guide](https://www.rust-lang.org/tools/install) for detailed troubleshooting steps.
  - For Python dependency issues, consider using virtual environments or Docker containers to isolate the project dependencies.
