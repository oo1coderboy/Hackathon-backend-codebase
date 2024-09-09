import random
import re
from datetime import datetime

#####################---------------DATE---------------##########################
 
def generate_random_day(month, year):
    # Return a random day based on the month and year to ensure the date is valid
    if month in ['April', 'June', 'September', 'November']:
        return random.randint(1, 30)
    elif month == 'February':
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # Leap year check
            return random.randint(1, 29)
        else:
            return random.randint(1, 28)
    else:
        return random.randint(1, 31)
 
def generate_random_date(old_val):
    # Define date patterns
    date_patterns = [
        (r'\b(\d{4})-(\d{2})-(\d{2})\b', '%Y-%m-%d'),             # YYYY-MM-DD
        (r'\b(\d{2})/(\d{2})/(\d{4})\b', '%m/%d/%Y'),             # MM/DD/YYYY
        (r'\b(\d{2})-(\d{2})-(\d{4})\b', '%d-%m-%Y'),             # DD-MM-YYYY
        (r'\b(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December),? (\d{4})\b', '%d %B %Y'),  # DD Month YYYY
        (r'\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (\d{4})\b', '%B %d, %Y')   # Month DD, YYYY
    ]
 
    new_val = old_val
 
    for pattern, date_format in date_patterns:
        match = re.search(pattern, old_val)
        if match:
            if date_format in ['%d %B %Y', '%B %d, %Y']:
                # Extract the current day, month, and year
                if date_format == '%d %B %Y':
                    day, month, year = match.groups()
                else:
                    month, day, year = match.groups()
                new_day = generate_random_day(month, int(year))
                if date_format == '%d %B %Y':
                    new_val = f"{new_day} {month} {year}"
                else:
                    new_val = f"{month} {new_day}, {year}"
            else:
                # Parse the date
                date_obj = datetime.strptime(old_val, date_format)
                # Generate a random day for the given month and year
                new_day = generate_random_day(date_obj.strftime('%B'), date_obj.year)
                # Replace the day part of the date
                if date_format == '%Y-%m-%d':
                    new_val = f"{date_obj.year}-{date_obj.month:02d}-{new_day:02d}"
                elif date_format == '%m/%d/%Y':
                    new_val = f"{date_obj.month:02d}/{new_day:02d}/{date_obj.year}"
                elif date_format == '%d-%m-%Y':
                    new_val = f"{new_day:02d}-{date_obj.month:02d}-{date_obj.year}"
            break
 
    return new_val


#############################Testing function for japan phone no and us phone number##################################

# def generate_new_us_phone_number(phone_number):
#     # Clean the input phone number by removing non-digit characters
#     cleaned_number = ''.join(filter(str.isdigit, phone_number))

#     # Determine the area code based on the cleaned number
#     if cleaned_number.startswith("1"):
#         area_code = cleaned_number[1:4]
#     else:
#         area_code = cleaned_number[:3]

#     # Generate random central office code and line number
#     central_office_code = random.randint(200, 999)
#     line_number = random.randint(1000, 9999)

#     # Format the fake US phone number
#     fake_phone_number = f"({area_code}) {central_office_code}-{line_number}"
#     return fake_phone_number

def random_phone_number(length):
    return ''.join(random.choices('0123456789', k=length))
 
def generate_new_us_phone_number(phone_number):
    us_pattern = r'(\+1[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4})|(\(\d{3}\)[-]?\d{3}[-]?\d{4})|(\d{3}[-\s]?\d{3}[-\s]?\d{4})|(\d{10})'
    match = re.match(us_pattern, phone_number)
    if not match:
        raise ValueError("Input is not a valid US phone number")
    if re.match(r'\+1[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}', phone_number):
        parts = re.findall(r'\d+', phone_number)
        new_number = f'+1-{random_phone_number(3)}-{random_phone_number(3)}-{random_phone_number(4)}'
    elif re.match(r'\(\d{3}\)[-]?\d{3}[-]?\d{4}', phone_number):
        parts = re.findall(r'\d+', phone_number)
        new_number = f'({random_phone_number(3)}){random_phone_number(3)}-{random_phone_number(4)}'
    elif re.match(r'\d{3}[-\s]?\d{3}[-\s]?\d{4}', phone_number):
        parts = re.findall(r'\d+', phone_number)
        new_number = f'{random_phone_number(3)}-{random_phone_number(3)}-{random_phone_number(4)}'
    elif re.match(r'\d{10}', phone_number):
        new_number = random_phone_number(10)
    else:
        new_number = phone_number  # This should not happen with the given pattern
    return new_number

