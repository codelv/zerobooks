"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the AGPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from datetime import datetime
from uuid import uuid4

from atom.api import Enum, Int, Str, Typed
from atomdb.sql import SQLModel


class Address(SQLModel):
    COUNTRIES = {
        "AD": "Andorra",
        "AE": "United Arab Emirates",
        "AF": "Afghanistan",
        "AG": "Antigua & Barbuda",
        "AI": "Anguilla",
        "AL": "Albania",
        "AM": "Armenia",
        "AN": "Netherlands Antilles",
        "AO": "Angola",
        "AQ": "Antarctica",
        "AR": "Argentina",
        "AS": "American Samoa",
        "AT": "Austria",
        "AU": "Australia",
        "AW": "Aruba",
        "AZ": "Azerbaijan",
        "BA": "Bosnia and Herzegovina",
        "BB": "Barbados",
        "BD": "Bangladesh",
        "BE": "Belgium",
        "BF": "Burkina Faso",
        "BG": "Bulgaria",
        "BH": "Bahrain",
        "BI": "Burundi",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BN": "Brunei Darussalam",
        "BO": "Bolivia",
        "BR": "Brazil",
        "BS": "Bahama",
        "BT": "Bhutan",
        "BV": "Bouvet Island",
        "BW": "Botswana",
        "BY": "Belarus",
        "BZ": "Belize",
        "CA": "Canada",
        "CC": "Cocos (Keeling) Islands",
        "CF": "Central African Republic",
        "CG": "Congo",
        "CH": "Switzerland",
        "CI": "Côte D'ivoire (Ivory Coast)",
        "CK": "Cook Iislands",
        "CL": "Chile",
        "CM": "Cameroon",
        "CN": "China",
        "CO": "Colombia",
        "CR": "Costa Rica",
        "CS": "Czechoslovakia (no longer exists)",
        "CU": "Cuba",
        "CV": "Cape Verde",
        "CX": "Christmas Island",
        "CY": "Cyprus",
        "CZ": "Czech Republic",
        "DE": "Germany",
        "DJ": "Djibouti",
        "DK": "Denmark",
        "DM": "Dominica",
        "DO": "Dominican Republic",
        "DZ": "Algeria",
        "EC": "Ecuador",
        "EE": "Estonia",
        "EG": "Egypt",
        "EH": "Western Sahara",
        "ER": "Eritrea",
        "ES": "Spain",
        "ET": "Ethiopia",
        "FI": "Finland",
        "FJ": "Fiji",
        "FK": "Falkland Islands (Malvinas)",
        "FM": "Micronesia",
        "FO": "Faroe Islands",
        "FR": "France",
        "FX": "France, Metropolitan",
        "GA": "Gabon",
        "GB": "United Kingdom (Great Britain)",
        "GD": "Grenada",
        "GE": "Georgia",
        "GF": "French Guiana",
        "GH": "Ghana",
        "GI": "Gibraltar",
        "GL": "Greenland",
        "GM": "Gambia",
        "GN": "Guinea",
        "GP": "Guadeloupe",
        "GQ": "Equatorial Guinea",
        "GR": "Greece",
        "GS": "South Georgia and the South Sandwich Islands",
        "GT": "Guatemala",
        "GU": "Guam",
        "GW": "Guinea-Bissau",
        "GY": "Guyana",
        "HK": "Hong Kong",
        "HM": "Heard & McDonald Islands",
        "HN": "Honduras",
        "HR": "Croatia",
        "HT": "Haiti",
        "HU": "Hungary",
        "ID": "Indonesia",
        "IE": "Ireland",
        "IL": "Israel",
        "IN": "India",
        "IO": "British Indian Ocean Territory",
        "IQ": "Iraq",
        "IR": "Islamic Republic of Iran",
        "IS": "Iceland",
        "IT": "Italy",
        "JM": "Jamaica",
        "JO": "Jordan",
        "JP": "Japan",
        "KE": "Kenya",
        "KG": "Kyrgyzstan",
        "KH": "Cambodia",
        "KI": "Kiribati",
        "KM": "Comoros",
        "KN": "St. Kitts and Nevis",
        "KP": "Korea, Democratic People's Republic of",
        "KR": "Korea, Republic of",
        "KW": "Kuwait",
        "KY": "Cayman Islands",
        "KZ": "Kazakhstan",
        "LA": "Lao People's Democratic Republic",
        "LB": "Lebanon",
        "LC": "Saint Lucia",
        "LI": "Liechtenstein",
        "LK": "Sri Lanka",
        "LR": "Liberia",
        "LS": "Lesotho",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "LV": "Latvia",
        "LY": "Libyan Arab Jamahiriya",
        "MA": "Morocco",
        "MC": "Monaco",
        "MD": "Moldova, Republic of",
        "MG": "Madagascar",
        "MH": "Marshall Islands",
        "ML": "Mali",
        "MN": "Mongolia",
        "MM": "Myanmar",
        "MO": "Macau",
        "MP": "Northern Mariana Islands",
        "MQ": "Martinique",
        "MR": "Mauritania",
        "MS": "Monserrat",
        "MT": "Malta",
        "MU": "Mauritius",
        "MV": "Maldives",
        "MW": "Malawi",
        "MX": "Mexico",
        "MY": "Malaysia",
        "MZ": "Mozambique",
        "NA": "Namibia",
        "NC": "New Caledonia",
        "NE": "Niger",
        "NF": "Norfolk Island",
        "NG": "Nigeria",
        "NI": "Nicaragua",
        "NL": "Netherlands",
        "NO": "Norway",
        "NP": "Nepal",
        "NR": "Nauru",
        "NU": "Niue",
        "NZ": "New Zealand",
        "OM": "Oman",
        "PA": "Panama",
        "PE": "Peru",
        "PF": "French Polynesia",
        "PG": "Papua New Guinea",
        "PH": "Philippines",
        "PK": "Pakistan",
        "PL": "Poland",
        "PM": "St. Pierre & Miquelon",
        "PN": "Pitcairn",
        "PR": "Puerto Rico",
        "PT": "Portugal",
        "PW": "Palau",
        "PY": "Paraguay",
        "QA": "Qatar",
        "RE": "Réunion",
        "RO": "Romania",
        "RU": "Russian Federation",
        "RW": "Rwanda",
        "SA": "Saudi Arabia",
        "SB": "Solomon Islands",
        "SC": "Seychelles",
        "SD": "Sudan",
        "SE": "Sweden",
        "SG": "Singapore",
        "SH": "St. Helena",
        "SI": "Slovenia",
        "SJ": "Svalbard & Jan Mayen Islands",
        "SK": "Slovakia",
        "SL": "Sierra Leone",
        "SM": "San Marino",
        "SN": "Senegal",
        "SO": "Somalia",
        "SR": "Suriname",
        "ST": "Sao Tome & Principe",
        "SV": "El Salvador",
        "SY": "Syrian Arab Republic",
        "SZ": "Swaziland",
        "TC": "Turks & Caicos Islands",
        "TD": "Chad",
        "TF": "French Southern Territories",
        "TG": "Togo",
        "TH": "Thailand",
        "TJ": "Tajikistan",
        "TK": "Tokelau",
        "TM": "Turkmenistan",
        "TN": "Tunisia",
        "TO": "Tonga",
        "TP": "East Timor",
        "TR": "Turkey",
        "TT": "Trinidad & Tobago",
        "TV": "Tuvalu",
        "TW": "Taiwan, Province of China",
        "TZ": "Tanzania, United Republic of",
        "UA": "Ukraine",
        "UG": "Uganda",
        "UM": "United States Minor Outlying Islands",
        "US": "United States of America",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VA": "Vatican City State (Holy See)",
        "VC": "St. Vincent & the Grenadines",
        "VE": "Venezuela",
        "VG": "British Virgin Islands",
        "VI": "United States Virgin Islands",
        "VN": "Viet Nam",
        "VU": "Vanuatu",
        "WF": "Wallis & Futuna Islands",
        "WS": "Samoa",
        "YE": "Yemen",
        "YT": "Mayotte",
        "YU": "Yugoslavia",
        "ZA": "South Africa",
        "ZM": "Zambia",
        "ZR": "Zaire",
        "ZW": "Zimbabwe",
    }

    STATES = {
        "AK": "Alaska",
        "AL": "Alabama",
        "AR": "Arkansas",
        "AZ": "Arizona",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DC": "District of Columbia",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "IA": "Iowa",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "MA": "Massachusetts",
        "MD": "Maryland",
        "ME": "Maine",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MO": "Missouri",
        "MS": "Mississippi",
        "MT": "Montana",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "NE": "Nebraska",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NV": "Nevada",
        "NY": "New York",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VA": "Virginia",
        "VT": "Vermont",
        "WA": "Washington",
        "WI": "Wisconsin",
        "WV": "West Virginia",
        "WY": "Wyoming",
    }

    #: Address ID
    id = Int().tag(primary_key=True)

    #: UUID
    uuid = Str(factory=lambda: str(uuid4().hex)).tag(length=36, unique=True)

    #: Street
    street = Str().tag(length=255)

    #: City
    city = Str().tag(length=255)

    #: States
    state = Enum("", *STATES.keys()).tag(length=2)

    #: Zipcodes
    zipcode = Str().tag(length=10)

    #: Countries
    country = Enum("", *COUNTRIES.keys()).tag(length=3)

    def _default_country(self):
        return "US"

    #: Dates
    created = Typed(datetime, factory=datetime.now)
    updated = Typed(datetime, factory=datetime.now)

    class Meta:
        db_table = "address"