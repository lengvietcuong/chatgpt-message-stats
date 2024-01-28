# ChatGPTMessageStats
A Python script that counts your messages on ChatGPT, returning the total number of messages, words, tokens, and characters.

## Installation
Clone the repository:
```bash
git clone https://github.com/lengvietcuong/chatgpt-message-stats.git
```
Install requirements using
```bash
pip install -r requirements.txt
```

## How to download your ChatGPT data
1. Go to https://chat.openai.com.
2. Click on your profile (bottom-left corner).
3. Settings -> Data controls -> Export data -> Export -> Confirm export.
4. Check your email inbox for the download link.

## Usage
1. Move your downloaded data file to the `data` folder in the project directory (no need to unzip).
2. Run `counter.py` and enjoy!

## Sample Output
```
💬 Messages
╒═════════╤═══════╕
│ User    │ 2,001 │
├─────────┼───────┤
│ ChatGPT │ 2,024 │
├─────────┼───────┤
│ Total   │ 4,025 │
╘═════════╧═══════╛

🔤 Words
╒═════════╤═════════╕
│ User    │  94,546 │
├─────────┼─────────┤
│ ChatGPT │ 394,872 │
├─────────┼─────────┤
│ Total   │ 489,418 │
╘═════════╧═════════╛

🟡 Tokens
╒═════════╤═════════╕
│ User    │ 170,627 │
├─────────┼─────────┤
│ ChatGPT │ 644,476 │
├─────────┼─────────┤
│ Total   │ 815,103 │
╘═════════╧═════════╛

ℹ️ Chars
╒═════════╤═══════════╕
│ User    │   773,619 │
├─────────┼───────────┤
│ ChatGPT │ 2,927,812 │
├─────────┼───────────┤
│ Total   │ 3,701,431 │
╘═════════╧═══════════╛
```