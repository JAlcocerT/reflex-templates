```sh
source .env
#export FORM_BRICKS_SHEET_URL="https://docs.google.com/spreadsheets/d/whateveryourgsheetis/export?format=csv"
```

---

## Testing `check_formbricks_subscription`

You can test the email validation function using a simple script. Here is an example:

```sh
python3 utils_test.py
```

**Tip:**
- Make sure to set the `FORM_BRICKS_SHEET_URL` environment variable before running your test.
- You can run this test from the `/login_formbricks` directory with `python -i utils.py` or by saving the snippet as `test_utils.py` and running `python test_utils.py`.