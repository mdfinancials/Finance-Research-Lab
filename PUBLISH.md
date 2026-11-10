# Publishing to GitHub

1. Sign into GitHub and create a **public** repository called `finance-research-lab` (do not initialise with a README).
2. Extract the supplied zip, open a terminal in the `finance-portfolio` folder.
3. Run:

```bash
git init
git add .
git commit -m "Initial finance research portfolio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/finance-research-lab.git
git push -u origin main
```

4. Check that the **Actions** tab's Python model tests pass.
5. Optionally deploy the Streamlit app at https://share.streamlit.io/ by selecting `app.py` from this repository. A Streamlit deployment account and permissions are required.
6. Add the repository URL to your CV and LinkedIn **Featured** section. Optionally add the Streamlit live-demo URL.

Never publish personal banking/customer data, work files, internal tools, credentials, or employer intellectual property.