# def generate_new_japan_phone_number(mobile_number):
#     # Clean the input mobile number by removing non-digit characters
#     cleaned_number = ''.join(filter(str.isdigit, mobile_number))

#     # Ensure the country code and first digit structure is preserved
#     fake_number = list(cleaned_number)
#     for i in range(len(fake_number)):
#         if fake_number[i].isdigit():
#             # Replace each digit with a random digit from 0 to 9
#             fake_number[i] = str(random.randint(0, 9))

#     # Format the fake Japan phone number as per the input structure
#     fake_japan_phone_number = f"+81-{fake_number[3]}-{fake_number[4:8]}-{fake_number[8:]}"
#     return fake_japan_phone_number


def random_phone_number(length):
    return ''.join(random.choices('0123456789', k=length))
 
def generate_new_japan_phone_number(phone_number):
    japan_pattern = r'(\+81[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{4})|(\(0\d{1,4}\)[-]?\d{1,4}[-]?\d{4})|(0\d{1,4}[-]?\d{1,4}[-]?\d{4})'
    match = re.match(japan_pattern, phone_number)
    if not match:
        raise ValueError("Input is not a valid Japan phone number")
 
    if re.match(r'\+81[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{4}', phone_number):
        new_number = '+81-' + random_phone_number(1) + '-' + random_phone_number(4) + '-' + random_phone_number(4)
    elif re.match(r'\(0\d{1,4}\)[-]?\d{1,4}[-]?\d{4}', phone_number):
        new_number = re.sub(r'\D', '', phone_number)  # Remove non-digit characters
        new_number = '(' + new_number[:5] + ')' + new_number[5:]
    elif re.match(r'0\d{1,4}[-]?\d{1,4}[-]?\d{4}', phone_number):
        new_number = '0' + re.sub(r'\D', '', phone_number)  # Remove non-digit characters
    else:
        new_number = phone_number  # This should not happen with the given pattern
 
    return new_number


# PHONE_NUMBER_INDIA
# def generate_new_indian_phone_number(mobile_number):
#     cleaned_number = mobile_number.strip().replace(" ", "")
#     cleaned_number = mobile_number.strip().replace("-", "")
#     country_code = "+91"

#     if cleaned_number.startswith(country_code):
#         initial_digit = cleaned_number[3]
#     else:
#         initial_digit = cleaned_number[0]

#     remaining_digits = "".join([str(random.randint(0, 9)) for _ in range(9)])

#     new_mobile_number = f"{country_code} {initial_digit}{remaining_digits[:4]}-{remaining_digits[4:]}"
#     return new_mobile_number

def random_phone_number(length):
    return ''.join(random.choices('0123456789', k=length))

def generate_new_indian_phone_number(phone_number):
    india_pattern = r'(\+91[-\s]?\d{5}[-\s]?\d{5})|(\+91\d{10})|(\(91\)\d{10})|(0\d{10})|(0\d{2}[-\s]?\d{7})'
    match = re.match(india_pattern, phone_number)
    if not match:
        raise ValueError("Input is not a valid Indian phone number")
 
    if re.match(r'\+91[-\s]?\d{5}[-\s]?\d{5}', phone_number):
        new_number = '+91-' + random_phone_number(5) + '-' + random_phone_number(5)
    elif re.match(r'\+91\d{10}', phone_number):
        new_number = '+91-' + random_phone_number(10)
    elif re.match(r'\(91\)\d{10}', phone_number):
        new_number = '(91)' + random_phone_number(10)
    elif re.match(r'0\d{10}', phone_number):
        new_number = '0' + random_phone_number(10)
    elif re.match(r'0\d{2}[-\s]?\d{7}', phone_number):
        parts = re.split(r'[-\s]', phone_number)
        new_number = '0' + parts[0][1:] + '-' + random_phone_number(len(parts[1]))
    else:
        new_number = phone_number  # This should not happen with the given pattern
 
    return new_number


# CARD_NUMBER

def generate_new_card_number(card_number):
    # Change the last 6 digits of the card number to random digits
    count = 0
    n = len(card_number)

    for i in range(len(card_number)):
        char = card_number[n-1-i]
        if char.isdigit():
            # Replace digit with random digit from 0 to 9
            card_number = card_number[:n-1-i] + str(random.randint(0, 9)) + card_number[n-i:]
            count += 1

        if count == 7:
            break

    return card_number

