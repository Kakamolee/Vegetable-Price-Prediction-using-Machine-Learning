# Function for forgot password

def mypassword():
    def fpassword():
        # Declare a digits variable
        # which stores all digits
        digits = "0123456789"
        OTP = ""

        # length of password can be changed
        # by changing value in range
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]

        return OTP

    content = fpassword()

    receipent_email = input("Enter Your Registered Email Id : ")
    temp = content
    print(temp)
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()  # identify computer
    mail.starttls()  # transport layer security
    # admin mail-id and password (check that the account should off the less secure app in settings)
    mail.login('beprojectvpp@gmail.com', '20192020')
    # first mail-id for recipients second is for admin
    header = 'To:' + receipent_email + '\n' + 'From: ' \
             + 'BE-Project Password Reset' + '\n' + 'Subject : Your OTP For Resetting Password \n'

    content = header + content
    mail.sendmail('beprojectvpp@gmail.com', receipent_email, content)
    mail.close()
