from atom.api import Atom, Property, Instance, Enum, Unicode, List, Dict

class Model(Atom):
    pass

class System(Model):
    """ System configuration
    
    """
    _instance = None
    
    @classmethod
    def instance(cls):
        return cls._instance or cls()
    
    def __init__(self, *args, **kwargs):
        if System._instance is not None:
            raise RuntimeError("Only one System may exist")
        System._instance = self
        super(System, self).__init__(*args, **kwargs)
        
    name_prefixes = Dict(str, str, default={
        '1Lt.': 'First Lieutenant: Army',
        '1stLt.': 'First Lieutenant: Air Force, Marine Corps',
        '2Lt.': 'Second Lieutenant: Army',
        '2ndLt.': 'Second Lieutenant: Air Force, Marine Corps',
        'Amb.': 'Ambassador',
        'Amb. & Mrs.': 'Ambassador and',
        'BG': 'Brigadier General: Army',
        'BGen.': 'Brigadier General: Air Force',
        'BrigGen.': 'Brigadier General: Marine Corps',
        'Brother': 'Brotherhood, Catholic',
        'CAPT': 'Captain: Navy, Coast Guard',
        'CDR': 'Commander: Navy, Coast Guard',
        'COL': 'Colonel: Army',
        'CPT': 'Captain: Army',
        'Capt.': 'Captain: Air Force, Marine Corps',
        'Capt. & Mrs.': 'Captain and Mrs.: USAF, USMC',
        'Col.': 'Colonel: Air Force, Marine Corps',
        'Col. & Mrs.': 'Colonel & Mrs.: USAF, USMC',
        'Dean': 'Dean: College or University',
        'Dr.': 'Anyone with doctorate',
        'Dr. & Mrs.': 'Doctor & Mrs.',
        'Drs.': 'Doctors',
        'ENS': 'Ensign: Navy, Coast Guard',
        'Est. of': 'Estate of',
        'GEN': 'General: Army',
        'Gen.': 'General: Air Force, Marine Corps',
        'Gen. & Mrs.': 'General and Mrs.',
        'Gov.': 'Governor',
        'Hon.': 'Judge',
        'Hon. & Mrs.': 'Judge and Mrs.',
        'Justice': 'Supreme Court, Associate Justice',
        'LCDR': 'Lieutenant Commander: Navy, Coast Guard',
        'LCDR & Mrs.': 'Lieutenant Commander & Mrs.: USN, USCG',
        'LCpl': 'Lance Corporal: Marines',
        'LT': 'Lieutenant: Army',
        'LTC': 'Lieutenant Colonel: Army',
        'LTG': 'Lieutenant General: Army',
        'LTJG': 'Lieutenant Junior Grade: Navy, Coast Guard',
        'Lt.': 'Lieutenant: Air Force, Marine Corps',
        'LtCol.': 'Lieutenant Colonel: Air Force, Marine Corps',
        'LtGen.': 'Lieutenant General: Air Force, Marines',
        'MAJ': 'Major: Army',
        'MG': 'Major General: Army',
        'MSG': 'Master Sergeant: Army',
        'MSgt.': 'Master Sergeant: Air Force, Marine Corps',
        'Maj.': 'Major: Air Force, Marine Corps',
        'MajGen.': 'Major General: Air Force, Marine Corps',
        'Mayor': 'Mayor',
        'Mdme.': 'Madame: foreign female',
        'Miss': 'Female, unmarried',
        'Mr.': 'Male',
        'Mr. & Dr.': 'Mister and Doctor',
        'Mr. & Mrs.': 'Married: male and female',
        'Mrs.': 'Female, married or widowed',
        'Ms.': 'Female',
        'Msgr.': 'Monsignor',
        'Prince': 'Prince',
        'Prof.': 'Professor: College or University',
        'Prof. & Mrs.': 'Professor and female',
        'RADM': 'Rear Admiral: Navy',
        'RT. REV.': 'Right Reverend',
        'Rabbi': 'Rabbi',
        'Rev.': 'Clergy: Protestant',
        'Rev. & Mrs.': 'Married clergy: Protestant',
        'Rev. Dr .': 'Clergy with Doctorate: Protestant',
        'Rev. Dr. & Mrs.': 'Married clergy with doctorate: Protestant',
        'Rev. Father': 'Priest',
        'Senator': 'Senator',
        'Sir': 'Sir',
        'Sister': 'Member of Sisterhood'
    })
    
    #: Accepted name suffixes
    name_suffixes = Dict(str, str, default={
        'B.V.M.': 'Blessed Virgin Mary',
        'CFRE': 'Certified Fund Raising Executive',
        'CLU': 'Chartered Life Underwriter',
        'CPA': 'Certified Public Accountant',
        'C.S.C.': 'Congregation of Holy Cross',
        'C.S.J.': 'Sisters of St. Joseph',
        'D.C.': 'Doctor of Chiropractic',
        'D.D.': 'Doctor of Divinity',
        'D.D.S.': 'Doctor of Dental Surgery',
        'D.M.D.': 'Doctor of Dental Medicine',
        'D.O.': 'Doctor of Osteopathy',
        'D.V.M.': 'Doctor of Veterinary Medicine',
        'Ed.D.': 'Doctor of Education',
        'Esq.': 'Esquire',
        'II': 'The Second',
        'III': 'The Third',
        'IV': 'The Fourth',
        'Inc.': 'Incorporated',
        'J.D.': 'Juris Doctor',
        'Jr.': 'Junior',
        'LL.D.': 'Doctor of Laws',
        'Ltd.': 'Limited',
        'M.D.': 'Doctor of Medicine',
        'O.D.': 'Doctor of Optometry',
        'O.S.B.': 'Order of St Benedict',
        'P.C.': 'Past Commander, Police Constable, Post Commander',
        'P.E.': 'Protestant Episcopal',
        'Ph.D.': 'Doctor of Philosophy',
        'Ret.': 'Retired',
        'R.G.S': 'Sisters of Our Lady of Charity of the Good Shepherd',
        'R.N.': 'Registered Nurse',
        'R.N.C.': 'Registered Nurse Clinician',
        'S.H.C.J.': 'Society of Holy Child Jesus',
        'S.J.': 'Society of Jesus',
        'S.N.J.M.': 'Sisters of Holy Names of Jesus & Mary',
        'Sr.': 'Senior',
        'S.S.M.O.': 'Sister of Saint Mary Order',
        'USA': 'United States Army',
        'USAF': 'United States Air Force',
        'USAFR': 'United States Air Force Reserve',
        'USAR': 'United States Army Reserve',
        'USCG': 'United States Coast Guard',
        'USMC': 'United States Marine Corps',
        'USMCR': 'United States Marine Corps Reserve',
        'USN': 'United States Navy',
        'USNR': 'United States Navy Reserve',
    })
    
    #: US states
    states = List(str, default=[
        'PA'    
    ])
    
    #: Display name
    display_name_formats = List(str, default=[
        '{first_name} {last_name}',
        '{last_name}, {first_name}',
        '{title} {first_name} {last_name}',
        '{title} {first_name} {last_name} {suffix}',
        '{title} {last_name}',
    ])
    
    #: Terms
    invoice_terms = Dict(str, str, default={
        'PIA': 'Payment in advance',
        'Net 7': 'Payment seven days after invoice date',
        'Net 10': 'Payment ten days after invoice date',
        'Net 30': 'Payment 30 days after invoice date',
        'Net 60': 'Payment 60 days after invoice date',
        'Net 90': 'Payment 90 days after invoice date',
        'EOM': 'End of month',
        '21 MFI': '21st of the month following invoice date',
        '1% 10 Net 30': '1% discount if payment received within ten days otherwise payment 30 days after invoice date',
        'COD': 'Cash on delivery',
        'Cash account': 'Account conducted on a cash basis, no credit',
        'Letter of credit': 'A documentary credit confirmed by a bank, often used for export',
        'Bill of exchange': 'A promise to pay at a later date, usually supported by a bank',
        'CND': 'Cash next delivery',
        'CBS': 'Cash before shipment',
        'CIA': 'Cash in advance',
        'CWO': 'Cash with order',
        '1MD': "Monthly credit payment of a full month's supply",
        '2MD': 'As above plus an extra calendar month',
        'Contra': 'Payment from the customer offset against the value of supplies purchased from the customer',
        'Stage payment': 'Payment of agreed amounts at stage',
    })
