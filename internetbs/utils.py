import faker

faker_instance = faker.Faker('en_US')

def make_fake_contact_data_with_email(email):
    """
        <contactType>_<contactField>

        Valid values for contactType are:
        Registrant
        Admin
        Technical
        Billing

        For each contactType the following contactFields are mandatory:
        FirstName
        LastName
        Email
        PhoneNumber
        Street
        City
        CountryCode
        PostalCode
    """
    fake_data = {
        'FirstName' : faker_instance.first_name(),
        'LastName' : faker_instance.last_name(),
        'PhoneNumber' : "+1.2025550129", # totally fake
        'Email' : email,
        'Street' : faker_instance.street_address(),
        'City' : faker_instance.city(),
        'CountryCode' : faker_instance.country_code(),
        'PostalCode' : faker_instance.postalcode()
    }

    types = {
        'Registrant',
        'Admin',
        'Technical',
        'Billing'
    }
    result = {}

    for contactType in types:
        for field in fake_data.keys():
            key = '_'.join([contactType, field])
            result[key] = fake_data[field]

    return result