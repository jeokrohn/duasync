user_data = ['Adrienne', 'Alvarado', 'aalvarad',
             'Beatrice', 'Rich', 'brich',
             'Rahim', 'Kaufman', 'rkaufman',
             'Ciaran', 'Martinez', 'cmartine',
             'Kameko', 'Savage', 'ksavage',
             'Ori', 'Harrington', 'oharring',
             'Judah', 'Flynn', 'jflynn',
             'Malachi', 'Tyson', 'mtyson',
             'Justina', 'May', 'jmay',
             'Roth', 'Bridges', 'rbridges',
             'Ira', 'Mcclure', 'imcclure',
             'Rosalyn', 'Griffith', 'rgriffit',
             'Hilda', 'Rice', 'hrice',
             'Elton', 'William', 'ewilliam',
             'Darius', 'Brown', 'dbrown',
             'Stacy', 'Parker', 'sparker',
             'Otto', 'Brown', 'obrown',
             'Leandra', 'Cannon', 'lcannon',
             'Molly', 'Wells', 'mwells',
             'Cameron', 'Baker', 'cbaker',
             'Stella', 'Solis', 'ssolis',
             'Laith', 'Morse', 'lmorse',
             'Willa', 'Figueroa', 'wfiguero',
             'Aretha', 'Mcintosh', 'amcintos',
             'Kathleen', 'Carney', 'kcarney',
             'Jin', 'Burch', 'jburch',
             'Norman', 'Hampton', 'nhampton',
             'Olympia', 'Stone', 'ostone',
             'Nevada', 'Whitaker', 'nwhitake',
             'Garth', 'Fulton', 'gfulton',
             'Claire', 'Mcgowan', 'cmcgowan',
             'Brenda', 'Sharp', 'bsharp',
             'Malcolm', 'Bush', 'mbush',
             'Adena', 'Villarreal', 'avillarr',
             'Nichole', 'Jefferson', 'njeffers',
             'Colette', 'Spencer', 'cspencer',
             'Amber', 'Kent', 'akent',
             'Winter', 'Shannon', 'wshannon',
             'Charles', 'Ratliff', 'cratliff',
             'Summer', 'Mcintyre', 'smcintyr',
             'Warren', 'Clay', 'wclay',
             'Cyrus', 'Adams', 'cadams',
             'Jenette', 'Sykes', 'jsykes',
             'Kelly', 'Robles', 'krobles',
             'Jocelyn', 'Brown', 'jbrown',
             'Cailin', 'Holloway', 'chollowa',
             'Yasir', 'Mcdonald', 'ymcdonal',
             'Chancellor', 'Bauer', 'cbauer',
             'Halla', 'Meyer', 'hmeyer',
             'Jayme', 'Morse', 'jmorse']

# read a gmail address from a file
# this gmail address is used as a template to create the email addresses for the test users so that all Webex emails
# for these user get sent to the main gmail account
with open('gmail', 'r') as f:
    gmail_address = f.readline().strip()

class TestUser:
    def __init__(self, first, last, email):
        self._first = first
        self._last = last
        if '@' not in email:
            lhs, rhs = gmail_address.split('@')
            email = f'{lhs}+du1-{email}@{rhs}'
        self._email = email

    @property
    def first(self):
        return self._first

    @property
    def last(self):
        return self._last

    @property
    def email(self):
        return self._email

    @property
    def display_name(self):
        return f'{self.first} {self.last}'

    def __repr__(self):
        return f'{self.first} {self.last} ({self.email})'


def testusers():
    """
    Generator for test users
    :return: yields TestUser instance
    """
    i = iter(user_data)
    for first in i:
        last = next(i)
        id = next(i)
        yield TestUser(first, last, id)


def display_name(u):
    return f'{u[0]} {u[1]}'
