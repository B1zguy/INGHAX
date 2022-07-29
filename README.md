# INGHAX
Programmatically login to ING bank. It inputs the login code to the always changing keypad. Immense thanks to [R3zk0n](https://github.com/R3zk0n) for helping implement the OCR components!

## The challenges
- The keys on the keypad change position each page load
- The keys are images, sent as base64

This code be repurposed for logging into any other bank, since ING is the only one (to my knowledge in my country) that doesn't use a password field.