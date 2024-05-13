import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver_email, name, exam_data):
    sender_email = "sender@gmail.com"  # Update with your sender Gmail address
    sender_password = ""  # Update with your Google account app password (turn on 2FA and search for app password and generate in accounts settings)

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Exam Data Available"

    # Email body
    body = f"Dear {name},\n\nThe following exam data is available:\n\n"
    for exam in exam_data:
        symbol_no = exam['SymbolNo']
        subject_name = exam['SubjectName']
        room_no = exam['RoomNo']
        body += f"Symbol No: {symbol_no}\nSubject: {subject_name}\nRoom No: {room_no}\n\n"

    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send email
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

def main():
    symbol_numbers = {
        "118102038": "anishbista9235@gmail.com",
        "118102040": "minusking2002@gmail.com",
        "118102041": "diamondthagunna@gmail.com",
        "118102042": "joeh5730@gmail.com",
        "118102050": "sabeenpandey2@gmail.com",
        "118102051": "sajan7ghimire@gmail.com"
    }

    for symbol_no, receiver_email in symbol_numbers.items():
        api_url = f"https://www.janamaitri.edu.np/student-exam-data?exam_data={symbol_no}"

        try:
            response = requests.get(api_url)
            data = response.json()

            if data['status'] == 'success':
                exam_data = data['data']
                name = get_name(symbol_no)
                send_email(receiver_email, name, exam_data)
                print(f"Email sent successfully to {receiver_email}.")
            else:
                print(f"No action needed for symbol number {symbol_no}. API response:", data)
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while making the request for symbol number {symbol_no}:", e)
        except KeyError:
            print(f"Error: Unexpected response format from the API for symbol number {symbol_no}.")

def get_name(symbol_no):
    names = {
        "118102038": "Anish Bista",
        "118102040": "Bimal Paudel",
        "118102041": "Deepak Thagunna",
        "118102042": "Dibesh Shah",
        "118102050": "Sabin Pandey",
        "118102051": "Sajan Ghimire"
    }
    return names.get(symbol_no, "Unknown")

if __name__ == "__main__":
    main()

