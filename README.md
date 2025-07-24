# README MAGIK
![readme-magik-banner.png](readme-magik-banner.png)

This project uses a GitHub Action to automatically generate and update the `README.md` on your GitHub profile repository (`your-username/your-username`).

## Setup Guide

To get this running on your own profile, follow these steps:

1.  **Fork this Repository**
    Click the "Fork" button at the top-right of this page to create your own copy of this project.

2.  **Create a Profile Repository**
    If you don't have one already, create a new public repository with the same name as your GitHub username (e.g., `jayx2u/jayx2u`). A `README.md` file in this repository will appear on your public profile page.

3.  **Generate a Personal Access Token (PAT)**
    The workflow requires a PAT to read your repository statistics and commit the updated README to your profile repository.
    *   Go to **Settings** > **Developer settings** > **Personal access tokens** > **Fine-grained tokens**.
    *   Click **Generate new token**.
    *   Give it a name (e.g., `readme-magik-token`) and set the expiration to `No expiration`.
    *   Under **Repository access**, select **Only select repositories** and choose your profile repository (e.g., `jayx2u/jayx2u`).
    *   Under **Permissions**, go to **Repository permissions**.
    *   Set **Contents** to `Read and write`. This allows the action to check out your profile repository and push the updated README.
    *   Click **Generate token** and copy the token value. You will not be able to see it again.

4.  **Add the PAT as a Repository Secret**
    *   In your forked `readme-magik` repository, go to **Settings** > **Secrets and variables** > **Actions**.
    *   Click **New repository secret**.
    *   Name the secret `REPO_PAT`.
    *   Paste the PAT you copied in the previous step into the "Secret" field.
    *   Click **Add secret**.

5.  **Run the Workflow**
    The workflow is configured to run automatically every hour or on a push to the `main` branch.

After the workflow completes, your profile README should be updated!