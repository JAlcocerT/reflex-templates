from utils import check_formbricks_subscription, get_authorized_emails

# Print all authorized emails
print("Authorized emails:")
for email in get_authorized_emails():
    print("-", email)

# Replace with an email you expect to be in your Google Sheet
#email_to_test = "yosuaporco@gmail.com"
email_to_test = "test@example.com"

if check_formbricks_subscription(email_to_test):
    print(f"{email_to_test} is authorized!")
else:
    print(f"{email_to_test} is NOT authorized.")