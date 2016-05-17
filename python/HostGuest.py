
from util import *

class HostSpot(object):
    def __init__(self, host_id_num0, host_spot_id_num0):
        self.host_id_num=host_id_num0
        self.host_spot_id_num=host_spot_id_num0
    
    def __str__(self):
        ans = '''
Host Spot:
    Host's ID Number: '''+str(self.host_id_num)+'''
    This Spot's ID Number: '''+str(self.host_spot_id_num)+'''
'''
        return ans
    
    def __repr__(self):
        ans = ''+ \
            '''HostSpot('''+ \
                '''host_id_num0='''+self.host_id_num.__repr__()+''', '''+ \
                '''host_spot_id_num0='''+self.host_spot_id_num.__repr__()+''', '''+ \
            ''')'''
        return ans

class Host(object):
    def __init__(self, name0='NO_NAME', email0='NO_EMAIL', phone_number0='', days_housing_is_available0=frozenset(['Friday', 'Saturday', 'Sunday']), has_cats0=False, has_dogs0=False, willing_to_house_smokers0=True, willing_to_provide_rides0=True, late_night_tendencies0="survivors' club", preferred_house_guests0=[], num_spots_available0=0, misc_info0='', id_num0=-1):
        self.name=name0
        self.email=email0
        self.phone_number=phone_number0 # is a string
        self.days_housing_is_available=days_housing_is_available0 # is a frozenset
        self.has_cats=has_cats0
        self.has_dogs=has_dogs0
        self.willing_to_house_smokers=willing_to_house_smokers0
        self.willing_to_provide_rides=willing_to_provide_rides0
        self.late_night_tendencies=late_night_tendencies0 # is a string, one of "early sleeper", "some late night", or "survivors' club".
        self.preferred_house_guests=preferred_house_guests0
        self.num_spots_available=num_spots_available0
        self.misc_info=misc_info0 # is a string
        self.id_num=id_num0 if id_num0!=-1 else generate_unique_identifier()
        assertion(len(self.days_housing_is_available)>0, 'Hosts must have at least one day of housing available.')
    
    def __str__(self):
        ans = '''
Host:
    ID Number: '''+str(self.id_num)+'''
    Name: '''+self.name+'''
    Email: '''+self.email+'''
    Phone Number: '''+self.phone_number+'''
    Days Housing Is Available: '''+(('Friday, ' if 'Friday' in self.days_housing_is_available else '')+('Saturday, ' if 'Saturday' in self.days_housing_is_available else '')+('Sunday, ' if 'Sunday' in self.days_housing_is_available else ''))[:-2]+'''
    Has Cats: '''+('Yes' if self.has_cats else 'No')+'''
    Has Dogs: '''+('Yes' if self.has_dogs else 'No')+'''
    Willing to House Smokers: '''+('Yes' if self.willing_to_house_smokers else 'No')+''' 
    Willing to Provide Rides: '''+('Yes' if self.willing_to_provide_rides else 'No')+'''
    Late Night Tendencies: '''+self.late_night_tendencies+'''
    Preferred House Guests: '''+', '.join(sorted(list(set([guest.name for guest in guests if guest.id_num in self.preferred_house_guests]))))+'''
    Number of Spots Available: '''+str(self.num_host_spots_available)+'''
    Misc. Info.: '''+self.misc_info+'''
'''
        return ans
    
    def __repr__(self):
        ans = ''+ \
            '''Host('''+ \
                '''name0='''+self.name.__repr__()+''', '''+ \
                '''email0='''+self.email.__repr__()+''', '''+ \
                '''phone_number0='''+self.phone_number.__repr__()+''', '''+ \
                '''days_housing_is_available0='''+self.days_housing_is_available.__repr__()+''', '''+ \
                '''has_cats0='''+self.has_cats.__repr__()+''', '''+ \
                '''has_dogs0='''+self.has_dogs.__repr__()+''', '''+ \
                '''willing_to_house_smokers0='''+self.willing_to_house_smokers.__repr__()+''', '''+ \
                '''willing_to_provide_rides0='''+self.willing_to_provide_rides.__repr__()+''', '''+ \
                '''late_night_tendencies0='''+self.late_night_tendencies.__repr__()+''', '''+ \
                '''preferred_house_guests0='''+self.preferred_house_guests.__repr__()+''', '''+ \
                '''num_spots_available0='''+self.num_spots_available.__repr__()+''', '''+ \
                '''misc_info0='''+self.misc_info.__repr__()+''', '''+ \
                '''id_num0='''+self.id_num.__repr__()+ \
            ''')'''
        return ans

