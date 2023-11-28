from datetime import datetime

def calc_birthday(data):
        """
        The calc_birthday function takes a date object as input and returns the number of days until the next birthday.
        If today is your birthday, it will return 0.
        
        :param data: Pass the birth date of a person to the function
        :return: The number of days until the next birthday
        :doc-author: Trelent
        """
        today = datetime.now().date()
        birth_date = data
        if birth_date.month == 2 and birth_date.day == 29:
            future_birthday = datetime(year = today.year, month = 2, day = birth_date.day - int(bool(today.year%4))).date()    
            if future_birthday < today: 
                future_birthday = datetime(year = today.year + 1, month = 2, day = birth_date.day - int(bool((today.year+1)%4))).date()    
        else:
            future_birthday = datetime(year = today.year, month = birth_date.month, day = birth_date.day).date()
            if future_birthday < today:
                future_birthday = future_birthday.replace(year = today.year + 1)
        return (future_birthday - today).days
    
def next_seven_days(contacts):
    """
    The next_seven_days function takes a list of contacts and returns a list of contacts whose birthday is within the next seven days.
    
    
    :param contacts: Pass in the list of contacts
    :return: A list of contacts that have birthdays in the next seven days
    :doc-author: Trelent
    """
    list_contacts = []
    for contact in contacts:
        if calc_birthday(contact.birthday) <= 7:
            list_contacts.append(contact)
    return list_contacts
