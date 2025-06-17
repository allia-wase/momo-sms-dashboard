import xml.etree.ElementTree as ET
import re
import logging

logging.basicConfig(filename='logs/unprocessed_sms.log', level=logging.WARNING)

# Define regex patterns for each transaction type
patterns = {
    "Incoming Money": r"You have received (\d+) RWF from (.+?)\. Transaction ID: ([\w\d]+)\. Date: ([\d\- :]+)\.",
    "Airtime Bill Payment": r".*Airtime.*?(\d+) RWF.*?TxId:? ?([\w\d]+).*?Date: ([\d\- :]+)",
    "Withdrawal from Agent": r"have via agent: (.+?) $$(\d+)$$, withdrawn (\d+) RWF on ([\d\- :]+)\.",
    "Bank Deposit": r"Your bank deposit of (\d+) RWF was successful.*?Transaction ID: ([\w\d]+).*?Date: ([\d\- :]+)",
    "Payment to Code Holder": r"Your payment of (\d+) RWF to (.+?) has been completed.*?TxId:? ?([\w\d]+).*?Date: ([\d\- :]+)"
}

def extract_data(sms_body):
    for tx_type, pattern in patterns.items():
        match = re.search(pattern, sms_body)
        if match:
            amount = int(match.group(1))
            sender_or_recipient = match.group(2)
            transaction_id = match.group(3) if len(match.groups()) >= 3 else None
            date = match.group(4) if len(match.groups()) >= 4 else None

            return {
                'type': tx_type,
                'amount': amount,
                'sender': sender_or_recipient if tx_type == "Incoming Money" or tx_type == "Withdrawal from Agent" else None,
                'recipient': sender_or_recipient if tx_type != "Incoming Money" and tx_type != "Withdrawal from Agent" else None,
                'transaction_id': transaction_id,
                'date': date,
                'description': sms_body
            }
    logging.warning(f"Unmatched SMS: {sms_body}")
    return None

def parse_sms_file(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    transactions = []
    for sms in root.findall('sms'):
        body = sms.find('body').text.strip()
        data = extract_data(body)
        if data:
            transactions.append(data)
    return transactions

if __name__ == "__main__":
    transactions = parse_sms_file("data/sms.xml")
    print(f"Parsed {len(transactions)} messages.")