class Guest(object):
    def __init__(self, name0='NO_NAME', email0='NO_EMAIL', phone_number0='', days_housing_is_needed0=frozenset(['Friday', 'Saturday', 'Sunday']), can_be_around_cats0=True, can_be_around_dogs0=True, smokes0=False, has_ride0=True, late_night_tendencies0="survivors' club", preferred_house_guests0=[], misc_info0='', id_num0=-1):
        self.name=name0
        self.email=email0
        self.phone_number=phone_number0 # is a string
        self.days_housing_is_needed=days_housing_is_needed0 # is a frozenset
        self.can_be_around_cats=can_be_around_cats0
        self.can_be_around_dogs=can_be_around_dogs0
        self.smokes=smokes0
        self.has_ride=has_ride0
        self.late_night_tendencies=late_night_tendencies0 # is a string
        self.preferred_house_guests=preferred_house_guests0
        self.misc_info=misc_info0 # is a string
        self.id_num=id_num0 
        assertion(len(self.days_housing_is_needed)>0, 'Guests must require at least one day of needed housing.')
    
    def __str__(self):
        ans = '''
Guest:
    ID Number: '''+str(self.id_num)+'''
    Name: '''+self.name+'''
    Email: '''+self.email+'''
    Phone Number: '''+self.phone_number+'''
    Days Housing Is Needed: '''+(('Friday, ' if 'Friday' in self.days_housing_is_needed else '')+('Saturday, ' if 'Saturday' in self.days_housing_is_needed else '')+('Sunday, ' if 'Sunday' in self.days_housing_is_needed else ''))[:-2]+'''
    Allergic to Cats: '''+('Yes' if not self.can_be_around_cats else 'No')+'''
    Allergic to Dogs: '''+('Yes' if not self.can_be_around_dogs else 'No')+'''
    Smokes: '''+('Yes' if self.smokes else 'No')+''' 
    Needs Transportation: '''+('Yes' if not self.has_ride else 'No')+'''
    Late Night Tendencies: '''+self.late_night_tendencies+'''
    Preferred Hosts: '''+', '.join(sorted(list(set([host.name for host in hosts if host.id_num in self.preferred_house_guests]))))+'''
    Preferred Fellow House Guests: '''+', '.join(sorted(list(set([guest.name for guest in guests if guest.id_num != self.id_num and guest.id_num in self.preferred_house_guests]))))+'''
    Misc. Info.: '''+self.misc_info+'''
'''
        return ans
    
    def __repr__(self):
        ans = ''+ \
            '''Guest('''+ \
                '''name0='''+self.name.__repr__()+''', '''+ \
                '''email0='''+self.email.__repr__()+''', '''+ \
                '''phone_number0='''+self.phone_number.__repr__()+''', '''+ \
                '''days_housing_is_needed0='''+self.days_housing_is_needed.__repr__()+''', '''+ \
                '''can_be_around_cats0='''+self.can_be_around_cats.__repr__()+''', '''+ \
                '''can_be_around_dogs0='''+self.can_be_around_dogs.__repr__()+''', '''+ \
                '''smokes0='''+self.smokes.__repr__()+''', '''+ \
                '''has_ride0='''+self.has_ride.__repr__()+''', '''+ \
                '''late_night_tendencies0='''+self.late_night_tendencies.__repr__()+''', '''+ \
                '''preferred_house_guests0='''+self.preferred_house_guests.__repr__()+''', '''+ \
                '''misc_info0='''+self.misc_info.__repr__()+''', '''+ \
                '''id_num0='''+self.id_num.__repr__()+ \
            ''')'''
        return ans

def are_compatible(host, guest):
    # Check if the days housing is needed is a subset of days housing is available
    if not guest.days_housing_is_needed.issubset(host.days_housing_is_available): 
        return False
    
    # Cat compatibility
    if not guest.can_be_around_cats: 
        if host.has_cats:
            return False
    
    # Dog compatibility
    if not guest.can_be_around_dogs: 
        if host.has_dogs:
            return False
    
    # Smoking compatibility
    if guest.smokes:
        if not host.willing_to_house_smokers:
            return False
    
    # Rides
    if not guest.has_ride:
        if not host.willing_to_provide_rides:
            return False
    
    return True

