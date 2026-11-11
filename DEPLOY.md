# Launch the interactive Finance Research Lab

The full interactive portfolio is implemented in `app.py` using Streamlit. The five underlying finance engines are in `projects/`, and the case studies are in `case_studies/`.

## Deploy publicly using Streamlit Community Cloud

1. Visit **https://share.streamlit.io** and sign in using GitHub.
2. Choose **Create app** → **Yup, I have an app**.
3. Set these fields:
   - **Repository:** `mdfinancials/Finance-Research-Lab`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (optional):** try `md-finance-research-lab` (availability is not guaranteed).
4. Click **Deploy**. Community Cloud will use the root `requirements.txt`.
5. Open your assigned `.streamlit.app` URL; test the Home page, all five model categories and Applied Case Studies.
6. Make sure the application is public and accessible in a private browser window before using its link on a CV.
7. Add the verified live URL to the GitHub repository description/website field, README and LinkedIn Featured.

**Official instructions:** https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

### Troubleshooting

- If you get `ModuleNotFoundError`, check that `projects/` and `case_studies/` are present, that your main app is `app.py` and that dependencies installed.
- If you get an exception, open **Manage app → Logs**, copy the traceback, and fix the relevant function in GitHub.
- If GitHub Actions tests are queued, that is not evidence they have passed. Check the latest workflow run before presenting this as a tested release.
- The app should be identified as an educational portfolio with model assumptions disclosed. Never upload sensitive bank/customer information, proprietary code or secrets.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest -q
streamlit run app.py
```

### Final recruiter-readiness checklist
- [ ] Streamlit app is live and reachable without logging in.
- [ ] Home page loads without errors.
- [ ] Five categories and five applied case studies render without errors.
- [ ] GitHub Actions checks pass on the published commit.
- [ ] NVIDIA Excel workbook uploaded separately if presenting spreadsheet work.
- [ ] Case studies clearly distinguish sourced results from hypothetical model inputs.