# MAC ADDRESS
def generate_random_mac(mac_address):
    # Extract the separator used in the input MAC address
    separator = ':' if ':' in mac_address else '-'

    # Split the input MAC address into parts based on the separator
    parts = mac_address.split(separator)

    # Generate new random hexadecimal digits for each part
    new_parts = [f"{random.randint(0, 255):02X}" for _ in range(len(parts))]

    # Join the new parts with the original separator
    new_mac_address = separator.join(new_parts)

    return new_mac_address

# ADHAR

def generate_random_adhar(pattern):
    # Generate random digits for Aadhar number parts
    part1 = f"{random.randint(0, 9999):04}"
    part2 = f"{random.randint(0, 9999):04}"
    part3 = f"{random.randint(0, 9999):04}"

    # Choose a random separator (either '-' or ' ')
    separator = random.choice(['-', ' '])

    # Format the Aadhar number
    new_adhar_number = f"{part1}{separator}{part2}{separator}{part3}"

    return new_adhar_number

# PAN NUMBER

def generate_random_pan_number(pattern):
    # Generate random uppercase letters
    letters = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5))

    # Generate random digits (0-9)
    digits = ''.join(random.choice('0123456789') for _ in range(4))

    # Generate a random uppercase letter for the last character
    last_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Format the PAN number
    new_pan_number = f"{letters}{digits}{last_char}"

    return new_pan_number

# TIME

def generate_random_time(input_time):
    # Define the regex pattern to match time
    regex_pattern = r"\b(1[0-2]|0?[1-9]):[0-5][0-9]\s*(AM|PM|am|pm)?\b"

    # Validate if the input matches the pattern
    if not re.fullmatch(regex_pattern, input_time):
        return input_time

    # Parse the input time
    match = re.match(r"(\d{1,2}):([0-5][0-9])\s*(AM|PM|am|pm)?", input_time)
    if not match:
        return input_time

    hour = int(match.group(1))
    minute = match.group(2)
    am_pm = match.group(3)

    # Generate a new hour (random between 1 and 12)
    new_hour = random.randint(1, 12)

    # Generate a new minute (random between 0 and 59)
    new_minute = random.randint(0, 59)

    # Construct the new time string in the same pattern
    if am_pm is not None:
        new_time = f"{new_hour:02}:{new_minute:02} {am_pm}"
    else:
        new_time = f"{new_hour:02}:{new_minute:02}"

    return new_time


###############POSTAL CODE##########################################

import string

def generate_random_Indian_pin(original_pin):
    # Validate that the original PIN is a 6-digit number
    if not (original_pin.isdigit() and len(original_pin) == 6):
        return original_pin

    # Extract parts of the original PIN
    first_digit = original_pin[0]
    second_digit = original_pin[1]
    third_digit = original_pin[2]

    # Generate the new random last three digits
    last_three_digits = f"{random.randint(0, 999):03d}"

    # Combine to form the new PIN
    new_pin = first_digit + second_digit + third_digit + last_three_digits

    return new_pin

def generate_random_japan_pin(original_pin):
    # Validate that the original PIN is in the format NNN-NNNN
    if not (original_pin.isdigit() and len(original_pin) == 7):
        return original_pin

    # Extract the first three digits (regional code) from the original PIN
    regional_code = original_pin[:3]

    # Generate the new random last four digits
    last_four_digits = f"{random.randint(0, 9999):04d}"

    # Combine to form the new PIN
    new_pin = regional_code + last_four_digits

    return new_pin



def generate_random_US_pin(original_pin):
    # Define the regex pattern for validation
    pattern = re.compile(r"\b\d{5}(-\d{4})?\b")

    # Validate that the original PIN matches the pattern
    if not pattern.fullmatch(original_pin):
        return original_pin

    # Generate the random 5-digit part
    first_part = f"{random.randint(0, 99999):05d}"

    # Check if the original PIN has the optional 4-digit part
    if '-' in original_pin:
        second_part = f"{random.randint(0, 9999):04d}"
        new_pin = first_part + '-' + second_part
    else:
        new_pin = first_part

    return new_pin


def generate_random_canada_pin(original_pin):
    # Define the regex pattern for validation
    pattern = re.compile(r"\b[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d\b")

    # Validate that the original PIN matches the pattern
    if not pattern.fullmatch(original_pin):
        return original_pin

    # Helper functions to generate random letter and digit
    def random_letter():
        return random.choice(string.ascii_uppercase)

    def random_digit():
        return random.choice(string.digits)

    # Generate the random PIN following the same pattern
    new_pin = (
        random_letter() +
        random_digit() +
        random_letter() +
        " " +
        random_digit() +
        random_letter() +
        random_digit()
    )

    return new_pin