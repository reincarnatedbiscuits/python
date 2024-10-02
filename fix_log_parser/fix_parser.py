-'''
    Author: Chris Lee

    TODOs:
        * PEP compliance (pylint, black, Flake8, isort, pep257, ruff)
        * tkinter or other UI for file selection
        * output format:
            * flat text / formatted text e.g., HTML format
            * Excel (will need pandas, xlsxwriter, xlwing, openpyxl)
                * will need to build a dictionary for header rows with count for fields that could repeat in a FIX log row
                * first row will be FIX tag
                * second row will be 
        * Excel formatting e.g., bold first line, border under header rows

'''


import os
import datetime

def parse_file():
    fix42dict = dict()
    fix44dict = dict()
    with open("C:\\temp\\python\\fix_parser\\fix.4.2.dictionary.txt") as fix42fixfile:
        for line in fix42fixfile:
            (key, val) = line.split('\t')
            fix42dict[key] = val.strip()
    print("imported FIX 4.2 dictionary")
    with open("C:\\temp\\python\\fix_parser\\fix.4.4.dictionary.txt") as fix44fixfile:
        for line in fix44fixfile:
            (key, val) = line.split('\t')
            fix44dict[key] = val.strip()
    print("imported FIX 4.4 dictionary")

    fields_that_could_repeat = ['76', '150']

    ''' FYI:
        Tag 30:
            Reuter Exchange Mnemonics (FIX 4.2), lookup table (FIX 4.4)

        Tag 65:
            Additional information about the security (e.g. preferred, warrants, etc.). Note also see SecurityType <167>.
            As defined in the NYSE Stock and bond Symbol Directory and in the AMEX Fitch Directory

        Tag 100:
            Reuter Exchange Mnemonics (FIX 4.2), lookup table (FIX 4.4)

        Tag 207:
            Reuter Exchange Mnemonics

        Tag 275:
            Reuter Exchange Mnemonics

        Tag 308:
            Reuter Exchange Mnemonics

    '''

    tags_returning_reteurs_exchange = ['30', '100', '207', '275', '308']

    reuters_exchange_mnemonics = {'Abidjan Stock Exchange': 'CI',
        'American Stock Exchange': 'A',
        'Amman Stock Exchange': 'AM',
        'AEX Options and Futures Exchange': 'E',
        'AEX Stock Exchange': 'AS',
        'Australian Stock Exchange': 'AX',
        'Bahrain Stock Exchange': 'BH',
        'Barcelona Stock Exchange - Floor Trading': 'BC',
        'Barcelona Stock Exchange - CATS Feed': 'MC',
        'Beirut Stock Exchange': 'BY',
        'Belfox': 'b',
        'Berlin Stock Exchange': 'BE',
        'Berne Stock Exchange': 'BN',
        'Bilbao Stock Exchange': 'BI',
        'BIVA Stock Exchange': 'BIV',
        'Bombay Stock Exchange': 'BO',
        'Boston Stock Exchange': 'B',
        'Botswana Share Market': 'BT',
        'Bremen Stock Exchange': 'BM',
        'Brussels Stock Exchange': 'BR',
        'Calcutta Stock Exchange': 'CL',
        'Canadian Ventures Exchange': 'V',
        'Channel Islands': 'CH',
        'Chicago Board Options Exchange': 'W',
        'Chicago Stock Exchange': 'MW',
        'Chile Electronic Exchange': 'CE',
        'Cincinnati Stock Exchange': 'C',
        'Colombo Stock Exchange': 'CM',
        'Copenhagen Stock Exchange': 'CO',
        'Dehli Stock Exchange': 'DL',
        'Doha Securities Market': 'QA',
        'Dubai Financial Market': 'DU',
        'Dusseldorf Stock Exchange': 'D',
        'Electronic Stock Exchange  of Venezuela': 'EB',
        'Eurex Germany (DTB)': 'd',
        'Eurex Switzerland (SFF)': 'Z',
        'Frankfurt Stock Exchange': 'F',
        'Fukuoka Stock Exchange': 'FU',
        'Ghana Stock Exchange': 'GH',
        'Hamburg Stock Exchange': 'H',
        'Hanover Stock Exchange': 'HA',
        'Helsinki Stock Exchange': 'HE',
        'Hong Kong Stock Exchange': 'HK',
        'Iceland Stock Exchange': 'IC',
        'Interbolsa (Portugal)': 'IN',
        'Irish Stock Exchange': 'I',
        'Istanbul Stock Exchange': 'IS',
        'Jakarta Stock Exchange': 'JK',
        'Japanese Securities Dealers Association (JASDAQ)': 'Q',
        'Johannesburg Stock Exchange': 'J',
        'Pakistan Stock Exchange (formerly Karachi Stock Exchange)': 'KA',
        'KASDAQ (Korea)': 'KQ',
        'Kazakhstan Stock Exchange': 'KZ',
        'Korea Stock Exchange': 'KS',
        'Kuala Lumpur Stock Exchange': 'KL',
        'Kuwait Stock Exchange': 'KW',
        'Kyoto Stock Exchange': 'KY',
        'Lagos Stock Exchange': 'LG',
        'Latin American Market in Spain (LATIBEX)': 'LA',
        'Le Nouveau Marche': 'LN',
        'Lima Stock Exchange': 'LM',
        'Lisbon Stock Exchange (Portugal)': 'LS',
        'London Stock Exchange': 'L',
        'Lusaka Stock Exchange': 'LZ',
        'Luxembourg Stock Exchange': 'LU',
        'Madras Stock Exchange': 'MD',
        'Madrid Stock Exchange - Floor Trading': 'MA',
        'Madrid Stock Exchange - CATS Feed': 'MC',
        'Malta Stock Exchange': 'MT',
        'Mauritius Stock Exchange': 'MZ',
        'Medellin Stock Excahnge': 'ML',
        'Mexican Stock Exchange': 'MX',
        'Milan Stock Exchange': 'MI',
        'MONEP Paris Stock Options': 'p',
        'Montreal Exchange': 'M',
        'Moscow Inter Bank Currency Exchange': 'MM',
        'Moscow Stock Exchange': 'MO',
        'Munich Stock Exchange': 'MU',
        'Muscat Stock Exchange': 'OM',
        'Namibia Stock Exchange': 'NM',
        'Nagoya Stock Exchange': 'NG',
        'Nairobi Stock Exchange': 'NR',
        'NASDAQ': 'O',
        'NASDAQ Dealers - Bulletin Board': 'OB',
        'NASDAQ Japan': 'OJ',
        'National Stock Exchange of India': 'NS',
        'New York Stock Exchange': 'N',
        'New Zealand Stock Exchange': 'NZ',
        'NewEx (Austria)': 'NW',
        'Occidente Stock Exchange': 'OD',
        'Osaka Stock Exchange': 'OS',
        'Oslo Stock Exchange': 'OL',
        'Pacific Stock Exchange': 'P',
        'Paris Stock Exchange': 'PA',
        'Philadelphia Stock Exchange': 'PH',
        'Philadelphia Stock Exchange Options': 'X',
        'Philippine Stock Exchange': 'PS',
        'Prague Stock Exchange': 'PR',
        'Pink Sheets (National Quotation Bureau)': 'PNK',
        'RASDAQ (Romania)': 'RQ',
        'Riga Stock Exchange': 'RI',
        'Rio de Janeiro OTC Stock Exchange (SOMA)': 'SO',
        'Russian Trading System': 'RTS',
        'Santiago Stock Exchange': 'SN',
        'Sao Paulo Stock Exchange': 'SA',
        'Sapporo Stock Exchange': 'SP',
        'Saudi Stock Exchange': 'SE',
        'SBI Stock Exchange (Sweden)': 'SBI',
        'Singapore Stock Exchange': 'SI',
        'Shanghai Stock Exchange': 'SS',
        'Shenzhen Stock Exchange': 'SZ',
        'Stockholm Stock Exchange': 'ST',
        'Stuttgart Stock Exchange': 'SG',
        'St. Petersburg Stock Exchange': 'PE',
        'Surabaya Stock Exchange': 'SU',
        'SWX Swiss Exchange': 'S',
        'Taiwan OTC Securities Exchange': 'TWO',
        'Taiwan Stock Exchange': 'TW',
        'Tallinn Stock Exchange': 'TL',
        'Tel Aviv Stock Exchange': 'TA',
        'Thailand Stock Exchange': 'BK',
        'Third Market': 'TH',
        'Tokyo Stock Exchange': 'T',
        'Toronto Options Exchange': 'K',
        'Toronto Stock Exchange': 'TO',
        'Tradepoint Stock Exchange': 'TP',
        'Tunis Stock Exchange': 'TN',
        'Ukraine PFTS': 'PFT',
        'Valencia Stock Exchange': 'VA',
        'Vilnus Stock Exchange': 'VL',
        'virt-x': 'VX',
        'Vienna Stock Exchange': 'VI',
        'Zimbabwe Stock Exchange': 'ZI',
        'American Stock Exchange Options': '1',
        'Chicago Mercantile Exchange (CME) Futures Exchange (LIFFE)': '2',
        'Jiway': '14',
        'International Securities Market Association(ISMA)': '15',
        'London International Financial': '3',
        'London Traded Options Market': '5',
        'MEFF Renta Variable': '16',
        'Montreal Exchange Options (MOE)': 'unknown',
        'New York Mercantile Exchange (NYMEX)':	'12',
        'None': '0',
        'Non-exchange-based Over The Counter Market': '11',
        'NYFIX Millennium': '13',
        'NYSE BBSS (broker booth system)': '10',
        'Pacific Stock Exchange Options (PAO)': '8',
        'POSIT': '4',
        'Stockholm Options Market': '17',
        'Vancouver Options Exchange (VAO)': '9',
        'MEFF Renta Variable': '??',
        'Stockholm Options Market':	'??'
        }

    iso3166_1_country_code = {}

    fix42fields = {
        '4': {
            'B': 'Buy', 
            'S': 'Sell',
            'X': 'Cross',
            'T': 'Trade'
        },
        '5': {
            'N': 'New',
            'C': 'Cancel',
            'R': 'Replace'
        },
        '13': {
            '1': 'per share',
            '2': 'percentage',
            '3': 'absolute'
        },
        '18': {
            '1': 'Not held',
			'2': 'Work',
			'3': 'Go along',
			'4': 'Over the day',
			'5': 'Held',
			'6': 'Participate don\'t initiate',
			'7': 'Strict scale',
			'8': 'Try to scale',
			'9': 'Stay on bidside',
			'0': 'Stay on offerside',
			'A': 'No cross (cross is forbidden)',
			'B': 'OK to cross',
			'C': 'Call first',
			'D': 'Percent of volume \'(indicates that the sender does not want to be all of the volume on the floor vs. a specific percentage)\'',
			'E': 'Do not increase - DNI',
			'F': 'Do not reduce - DNR',
			'G': 'All or none - AON',
			'I': 'Institutions only',
			'L': 'Last peg (last sale)',
			'M': 'Mid-price peg (midprice of inside quote)',
			'N': 'Non-negotiable',
			'O': 'Opening peg',
			'P': 'Market peg',
			'R': 'Primary peg (primary market - buy at bid/sell at offer)',
			'S': 'Suspend',
			'T': 'Fixed Peg to Local best bid or offer at time of order',
			'U': 'Customer Display Instruction (Rule11Ac1-1/4)',
			'V': 'Netting (for Forex)',
			'W': 'Peg to VWAP'
        },
        '20': {
           '0': 'New',
           '1': 'Cancel',
           '2': 'Correct',
           '3': 'Status'
        },
        '21': {
            '1': 'Automated execution order, private, no Broker intervention',
            '2': 'Automated execution order, public, Broker intervention OK',
            '3': 'Manual order, best execution'
        },
        '22': {
            '1': 'CUSIP',
            '2': 'SEDOL',
            '3': 'QUIK',
            '4': 'ISIN number',
            '5': 'RIC code',
            '6': 'ISO Currency  Code',
            '7': 'ISO Country  Code',
            '8': 'Exchange Symbol',
            '9': 'Consolidated Tape Association (CTA) Symbol (SIAC CTS/CQS line format)'
        },
        '25': {
            'L': 'Low',
            'M': 'Medium',
            'H': 'High'
        },
        '27': {
            'S': 'Small',
            'M': 'Medium',
            'L': 'Large'
        },
        '28': {
            'N': 'New',
            'C': 'Cancel',
            'R': 'Replace'
        },
        '29': {
            '1': 'Agent',
            '2': 'Cross as agent',
            '3': 'Cross as principal',
            '4': 'Principal'
        },
        '35': {
            '0': 'Heartbeat',
            '1': 'Test Request',
            '2': 'Resend Request',
            '3': 'Reject',
            '4': 'Sequence Reset',
            '5': 'Logout',
            '6': 'Indication of Interest',
            '7': 'Advertisement',
            '8': 'Execution Report',
            '9': 'Order Cancel Reject',
            'A': 'Logon',
            'B': 'News',
            'C': 'Email',
            'D': 'Order - Single',
            'E': 'Order - List',
            'F': 'Order Cancel Request',
            'G': 'Order Cancel/Replace Request',
            'H': 'Order Status Request',
            'J': 'Allocation',
            'K': 'List Cancel Request',
            'L': 'List Execute',
            'M': 'List Status Request',
            'N': 'List Status',
            'P': 'Allocation ACK',
            'Q': 'Don\'t Know Trade  (DK)',
            'R': 'Quote Request',
            'S': 'Quote',
            'T': 'Settlement Instructions',
            'V': 'Market Data Request',
            'W': 'Market Data-Snapshot/Full Refresh',
            'X': 'Market Data-Incremental Refresh',
            'Y': 'Market Data Request Reject',
            'Z': 'Quote Cancel',
            'a': 'Quote Status Request',
            'b': 'Quote Acknowledgement',
            'c': 'Security Definition Request',
            'd': 'Security Definition',
            'e': 'Security Status Request',
            'f': 'Security Status',
            'g': 'Trading Session Status Request',
            'h': 'Trading Session Status',
            'i': 'Mass Quote',
            'j': 'Business Message Reject',
            'k': 'Bid Request',
            'l': 'Bid Response  (lowercase L)',
            'm': 'List Strike Price'
        },
        '39': {
            '0': 'New',
            '1': 'Partially filled',
            '2': 'Filled',
            '3': 'Done for day',
            '4': 'Canceled',
            '5': 'Replaced',
            '6': 'Pending Cancel (e.g. result of Order Cancel Request )',
            '7': 'Stopped',
            '8': 'Rejected',
            '9': 'Suspended',
            'A': 'Pending New',
            'B': 'Calculated',
            'C': 'Expired',
            'D': 'Accepted for bidding',
            'E': 'Pending Replace (e.g. result of Order Cancel/Replace Request )'
        },
        '40': {
            '1': 'Market',
            '2': 'Limit',
            '3': 'Stop',
            '4': 'Stop limit',
            '5': 'Market on close',
            '6': 'With or without',
            '7': 'Limit or better',
            '8': 'Limit with or without',
            '9': 'On basis',
            'A': 'On close',
            'B': 'Limit on close',
            'C': 'Forex - Market',
            'D': 'Previously quoted',
            'E': 'Previously indicated',
            'F': 'Forex - Limit',
            'G': 'Forex - Swap',
            'H': 'Forex - Previously Quoted',
            'I': 'Funari (Limit Day Order with unexecuted portion handled as Market On Close. e.g. Japan)',
            'P': 'Pegged'
        },
        '54': {
            '1': 'Buy',
            '2': 'Sell',
            '3': 'Buy minus',
            '4': 'Sell plus',
            '5': 'Sell short',
            '6': 'Sell short exempt',
            '7': 'Undisclosed (valid for IOI and List Order messages only)',
            '8': 'Cross (orders where counterparty is an exchange, valid for all messages except IOIs)',
            '9': 'Cross short'
        },
        '59': {
            '0': 'Day',
            '1': 'Good Till Cancel (GTC)',
            '2': 'At the Opening (OPG)',
            '3': 'Immediate or Cancel (IOC)',
            '4': 'Fill or Kill (FOK)',
            '5': 'Good Till Crossing (GTX)',
            '6': 'Good Till Date'
        },
        '61': {
            '0': 'Normal',
            '1': 'Flash',
            '2': 'Background'
        },
        '63': {
            '0': 'Regular',
            '1': 'Cash',
            '2': 'Next Day',
            '3': 'T+2',
            '4': 'T+3',
            '5': 'T+4',
            '6': 'Future',
            '7': 'When Issued',
            '8': 'Sellers Option',
            '9': 'T+5'
        },
        '71': {
            '0': 'New',
            '1': 'Replace',
            '2': 'Cancel',
            '3': 'Preliminary (without MiscFees and NetMoney)',
            '4': 'Calculated (includes MiscFees and NetMoney)',
            '5': 'Calculated without Preliminary (sent unsolicited by broker, includes MiscFees and NetMoney)'
        },
        '81': {
            '0': 'regular',
            '1': 'soft dollar',
            '2': 'step-in',
            '3': 'step-out',
            '4': 'soft-dollar step-in',
            '5': 'soft-dollar step-out',
            '6': 'plan sponsor'
        },
        '87': {
            '0': 'accepted (successfully processed)',
            '1': 'rejected',
            '2': 'partial accept',
            '3': 'received (received, not yet processed)'
        },
        '88': {
            '0': 'unknown account(s)',
            '1': 'incorrect quantity',
            '2': 'incorrect average price',
            '3': 'unknown executing broker mnemonic',
            '4': 'commission difference',
            '5': 'unknown OrderID',
            '6': 'unknown ListID',
            '7': 'other'
        },
        '94': {
            '0': 'New',
            '1': 'Reply',
            '2': 'Admin Reply'
        },
        '98': {
            '0': 'None / other',
            '1': 'PKCS (proprietary)',
            '2': 'DES (ECB mode)',
            '3': 'PKCS/DES (proprietary)',
            '4': 'PGP/DES (defunct)',
            '5': 'PGP/DES-MD5 (see app note on FIX web site)',
            '6': 'PEM/DES-MD5 (see app note on FIX web site)'
        },
        '102': {
            '0': 'Too late to cancel',
            '1': 'Unknown order',
            '2': 'Broker Option',
            '3': 'Order already in Pending Cancel or Pending Replace status'
        },
        '103': {
            '0': 'Broker option',
            '1': 'Unknown symbol',
            '2': 'Exchange closed',
            '3': 'Order exceeds limit',
            '4': 'Too late to enter',
            '5': 'Unknown Order',
            '6': 'Duplicate Order (e.g. dupe ClOrdID)',
            '7': 'Duplicate of a verbally communicated order',
            '8': 'Stale Order'
        },
        '104': {
            'A': 'All or none',
            'C': 'At the close',
            'I': 'In touch with',
            'L': 'Limit',
            'M': 'More behind',
            'O': 'At the open',
            'P': 'Taking a position',
            'Q': 'At the Market (previously called Current Quote)',
            'R': 'Ready to trade',
            'S': 'Portfolio show-n',
            'T': 'Through the day',
            'V': 'Versus',
            'W': 'Indication - Working away',
            'X': 'Crossing opportunity',
            'Y': 'At the Midpoint',
            'Z': 'Pre-open'
        },
        '113': {
            'Y': 'Indicates that party receiving message must report trade',
            'N': 'Indicates that party sending message will report trade'
        },
        '114': {
            'Y': 'Indicates the broker is responsible for locating the stock',
            'N': 'Indicates the broker is not required to locate'
        },
        '121': {
            'Y': 'Execute Forex after security trade',
            'N': 'Do not execute Forex after security trade'
        },
        '123': {
            'Y': 'MsgSeqNum  field valid',
            'N': 'MsgSeqNum'
        },
        '127': {
            'A': 'Unknown symbol',
            'B': 'Wrong side',
            'C': 'Quantity exceeds order',
            'D': 'No matching order',
            'E': 'Price  exceeds limit',
            'Z': 'Other'
        },
        '130': {
            'Y': 'Natural',
            'N': 'Not natural'
        },
        '139': {
            '1': 'Regulatory (e.g. SEC)',
            '2': 'Tax',
            '3': 'Local Commission',
            '4': 'Exchange Fees',
            '5': 'Stamp',
            '6': 'Levy',
            '7': 'Other',
            '8': 'Markup',
            '9': 'Consumption Tax'
        },
        '141': {
            'Y': 'Yes, reset sequence numbers',
            'N': 'No'
        },
        '150': {
            '0': 'New',
            '1': 'Partial fill',
            '2': 'Fill',
            '3': 'Done for day',
            '4': 'Canceled',
            '5': 'Replaced',
            '6': 'Pending Cancel (e.g. result of Order Cancel Request)',
            '7': 'Stopped',
            '8': 'Rejected',
            '9': 'Suspended',
            'A': 'Pending New',
            'B': 'Calculated',
            'C': 'Expired',
            'D': 'Restated (ExecutionRpt sent unsolicited by sellside, with ExecRestatementReason set)',
            'E': 'Pending Replace (e.g. result of Order Cancel/Replace Request)'
        },
        '160': {
            '0': 'Default',
            '1': 'Standing Instructions Provided',
            '2': 'Specific Allocation Account Overriding',
            '3': 'Specific Allocation Account Standing'
        },
        '163': {
            'N': 'New',
            'C': 'Cancel',
            'R': 'Replace'
        },
        '165': {
            '1': 'Broker\'s Instructions',
            '2': 'Institution\'s Instructions'
        },
        '166': {
            'CED': 'CEDEL',
            'DTC': 'Depository Trust Company',
            'EUR': 'Euroclear',
            'FED': 'Federal Book Entry',
            'PNY': 'Physical',
            'PTC': 'Participant Trust Company',
            'ISO Country Code': 'Local Market Settle Location'
        },
        '167': {
            'BA': 'Bankers Acceptance',
            'CB': 'Convertible Bond (Note not part of ISITC spec)',
            'CD': 'Certificate Of Deposit',
            'CMO': 'Collateralize Mortgage Obligation',
            'CORP': 'Corporate Bond',
            'CP': 'Commercial Paper',
            'CPP': 'Corporate Private Placement',
            'CS': 'Common Stock',
            'FHA': 'Federal Housing Authority',
            'FHL': 'Federal Home Loan',
            'FN': 'Federal National Mortgage Association',
            'FOR': 'Foreign Exchange Contract',
            'FUT': 'Future',
            'GN': 'Government National Mortgage Association',
            'GOVT': 'Treasuries + Agency Debenture',
            'MF': 'Mutual Fund',
            'MIO': 'Mortgage Interest Only',
            'MPO': 'Mortgage Principal Only',
            'MPP': 'Mortgage Private Placement',
            'MPT': 'Miscellaneous Pass-Thru',
            'MUNI': 'Municipal Bond',
            'NONE': 'No ISITC Security Type',
            'OPT': 'Option',
            'PS': 'Preferred Stock',
            'RP': 'Repurchase Agreement',
            'RVRP': 'Reverse Repurchase Agreement',
            'SL': 'Student Loan Marketing Association',
            'TD': 'Time Deposit',
            'USTB': 'US Treasury Bill',
            'WAR': 'Warrant',
            'ZOO': 'Cats, Tigers & Lions (a real code: US Treasury Receipts)',
            '?': '\'Wildcard\' entry (used on Security Definition Request  message)'
        },
        '169': {
            '0': 'Other',
            '1': 'DTC SID',
            '2': 'Thomson ALERT',
            '3': 'A Global Custodian (StandInstDbName must be provided)'
        },
        '197': {
            '0': 'F/X Netting',
            '1': 'F/X Swap'
        },
        '201': {
            '0': 'Put',
            '1': 'Call'
        },
        '203': {
            '0': 'Covered',
            '1': 'Uncovered'
        },
        '204': {
            '0': 'Customer',
            '1': 'Firm'
        },
        '208': {
            'Y': 'Details should be communicated',
            'N': 'Details should not be communicated'
        },
        '209': {
            '1': 'Match',
            '2': 'Forward',
            '3': 'Forward and Match'
        },
        '216': {
            '1': 'Target Firm',
            '2': 'Target List',
            '3': 'Block Firm',
            '4': 'Block List'
        },
        '219': {
            '1': 'CURVE',
            '2': '5-YR',
            '3': 'OLD-5',
            '4': '10-YR',
            '5': 'OLD-10',
            '6': '30-YR',
            '7': 'OLD-30',
            '8': '3-MO-LIBOR',
            '9': '6-MO-LIBOR'
        },
        '263': {
            '0': 'Snapshot',
            '1': 'Snapshot + Updates (Subscribe)',
            '2': 'Disable previous Snapshot + Update Request (Unsubscribe)'
        },
        '264': {
            '0': 'Full Book',
            '1': 'Top of Book',
            'N>1': 'Report best N price tiers of data'
        },
        '265': {
            '0': 'Full Refresh',
            '1': 'Incremental Refresh'
        },
        '266': {
            'Y': 'one book entry per side per price',
            'N': 'Multiple entries per side per price allowed',
            '(Not specified)': 'broker option'
        },
        '269': {
            '0': 'Bid',
            '1': 'Offer',
            '2': 'Trade',
            '3': 'Index Value',
            '4': 'Opening Price',
            '5': 'Closing Price',
            '6': 'Settlement Price',
            '7': 'Trading Session High Price',
            '8': 'Trading Session Low Price',
            '9': 'Trading Session VWAP Price'
        },
        '274': {
            '0': 'Plus Tick',
            '1': 'Zero-Plus Tick',
            '2': 'Minus Tick',
            '3': 'Zero-Minus Tick'
        },
        '276': {
            'A': 'Open / Active',
            'B': 'Closed / Inactive',
            'C': 'Exchange Best',
            'D': 'Consolidated Best',
            'E': 'Locked',
            'F': 'Crossed',
            'G': 'Depth',
            'H': 'Fast Trading',
            'I': 'Non-Firm'
        },
        '277': {
            'A': 'Cash (only) Market',
            'B': 'Average Price Trade',
            'C': 'Cash Trade (same day clearing)',
            'D': 'Next Day (only) Market',
            'E': 'Opening / Reopening Trade Detail',
            'F': 'Intraday Trade Detail',
            'G': 'Rule 127 Trade (NYSE)',
            'H': 'Rule 155 Trade (Amex)',
            'I': 'Sold Last (late reporting)',
            'J': 'Next Day Trade (next day clearing)',
            'K': 'Opened (late report of opened trade)',
            'L': 'Seller',
            'M': 'Sold (out of sequence)',
            'N': 'Stopped Stock (guarantee of price but does not execute the order)'
        },
        '279': {
            '0': 'New',
            '1': 'Change',
            '2': 'Delete'
        },
        '281': {
            '0': 'Unknown symbol',
            '1': 'Duplicate MDReqID',
            '2': 'Insufficient Bandwidth',
            '3': 'Insufficient Permissions',
            '4': 'Unsupported SubscriptionRequestType',
            '5': 'Unsupported MarketDepth',
            '6': 'Unsupported MDUpdateType',
            '7': 'Unsupported AggregatedBook',
            '8': 'Unsupported MDEntryType'
        },
        '285': {
            '0': 'Cancelation / Trade Bust',
            '1': 'Error'
        },
        '286': {
            '0': 'Daily Open / Close / Settlement price',
            '1': 'Session Open / Close / Settlement price',
            '2': 'Delivery Settlement price'
        },
        '291': {
            '1': 'Bankrupt'
        },
        '292': {
            'A': 'Ex-Dividend',
            'B': 'Ex-Distribution',
            'C': 'Ex-Rights',
            'D': 'New',
            'E': 'Ex-Interest'
        },
        '297': {
            '0': 'Accepted',
            '1': 'Canceled for Symbol (s)',
            '2': 'Canceled for Security Type (s)',
            '3': 'Canceled for Underlying Symbol',
            '4': 'Canceled All',
            '5': 'Rejected'
        },
        '303': {
            '1': 'Manual',
            '2': 'Automatic'
        },
        '305': {
            '1': 'CUSIP',
            '2': 'SEDOL',
            '3': 'QUIK',
            '4': 'ISIN number',
            '5': 'RIC code',
            '6': 'ISO Currency  Code',
            '7': 'ISO Country  Code',
            '8': 'Exchange Symbol',
            '9': 'Consolidated Tape Association (CTA) Symbol (SIAC CTS/CQS line format)'
        },
        '310': {
            'BA': 'Bankers Acceptance',
            'CB': 'Convertible Bond (Note not part of ISITC spec)',
            'CD': 'Certificate Of Deposit',
            'CMO': 'Collateralize Mortgage Obligation',
            'CORP': 'Corporate Bond',
            'CP': 'Commercial Paper',
            'CPP': 'Corporate Private Placement',
            'CS': 'Common Stock',
            'FHA': 'Federal Housing Authority',
            'FHL': 'Federal Home Loan',
            'FN': 'Federal National Mortgage Association',
            'FOR': 'Foreign Exchange Contract',
            'FUT': 'Future',
            'GN': 'Government National Mortgage Association',
            'GOVT': 'Treasuries + Agency Debenture',
            'MF': 'Mutual Fund',
            'MIO': 'Mortgage Interest Only',
            'MPO': 'Mortgage Principal Only',
            'MPP': 'Mortgage Private Placement',
            'MPT': 'Miscellaneous Pass-Thru',
            'MUNI': 'Municipal Bond',
            'NONE': 'No ISITC Security Type',
            'OPT': 'Option',
            'PS': 'Preferred Stock',
            'RP': 'Repurchase Agreement',
            'RVRP': 'Reverse Repurchase Agreement',
            'SL': 'Student Loan Marketing Association',
            'TD': 'Time Deposit',
            'USTB': 'US Treasury Bill',
            'WAR': 'Warrant',
            'ZOO': 'Cats, Tigers & Lions (a real code: US Treasury Receipts)',
            '?': '\'Wildcard\' entry (used on Security Definition Request  message)'
        },
        '321': {
            '0': 'Request Security identity and specifications',
            '1': 'Request Security identity for the specifications provided (Name of the security is not supplied)',
            '2': 'Request List Security Types',
            '3': 'Request List Securities (Can be qualified with SecurityExchange  is provided then only list Securities for the specific type)'
        },
        '323': {
            '1': 'Accept security proposal as is',
            '2': 'Accept security proposal with revisions as indicated in the message',
            '3': 'List of security types returned per request',
            '4': 'List of securities returned per request',
            '5': 'Reject security proposal',
            '6': 'Can not match selection criteria'
        },
        '325': {
            'Y': 'Message is being sent unsolicited',
            'N': 'Message is being sent as a result of a prior request'
        },
        '326': {
            '1': 'Opening Delay',
            '2': 'Trading Halt',
            '3': 'Resume',
            '4': 'No Open/No Resume',
            '5': 'Price Indication',
            '6': 'Trading Range Indication',
            '7': 'Market Imbalance Buy',
            '8': 'Market Imbalance Sell',
            '9': 'Market On Close Imbalance Buy',
            '10': 'Market On Close Imbalance Sell',
            '11': '(not assigned)',
            '12': 'No Market Imbalance',
            '13': 'No Market On Close Imbalance',
            '14': 'ITS Pre-Opening',
            '15': 'New Price Indication',
            '16': 'Trade Dissemination Time',
            '17': 'Ready to trade (start of session)',
            '18': 'Not Available for trading (end of session)',
            '19': 'Not Traded on this Market',
            '20': 'Unknown or Invalid'
        },
        '327': {
            'I': 'Order Imbalance',
            'X': 'Equipment Changeover',
            'P': 'News  Pending',
            'D': 'News  Dissemination',
            'E': 'Order Influx',
            'M': 'Additional Information'
        },
        '328': {
            'Y': 'Halt was due to common stock being halted',
            'N': 'Halt was not related to a halt of the common stock'
        },
        '329': {
            'Y': 'Halt was due to related security being halted',
            'N': 'Halt was not related to a halt of the related security'
        },
        '334': {
            '1': 'Cancel',
            '2': 'Error',
            '3': 'Correction'
        },
        '338': {
            '1': 'Electronic',
            '2': 'Open Outcry',
            '3': 'Two Party'
        },
        '339': {
            '1': 'Testing',
            '2': 'Simulated',
            '3': 'Production'
        },
        '340': {
            '1': 'Halted',
            '2': 'Open',
            '3': 'Closed',
            '4': 'Pre-Open',
            '5': 'Pre-Close'
        },
        '347': {
            'ISO-2022-JP (for using JIS)': 'ISO-2022-JP (for using JIS)',
            'EUC-JP (for using EUC)': 'EUC-JP (for using EUC)',
            'Shift_JIS (for using SJIS)': 'Shift_JIS (for using SJIS)',
            'UTF-8 (for using Unicode)': 'UTF-8 (for using Unicode)'
        },
        '368': {
            '1': 'Unknown symbol (Security)',
            '2': 'Exchange(Security) closed',
            '3': 'Quote exceeds limit',
            '4': 'Too late to enter',
            '5': 'Unknown Quote',
            '6': 'Duplicate Quote',
            '7': 'Invalid bid/ask spread',
            '8': 'Invalid price',
            '9': 'Not authorized to quote security'
        },
        '373': {
            '0': 'Invalid tag number',
            '1': 'Required tag missing',
            '2': 'Tag not defined for this message type',
            '3': 'Undefined Tag',
            '4': 'Tag specified without a value',
            '5': 'Value is incorrect (out of range) for this tag',
            '6': 'Incorrect data format for value',
            '7': 'Decryption problem',
            '8': 'Signature  problem',
            '9': 'CompID problem',
            '10': 'SendingTime  accuracy problem',
            '11': 'Invalid MsgType'
        },
        '374': {
            'N': 'New',
            'C': 'Cancel'
        },
        '377': {
            'Y': 'Was solcitied',
            'N': 'Was not solicited'
        },
        '378': {
            '0': 'GT Corporate action',
            '1': 'GT renewal / restatement (no corporate action)',
            '2': 'Verbal change',
            '3': 'Repricing of order',
            '4': 'Broker option',
            '5': 'Partial decline of OrderQty  (e.g. exchange-initiated partial cancel)'
        },
        '380': {
            '0': 'Other',
            '1': 'Unknown ID',
            '2': 'Unknown Security',
            '3': 'Unsupported Message Type',
            '4': 'Application not available',
            '5': 'Conditionally Required Field Missing'
        },
        '385': {
            'S': 'Send',
            'R': 'Receive'
        },
        '388': {
            '0': 'Related to displayed price',
            '1': 'Related to market price',
            '2': 'Related to primary price',
            '3': 'Related to local primary price',
            '4': 'Related to midpoint price',
            '5': 'Related to last trade price'
        },
        '394': {
            '1': '\'Non Disclosed\' Style (e.g. US/European)',
            '2': '\'Disclosed\' Style (e.g. Japanese)',
            '3': 'No Bidding Process'
        },
        '399': {
            '1': 'Sector',
            '2': 'Country',
            '3': 'Index'
        },
        '401': {
                '1': 'SideValue1',
                '2': 'SideValue2'
        },
        '409': {
                '1': '5day moving average',
                '2': '20 day moving average',
                '3': 'Normal Market Size',
                '4': 'Other'
        },
        '411': {
                'Y': 'True',
                'N': 'False'
        },
        '414': {
                '1': 'BuySide explicitly requests status using StatusRequest (Default). The sell-side firm can however, send a DONE status List Status  Response in an unsolicited fashion',
                '2': 'SellSide periodically sends status using List Status . Period optionally specified in ProgressPeriod',
                '3': 'Real-time execution reports (to be discouraged)'
        },
        '416': {
                '1': 'Net',
                '2': 'Gross'
        },
        '418': {
            'R': 'Risk Trade',
            'G': 'VWAP Guarantee',
            'A': 'Agency',
            'J': 'Guaranteed Close'
        },
        '419': {
            '2': 'Closing Price at morning session',
            '3': 'Closing Price',
            '4': 'Current price',
            '5': 'SQ',
            '6': 'VWAP through a day',
            '7': 'VWAP through a morning session',
            '8': 'VWAP through an afternoon session',
            '9': 'VWAP through a day except YORI',
            'A': 'VWAP through a morning session except YORI',
            'B': 'VWAP through an afternoon session except YORI',
            'C': 'Strike',
            'D': 'Open',
            'Z': 'Others'
        },
        '423': {
            '1': 'Percentage',
            '2': 'Per share (e.g. cents per share)',
            '3': 'Fixed Amount (absolute value)'
        },
        '427': {
            '0': 'book out all trades on day of execution',
            '1': 'accumulate executions until order is filled or expires',
            '2': 'accumulate until verbally notified otherwise'
        },
        '429': {
            '1': 'Ack',
            '2': 'Response',
            '3': 'Timed',
            '4': 'ExecStarted',
            '5': 'AllDone',
            '6': 'Alert'
        },
        '430': {
            '1': 'Net',
            '2': 'Gross'
        },
        '431': {
            '1': 'InBiddingProcess',
            '2': 'ReceivedForExecution',
            '3': 'Executing',
            '4': 'Canceling',
            '5': 'Alert',
            '6': 'All Done',
            '7': 'Reject'
        },
        '433': {
            '1': 'Immediate',
            '2': 'Wait for Execute Instruction (e.g. a List Execute  message or phone call before proceeding with execution of the list)'
        },
        '434': {
            '1': 'Order Cancel Request',
            '2': 'Order Cancel/Replace Request'
        }
    }

    # need https://www.onixs.biz/fix-dictionary/4.4/app_6_c.html

    fix44fields = {
        '4': {
            'B': 'Buy', 
            'S': 'Sell',
            'X': 'Cross',
            'T': 'Trade'
        },
        '5': {
            'N': 'New',
            'C': 'Cancel',
            'R': 'Replace'
        },
        '13': {
            '1': 'per unit (implying shares, par, currency, etc)',
            '2': 'percentage',
            '3': 'absolute (total monetary amount)',
            '4': '(for CIV buy orders) percentage waived - cash discount',
            '5': '(for CIV buy orders) percentage waived - enhanced units',
            '6': 'points per bond or or contract [Supply  component block if the object security is denominated in a size other than the industry default - 1000 par for bonds.]'
        },
        '18': {
            '1': 'Not held',
                '2': 'Work',
                '3': 'Go along',
                '4': 'Over the day',
                '5': 'Held',
                '6': 'Participate don\'t initiate',
                '7': 'Strict scale',
                '8': 'Try to scale',
                '9': 'Stay on bidside',
                '0': 'Stay on offerside',
                'A': 'No cross (cross is forbidden)',
                'B': 'OK to cross',
                'C': 'Call first',
                'D': 'Percent of volume (indicates that the sender does not want to be all of the volume on the floor vs. a specific percentage)',
                'E': 'Do not increase - DNI',
                'F': 'Do not reduce - DNR',
                'G': 'All or none - AON',
                'H': 'Reinstate on System Failure (mutually exclusive with Q)',
                'I': 'Institutions only',
                'J': 'Reinstate on Trading Halt (mutually exclusive with K)',
                'K': 'Cancel on Trading Halt (mutually exclusive with L)',
                'L': 'Last peg (last sale)',
                'M': 'Mid-price peg (midprice of inside quote)',
                'N': 'Non-negotiable',
                'O': 'Opening peg',
                'P': 'Market peg',
                'Q': 'Cancel on System Failure (mutually exclusive with H)',
                'R': 'Primary peg (primary market - buy at bid/sell at offer)',
                'S': 'Suspend',
                '<del>T': 'Fixed Peg to Local best bid or offer at time of order</del> (Replaced)',
                'U': 'Customer Display Instruction (RuleAc-/4)',
                'V': 'Netting (for Forex)',
                'W': 'Peg to VWAP',
                'X': 'Trade Along',
                'Y': 'Try to Stop',
                'Z': 'Cancel if Not Best',
                'a': 'Trailing Stop Peg',
                'b': 'Strict Limit (No Price Improvement)',
                'c': 'Ignore Price Validity Checks',
                'd': 'Peg to Limit Price',
                'e': 'Work to Target Strategy'
        },
        '21': {
            '1': 'Automated execution order, private, no Broker intervention',
            '2': 'Automated execution order, public, Broker intervention OK',
            '3': 'Manual order, best execution'
        },
        '22': {
            '1': 'CUSIP',
            '2': 'SEDOL',
            '3': 'QUIK',
            '4': 'ISIN number',
            '5': 'RIC code',
            '6': 'ISO Currency  Code',
            '7': 'ISO Country  Code',
            '8': 'Exchange Symbol',
            '9': 'Consolidated Tape Association (CTA) Symbol (SIAC CTS/CQS line format)',
            'A': 'Bloomberg Symbol',
            'B': 'Wertpapier',
            'C': 'Dutch',
            'D': 'Valoren',
            'E': 'Sicovam',
            'F': 'Belgian',
            'G': '"Common" (Clearstream and Euroclear)',
            'H': 'Clearing House / Clearing Organization',
            'I': 'ISDA/FpML Product Specification',
            'J': 'Options Price Reporting Authority'
        },
        '25': {
            'L': 'Low',
            'M': 'Medium',
            'H': 'High'
        },
        '27': {
            'S': 'Small',
            'M': 'Medium',
            'L': 'Large'
        },
        '28': {
            'N': 'New',
            'C': 'Cancel',
            'R': 'Replace'
        },
        '29': {
            '1': 'Agent',
            '2': 'Cross as agent',
            '3': 'Cross as principal',
            '4': 'Principal'
        },
        '35': {
            '0': 'Heartbeat',
            '1': 'Test Request',
            '2': 'Resend Request',
            '3': 'Reject',
            '4': 'Sequence Reset',
            '5': 'Logout',
            '6': 'Indication of Interest',
            '7': 'Advertisement',
            '8': 'Execution Report',
            '9': 'Order Cancel Reject',
            'A': 'Logon',
            'B': 'News',
            'C': 'Email',
            'D': 'New Order Single',
            'E': 'New Order List',
            'F': 'Order Cancel Request',
            'G': 'Order Cancel/Replace Request',
            'H': 'Order Status Request',
            'J': 'Allocation Instruction',
            'K': 'List Cancel Request',
            'L': 'List Execute',
            'M': 'List Status Request',
            'N': 'List Status',
            'P': 'Allocation Instruction Ack',
            'Q': 'Don\'t Know Trade  (DK)',
            'R': 'Quote Request',
            'S': 'Quote',
            'T': 'Settlement Instructions',
            'V': 'Market Data Request',
            'W': 'Market Data-Snapshot/Full Refresh',
            'X': 'Market Data-Incremental Refresh',
            'Y': 'Market Data Request Reject',
            'Z': 'Quote Cancel',
            'a': 'Quote Status Request',
            'b': 'Mass Quote Acknowledgement',
            'c': 'Security Definition Request',
            'd': 'Security Definition',
            'e': 'Security Status Request',
            'f': 'Security Status',
            'g': 'Trading Session Status Request',
            'h': 'Trading Session Status',
            'i': 'Mass Quote',
            'j': 'Business Message Reject',
            'k': 'Bid Request',
            'l': 'Bid Response  (lowercase L)',
            'm': 'List Strike Price',
            'n': 'XML message  (e.g. non-FIX MsgType)',
            'o': 'Registration Instructions',
            'p': 'Registration Instructions Response',
            'q': 'Order Mass Cancel Request',
            'r': 'Order Mass Cancel Report',
            's': 'New Order Cross',
            't': 'Cross Order Cancel/Replace Request  (a.k.a. Cross Order Modification Request)',
            'u': 'Cross Order Cancel Request',
            'v': 'Security Type Request',
            'w': 'Security Types',
            'x': 'Security List Request',
            'y': 'Security List',
            'z': 'Derivative Security List Request',
            'AA': 'Derivative Security List',
            'AB': 'New Order Multileg',
            'AC': 'Multileg Order Cancel/Replace  (a.k.a. Multileg Order Modification Request)',
            'AD': 'Trade Capture Report Request',
            'AE': 'Trade Capture Report',
            'AF': 'Order Mass Status Request',
            'AG': 'Quote Request Reject',
            'AH': 'RFQ Request',
            'AI': 'Quote Status Report',
            'AJ': 'Quote Response',
            'AK': 'Confirmation',
            'AL': 'Position Maintenance Request',
            'AM': 'Position Maintenance Report',
            'AN': 'Request For Positions',
            'AO': 'Request For Positions Ack',
            'AP': 'Position Report',
            'AQ': 'Trade Capture Report Request Ack',
            'AR': 'Trade Capture Report Ack',
            'AS': 'Allocation Report  (aka Allocation Claim)',
            'AT': 'Allocation Report Ack  (aka Allocation Claim Ack)',
            'AU': 'Confirmation Ack  (aka Affirmation)',
            'AV': 'Settlement Instruction Request',
            'AW': 'Assignment Report',
            'AX': 'Collateral Request',
            'AY': 'Collateral Assignment',
            'AZ': 'Collateral Response',
            'BA': 'Collateral Report',
            'BB': 'Collateral Inquiry',
            'BC': 'Network (Counterparty System) Status Request',
            'BD': 'Network (Counterparty System) Status Response',
            'BE': 'User Request',
            'BF': 'User Response',
            'BG': 'Collateral Inquiry Ack',
            'BH': 'Confirmation Request'
        },
        '39': {
            '0': 'New',
            '1': 'Partially filled',
            '2': 'Filled',
            '3': 'Done for day',
            '4': 'Canceled',
            '5': '<del>Replaced</del> (Removed/Replaced)',
            '6': 'Pending Cancel (e.g. result of Order Cancel Request )',
            '7': 'Stopped',
            '8': 'Rejected',
            '9': 'Suspended',
            'A': 'Pending New',
            'B': 'Calculated',
            'C': 'Expired',
            'D': 'Accepted for bidding',
            'E': 'Pending Replace (e.g. result of Order Cancel/Replace Request )'
        },
        '40': {
            '1': 'Market',
            '2': 'Limit',
            '3': 'Stop',
            '4': 'Stop limit',
            '6': 'With or without',
            '7': 'Limit or better (Deprecated)',
            '8': 'Limit with or without',
            '9': 'On basis',
            'D': 'Previously quoted',
            'E': 'Previously indicated',
            'G': 'Forex - Swap',
            'I': 'Funari (Limit Day Order with unexecuted portion handled as Market On Close. E.g. Japan)',
            'J': 'Market If Touched (MIT)',
            'K': 'Market with Leftover as Limit (market order then unexecuted quantity becomes limit order at last price)',
            'L': 'Previous Fund Valuation Point (Historic pricing) (for CIV)',
            'M': 'Next Fund Valuation Point (Forward pricing) (for CIV)',
            'P': 'Pegged'
        },
        '43': {
            'Y': 'Possible duplicate',
            'N': 'Original transmission'
        },
        '47': {
            'A': 'Agency single order',
            'B': 'Short exempt transaction (refer to A type)',
            'C': 'Program Order, non-index arb, for Member firm/org',
            'D': 'Program Order, index arb, for Member firm/org',
            'E': 'Short Exempt Transaction for Principal (was incorrectly identified in the FIX spec as "Registered Equity Market Maker',
            'F': 'Short exempt transaction (refer to W type)',
            'H': 'Short exempt transaction (refer to I type)',
            'I': 'Individual Investor, single order',
            'J': 'Program Order, index arb, for individual customer',
            'K': 'Program Order, non-index arb, for individual customer',
            'L': 'Short exempt transaction for member competing market-maker affiliated with the firm clearing the trade (refer to P and',
            'M': 'Program Order, index arb, for other member',
            'N': 'Program Order, non-index arb, for other member',
            'O': 'Proprietary transactions for competing market-maker that is affiliated with the clearing member (was incorrectly identified',
            'P': 'Principal',
            'R': 'Transactions for the account of a non-member competing market maker (was incorrectly identified in the FIX spec as "Competing',
            'S': 'Specialist trades',
            'T': 'Transactions for the account of an unaffiliated member\'s competing market maker (was incorrectly identified in the FIX',
            'U': 'Program Order, index arb, for other agency',
            'W': 'All other orders as agent for other member',
            'X': 'Short exempt transaction for member competing market-maker not affiliated with the firm clearing the trade (refer to W',
            'Y': 'Program Order, non-index arb, for other agency',
            'Z': 'Short exempt transaction for non-member competing market-maker (refer to A and R types)'
        },
        '54': {
            '1': 'Buy',
            '2': 'Sell',
            '3': 'Buy minus',
            '4': 'Sell plus',
            '5': 'Sell short',
            '6': 'Sell short exempt',
            '7': 'Undisclosed (valid for IOI and List Order messages only)',
            '8': 'Cross (orders where counterparty is an exchange, valid for all messages except IOIs)',
            '9': 'Cross short',
            'A': 'Cross short exempt',
            'B': '"As Defined" (for use with multileg instruments)',
            'C': '"Opposite" (for use with multileg instruments)',
            'D': 'Subscribe (e.g. CIV)',
            'E': 'Redeem (e.g. CIV)',
            'F': 'Lend (FINANCING - identifies direction of collateral)',
            'G': 'Borrow (FINANCING - identifies direction of collateral)'
        },
        '59': {
            '0': 'Day (or session)',
            '1': 'Good Till Cancel (GTC)',
            '2': 'At the Opening (OPG)',
            '3': 'Immediate or Cancel (IOC)',
            '4': 'Fill or Kill (FOK)',
            '5': 'Good Till Crossing (GTX)',
            '6': 'Good Till Date',
            '7': 'At the Close'
        },
        '61': {
            '0': 'Normal',
            '1': 'Flash',
            '2': 'Background'
        },
        '63': {
            '0': 'Regular',
            '1': 'Cash',
            '2': 'Next Day (T+)',
            '3': 'T+2',
            '4': 'T+3',
            '5': 'T+4',
            '6': 'Future',
            '7': 'When And If Issued',
            '8': 'Sellers Option',
            '9': 'T+5'
        },
        '71': {
            '0': 'New',
            '1': 'Replace',
            '2': 'Cancel'
        },
        '77': {
            'O': 'Open',
            'C': 'Close',
            'R': 'Rolled',
            'F': 'FIFO'
        },
        '81': {
            '0': 'regular',
            '1': 'soft dollar',
            '2': 'step-in',
            '3': 'step-out',
            '4': 'soft-dollar step-in',
            '5': 'soft-dollar step-out',
            '6': 'plan sponsor'
        },
        '87': {
            '0': 'accepted (successfully processed)',
            '1': 'block level reject',
            '2': 'account level reject',
            '3': 'received (received, not yet processed)',
            '4': 'incomplete',
            '5': 'rejected by intermediary'
        },
        '88': {
            '0': 'unknown account(s)',
            '1': 'incorrect quantity',
            '2': 'incorrect average price',
            '3': 'unknown executing broker mnemonic',
            '4': 'commission difference',
            '5': 'unknown OrderID',
            '6': 'unknown ListID',
            '7': 'other (further in Text )',
            '8': 'incorrect allocated quantity',
            '9': 'calculation difference',
            '10': 'unknown or stale ExecID',
            '11': 'mismatched data value (further in Text)',
            '12': 'unknown ClOrdID',
            '13': 'warehouse request rejected'
        },
        '94': {
            '0': 'New',
            '1': 'Reply',
            '2': 'Admin Reply'
        },
        '97': {
            'Y': 'Possible resend',
            'N': 'Original transmission'
        },
        '98': {
            '0': 'None / other',
            '1': 'PKCS (proprietary)',
            '2': 'DES (ECB mode)',
            '3': 'PKCS/DES (proprietary)',
            '4': 'PGP/DES (defunct)',
            '5': 'PGP/DES-MD5 (see app note on FIX web site)',
            '6': 'PEM/DES-MD5 (see app note on FIX web site)'
        },
        '102': {
            '0': 'Too late to cancel',
            '1': 'Unknown order',
            '2': 'Broker / Exchange Option',
            '3': 'Order already in Pending Cancel or Pending Replace status',
            '4': 'Unable to process Order Mass Cancel Request',
            '5': 'TransactTime  of order',
            '6': 'Duplicate ClOrdID  received',
            '99': 'Other'
        },
        '103': {
            '0': 'Broker / Exchange option',
            '1': 'Unknown symbol',
            '2': 'Exchange closed',
            '3': 'Order exceeds limit',
            '4': 'Too late to enter',
            '5': 'Unknown Order',
            '6': 'Duplicate Order (e.g. dupe ClOrdID )',
            '7': 'Duplicate of a verbally communicated order',
            '8': 'Stale Order',
            '9': 'Trade Along required',
            '10': 'Invalid Investor ID',
            '11': 'Unsupported order characteristic',
            '12': 'Surveillence Option',
            '13': 'Incorrect quantity',
            '14': 'Incorrect allocated quantity',
            '15': 'Unknown account(s)',
            '99': 'Other'
        },
        '104': {
            'A': 'All or none',
            'B': 'Market On Close (MOC) (held to close)',
            'C': 'At the close (around/not held to close)',
            'D': 'VWAP (Volume Weighted Avg Price)',
            'I': 'In touch with',
            'L': 'Limit',
            'M': 'More behind',
            'O': 'At the open',
            'P': 'Taking a position',
            'Q': 'At the Market (previously called Current Quote)',
            'R': 'Ready to trade',
            'S': 'Portfolio shown',
            'T': 'Through the day',
            'V': 'Versus',
            'W': 'Indication - Working away',
            'X': 'Crossing opportunity',
            'Y': 'At the Midpoint',
            'Z': 'Pre-open'
        },
        '113': {
            'Y': 'Indicates that party receiving message must report trade',
            'N': 'Indicates that party sending message will report trade'
        },
        '114': {
            'Y': 'Indicates the broker is responsible for locating the stock',
            'N': 'Indicates the broker is not required to locate'
        },
        '121': {
            'Y': 'Execute Forex after security trade',
            'N': 'Do not execute Forex after security trade'
        },
        '123': {
            'Y': 'MsgSeqNum  field valid',
            'N': 'MsgSeqNum'
        },
        '127': {
            'A': 'Unknown symbol',
            'B': 'Wrong side',
            'C': 'Quantity exceeds order',
            'D': 'No matching order',
            'E': 'Price  exceeds limit',
            'F': 'Calculation difference',
            'Z': 'Other'
        },
        '130': {
            'Y': 'Natural',
            'N': 'Not natural'
        },
        '139': {
            '1': 'Regulatory (e.g. SEC)',
            '2': 'Tax',
            '3': 'Local Commission',
            '4': 'Exchange Fees',
            '5': 'Stamp',
            '6': 'Levy',
            '7': 'Other',
            '8': 'Markup',
            '9': 'Consumption Tax',
            '10': 'Per transaction',
            '11': 'Conversion',
            '12': 'Agent'
        },
        '141': {
            'Y': 'Yes, reset sequence numbers',
            'N': 'No'
        },
        '150': {
            '0': 'New',
            '3': 'Done for day',
            '4': 'Canceled',
            '5': 'Replaced',
            '6': 'Pending Cancel (e.g. result of Order Cancel Request )',
            '7': 'Stopped',
            '8': 'Rejected',
            '9': 'Suspended',
            'A': 'Pending New',
            'B': 'Calculated',
            'C': 'Expired',
            'D': 'Restated (ExecRestatementReason  set)',
            'E': 'Pending Replace (e.g. result of Order Cancel/Replace Request )',
            'F': 'Trade (partial fill or fill)',
            'G': 'Trade Correct (formerly an ExecTransType )',
            'H': 'Trade Cancel (formerly an ExecTransType )',
            'I': 'Order Status (formerly an ExecTransType )',
        },
        '160': {
            '1': 'Standing Instructions Provided',
            '4': 'Specific Order for a single account (for CIV)',
            '5': 'Request reject'
        },
        '163': {
            'N': 'New',
            'C': 'Cancel',
            'R': 'Replace',
            'T': 'Restate (used where the Settlement Instruction is being used to communicate standing instructions which have not been',
        },
        '165': {
            '1': 'Broker\'s Instructions',
            '2': 'Institution\'s Instructions',
            '3': 'Investor (e.g. CIV use)'
        },
        '169': {
            '0': 'Other',
            '1': 'DTC SID',
            '2': 'Thomson ALERT',
            '3': 'A Global Custodian (StandInstDbName  must be provided)',
            '4': 'AccountNet'
        },
        '197': {
            '0': 'F/X Netting',
            '1': 'F/X Swap'
        },
        '203': {
            '0': 'Covered',
            '1': 'Uncovered'
        },
        '208': {
            'Y': 'Details should be communicated',
            'N': 'Details should not be communicated'
        },
        '209': {
            '1': 'Match',
            '2': 'Forward',
            '3': 'Forward and Match'
        },
        '216': {
            '1': 'Target Firm',
            '2': 'Target List',
            '3': 'Block Firm',
            '4': 'Block List'
        },
        '235': {
            'AFTERTAX': 'After Tax Yield (Municipals)',
            'ANNUAL': 'Annual Yield',
            'ATISSUE': 'Yield At Issue (Municipals)',
            'AVGMATURITY': 'Yield To Average Maturity',
            'BOOK': 'Book Yield',
            'CALL': 'Yield to Next Call',
            'CHANGE': 'Yield Change Since Close',
            'CLOSE': 'Closing Yield',
            'COMPOUND': 'Compound Yield',
            'CURRENT': 'Current Yield',
            'GROSS': 'True Gross Yield',
            'GOVTEQUIV': 'Government Equivalent Yield',
            'INFLATION': 'Yield with Inflation Assumption',
            'INVERSEFLOATER': 'Inverse Floater Bond Yield',
            'LASTCLOSE': 'Most Recent Closing Yield',
            'LASTMONTH': 'Closing Yield Most Recent Month',
            'LASTQUARTER': 'Closing Yield Most Recent Quarter',
            'LASTYEAR': 'Closing Yield Most Recent Year',
            'LONGAVGLIFE': 'Yield to Longest Average Life',
            'MARK': 'Mark To Market Yield',
            'MATURITY': 'Yield to Maturity',
            'NEXTREFUND': 'Yield To Next Refund (Sinking Fund Bonds)',
            'OPENAVG': 'Open Average Yield',
            'PUT': 'Yield to Next Put',
            'PREVCLOSE': 'Previous Close Yield',
            'PROCEEDS': 'Proceeds Yield',
            'SEMIANNUAL': 'Semi-annual Yield',
            'SHORTAVGLIFE': 'Yield to Shortest Average Life',
            'SIMPLE': 'Simple Yield',
            'TAXEQUIV': 'Tax Equivalent Yield',
            'TENDER': 'Yield to Tender Date',
            'TRUE': 'True Yield',
            'VALUE1/32': 'Yield Value Of 1/32',
            'WORST': 'Yield To Worst'
        },
        '258': {
            'Y': 'Traded Flat',
            'N': 'Not Traded Flat'
        },
        '263': {
            '0': 'Snapshot',
            '1': 'Snapshot + Updates (Subscribe)',
            '2': 'Disable previous Snapshot + Update Request (Unsubscribe)'
        },
        '264': {
            '0': 'Full Book',
            '1': 'Top of Book',
            'N>1': 'Report best N price tiers of data'
        },
        '265': {
            '0': 'Full Refresh',
            '1': 'Incremental Refresh'
        },
        '266': {
            'Y': 'one book entry per side per price',
            'N': 'Multiple entries per side per price allowed',
            '(Not specified)': 'broker option'
        },
        '269': {
            '0': 'Bid',
            '1': 'Offer',
            '2': 'Trade',
            '3': 'Index Value',
            '4': 'Opening Price',
            '5': 'Closing Price',
            '6': 'Settlement Price',
            '7': 'Trading Session High Price',
            '8': 'Trading Session Low Price',
            '9': 'Trading Session VWAP Price',
            'A': 'Imbalance',
            'B': 'Trade Volume',
            'C': 'Open Interest'
        },
        '274': {
            '0': 'Plus Tick',
            '1': 'Zero-Plus Tick',
            '2': 'Minus Tick',
            '3': 'Zero-Minus Tick'
        },
        '276': {
            'A': 'Open / Active',
            'B': 'Closed / Inactive',
            'C': 'Exchange Best',
            'D': 'Consolidated Best',
            'E': 'Locked',
            'F': 'Crossed',
            'G': 'Depth',
            'H': 'Fast Trading',
            'I': 'Non-Firm'
        },
        '277': {
            'A': 'Cash (only) Market',
            'B': 'Average Price Trade',
            'C': 'Cash Trade (same day clearing)',
            'D': 'Next Day (only) Market',
            'E': 'Opening / Reopening Trade Detail',
            'F': 'Intraday Trade Detail',
            'G': 'Rule 127 Trade (NYSE)',
            'H': 'Rule 155 Trade (Amex)',
            'I': 'Sold Last (late reporting)',
            'J': 'Next Day Trade (next day clearing)',
            'K': 'Opened (late report of opened trade)',
            'L': 'Seller',
            'M': 'Sold (out of sequence)',
            'N': 'Stopped Stock (guarantee of price but does not execute the order)',
            'P': 'Imbalance More Buyers (Cannot be used in combination with Q)',
            'Q': 'Imbalance More Sellers (Cannot be used in combination with P)',
            'R': 'Opening Price'
        },
        '279': {
            '0': 'New',
            '1': 'Change',
            '2': 'Delete'
        },
        '281': {
            '0': 'Unknown symbol',
            '1': 'Duplicate MDReqID',
            '2': 'Insufficient Bandwidth',
            '3': 'Insufficient Permissions',
            '4': 'Unsupported SubscriptionRequestType',
            '5': 'Unsupported MarketDepth',
            '6': 'Unsupported MDUpdateType',
            '7': 'Unsupported AggregatedBook',
            '8': 'Unsupported MDEntryType',
            '9': 'Unsupported TradingSessionID',
            'A': 'Unsupported Scope',
            'B': 'Unsupported OpenCloseSettlFlag',
            'C': 'Unsupported MDImplicitDelete'
        },
        '285': {
            '0': 'Cancelation / Trade Bust',
            '1': 'Error'
        },
        '286': {
            '0': 'Daily Open / Close / Settlement entry',
            '1': 'Session Open / Close / Settlement entry',
            '2': 'Delivery Settlement entry',
            '3': 'Expected entry',
            '4': 'Entry from previous business day',
            '5': 'Theoretical Price value'
        },
        '291': {
            '1': 'Bankrupt',
            '2': 'Pending delisting'
        },
        '292': {
            'A': 'Ex-Dividend',
            'B': 'Ex-Distribution',
            'C': 'Ex-Rights',
            'D': 'New',
            'E': 'Ex-Interest'
        },
        '297': {
            '0': 'Accepted',
            '1': 'Canceled for Symbol (s)',
            '2': 'Canceled for SecurityType (s)',
            '3': 'Canceled for UnderlyingSymbol',
            '4': 'Canceled All',
            '5': 'Rejected',
            '6': 'Removed from Market',
            '7': 'Expired',
            '8': 'Query',
            '9': 'Quote Not Found',
            '10': 'Pending',
            '11': 'Pass',
            '12': 'Locked Market Warning',
            '13': 'Cross Market Warning',
            '14': 'Canceled due to lock market',
            '15': 'Canceled due to cross market'
        },
        '298': {
            '1': 'Cancel for Symbol (s)',
            '2': 'Cancel for SecurityType (s)',
            '3': 'Cancel for UnderlyingSymbol',
            '4': 'Cancel All Quotes'
        },
        '300': {
            '1': 'Unknown symbol (Security)',
            '2': 'Exchange(Security) closed',
            '3': 'Quote Request exceeds limit',
            '4': 'Too late to enter',
            '5': 'Unknown Quote',
            '6': 'Duplicate Quote',
            '7': 'Invalid bid/ask spread',
            '8': 'Invalid price',
            '9': 'Not authorized to quote security',
            '99': 'Other'
        },
        '301': {
            '0': 'No Acknowledgement (Default)',
            '1': 'Acknowledge only negative or erroneous quotes',
            '2': 'Acknowledge each Quote messages'
        },
        '303': {
            '1': 'Manual',
            '2': 'Automatic'
        },
        '305': {
            '1': 'CUSIP',
            '2': 'SEDOL',
            '3': 'QUIK',
            '4': 'ISIN number',
            '5': 'RIC code',
            '6': 'ISO Currency  Code',
            '7': 'ISO Country  Code',
            '8': 'Exchange Symbol',
            '9': 'Consolidated Tape Association (CTA) Symbol (SIAC CTS/CQS line format)',
            'A': 'Bloomberg Symbol',
            'B': 'Wertpapier',
            'C': 'Dutch',
            'D': 'Valoren',
            'E': 'Sicovam',
            'F': 'Belgian',
            'G': '"Common" (Clearstream and Euroclear)',
            'H': 'Clearing House / Clearing Organization',
            'I': 'ISDA/FpML Product Specification',
            'J': 'Options Price Reporting Authority'
        },
        '310': {
            'TREASURY': 'Federal government or treasury',
            'PROVINCE': 'State, province, region, etc.',
            'AGENCY': 'Federal agency',
            'MORTGAGE': 'Mortgage passthrough',
            'CP': 'Commercial paper',
            'CORP': 'Corporate',
            'EQUITY': 'Equity',
            'SUPRA': 'Supra-national agency',
            'CASH': 'Cash'
        },
        '321': {
            '0': 'Request Security identity and specifications',
            '1': 'Request Security identity for the specifications provided (Name of the security is not supplied)',
            '2': 'Request List Security Types',
            '3': 'Request List Securities (Can be qualified with SecurityExchange . If provided then only list Securities for the specific type)'
        },
        '323': {
            '1': 'Accept security proposal as is',
            '2': 'Accept security proposal with revisions as indicated in the message',
            '5': 'Reject security proposal',
            '6': 'Can not match selection criteria'
            },
        '325': {
            'Y': 'Message is being sent unsolicited',
            'N': 'Message is being sent as a result of a prior request'
            },
        '326': {
            '1': 'Opening Delay',
            '2': 'Trading Halt',
            '3': 'Resume',
            '4': 'No Open/No Resume',
            '5': 'Price Indication',
            '6': 'Trading Range Indication',
            '7': 'Market Imbalance Buy',
            '8': 'Market Imbalance Sell',
            '9': 'Market On Close Imbalance Buy',
            '10': 'Market On Close Imbalance Sell',
            '11': '(not assigned)',
            '12': 'No Market Imbalance',
            '13': 'No Market On Close Imbalance',
            '14': 'ITS Pre-Opening',
            '15': 'New Price Indication',
            '16': 'Trade Dissemination Time',
            '17': 'Ready to trade (start of session)',
            '18': 'Not Available for trading (end of session)',
            '19': 'Not Traded on this Market',
            '20': 'Unknown or Invalid',
            '21': 'Pre-Open',
            '22': 'Opening Rotation',
            '23': 'Fast Market'
        },
        '327': {
            'I': 'Order Imbalance',
            'X': 'Equipment Changeover',
            'P': 'News  Pending',
            'D': 'News  Dissemination',
            'E': 'Order Influx',
            'M': 'Additional Information'
        },
        '328': {
            'Y': 'Halt was due to common stock being halted',
            'N': 'Halt was not related to a halt of the common stock'
        },
        '329': {
            'Y': 'Halt was due to related security being halted',
            'N': 'Halt was not related to a halt of the related security'
        },
        '334': {
            '1': 'Cancel',
            '2': 'Error',
            '3': 'Correction'
        },
        '338': {
            '1': 'Electronic',
            '2': 'Open Outcry',
            '3': 'Two Party'
        },
        '339': {
            '1': 'Testing',
            '2': 'Simulated',
            '3': 'Production'
        },
        '340': {
            '0': 'Unknown',
            '1': 'Halted',
            '2': 'Open',
            '3': 'Closed',
            '4': 'Pre-Open',
            '5': 'Pre-Close',
            '6': 'Request Rejected'
        },
        '347': {
            'ISO-2022-JP (for using JIS)': 'ISO-2022-JP (for using JIS)',
            'EUC-JP (for using EUC)': 'EUC-JP (for using EUC)',
            'Shift_JIS (for using SJIS)': 'Shift_JIS (for using SJIS)',
            'UTF-8 (for using Unicode)': 'UTF-8 (for using Unicode)'
        },
        '368': {
            '1': 'Unknown symbol (Security)',
            '2': 'Exchange(Security) closed',
            '3': 'Quote exceeds limit',
            '4': 'Too late to enter',
            '5': 'Unknown Quote',
            '6': 'Duplicate Quote',
            '7': 'Invalid bid/ask spread',
            '8': 'Invalid price',
            '9': 'Not authorized to quote security',
            '99': 'Other'
        },
        '373': {
            '0': 'Invalid tag number',
            '1': 'Required tag missing',
            '2': 'Tag not defined for this message type',
            '3': 'Undefined Tag',
            '4': 'Tag specified without a value',
            '5': 'Value is incorrect (out of range) for this tag',
            '6': 'Incorrect data format for value',
            '7': 'Decryption problem',
            '8': 'Signature  problem',
            '9': 'CompID problem',
            '10': 'SendingTime  accuracy problem',
            '11': 'Invalid MsgType',
            '12': 'XML Validation error',
            '13': 'Tag appears more than once',
            '14': 'Tag specified out of required order',
            '15': 'Repeating group fields out of order',
            '16': 'Incorrect NumInGroup count for repeating group',
            '17': 'Non "Data" value includes field delimiter (<SOH> character)',
            '99': 'Other'
        },
        '374': {
            'N': 'New',
            'C': 'Cancel'
        },
        '377': {
            'Y': 'Was solicitied',
            'N': 'Was not solicited'
        },
        '378': {
            '0': 'GT Corporate action',
            '1': 'GT renewal / restatement (no corporate action)',
            '2': 'Verbal change',
            '3': 'Repricing of order',
            '4': 'Broker option',
            '5': 'Partial decline of OrderQty  (e.g. exchange-initiated partial cancel)',
            '6': 'Cancel on Trading Halt',
            '7': 'Cancel on System Failure',
            '8': 'Market (Exchange) Option',
            '9': 'Canceled, Not Best',
            '10': 'Warehouse recap',
            '99': 'Other'
        },
        '380': {
            '0': 'Other',
            '1': 'Unkown ID',
            '2': 'Unknown Security',
            '3': 'Unsupported Message Type',
            '4': 'Application not available',
            '5': 'Conditionally Required Field Missing',
            '6': 'Not authorized',
            '7': 'DeliverTo firm not available at this time'
        },
        '385': {
            'S': 'Send',
            'R': 'Receive'
        },
        '388': {
            '0': 'Related to displayed price',
            '1': 'Related to market price',
            '2': 'Related to primary price',
            '3': 'Related to local primary price',
            '4': 'Related to midpoint price',
            '5': 'Related to last trade price',
            '6': 'Related to VWAP'
        },
        '394': {
            '1': '"Non Disclosed" Style (e.g. US/European)',
            '2': '"Disclosed" Style (e.g. Japanese)',
            '3': 'No Bidding Process'
        },
        '399': {
            '1': 'Sector',
            '2': 'Country',
            '3': 'Index'
        },
        '401': {
            '1': 'SideValue1',
            '2': 'SideValue2'
        },
        '409': {
            '1': '5day moving average',
            '2': '20 day moving average',
            '3': 'Normal Market Size',
            '4': 'Other'
        },
        '411': {
            'Y': 'True',
            'N': 'False'
        },
        '414': {
            '1': 'BuySide explicitly requests status using StatusRequest (Default) The sell-side firm can however, send a DONE status List Status  Response in an unsolicited fashion',
            '2': 'SellSide periodically sends status using ListStatus. Period optionally specified in ProgressPeriod',
            '3': 'Real-time execution reports (to be discouraged)'
        },
        '416': {
            '1': 'Net',
            '2': 'Gross'
        },
        '418': {
            'R': 'Risk Trade',
            'G': 'VWAP Guarantee',
            'A': 'Agency',
            'J': 'Guaranteed Close'
        },
        '419': {
            '2': 'Closing Price at morning session',
            '3': 'Closing Price',
            '4': 'Current price',
            '5': 'SQ',
            '6': 'VWAP through a day',
            '7': 'VWAP through a morning session',
            '8': 'VWAP through an afternoon session',
            '9': 'VWAP through a day except "YORI" (an opening auction)',
            'A': 'VWAP through a morning session except "YORI" (an opening auction)',
            'B': 'VWAP through an afternoon session except "YORI" (an opening auction)',
            'C': 'Strike',
            'D': 'Open',
            'Z': 'Others'
        },
        '423': {
            '1': 'Percentage (e.g. "dollar price" for fixed income)',
            '2': 'Per unit (i.e. per share or contract)',
            '3': 'Fixed Amount (absolute value)',
            '4': 'Discount - percentage points below par',
            '5': 'Premium - percentage points over par',
            '6': 'Spread',
            '7': 'TED price',
            '8': 'TED yield',
            '9': 'Yield',
            '10': 'Fixed cabinet trade price (primarily for listed futures and options)',
            '11': 'Variable cabinet trade price (primarily for listed futures and options)'
        },
        '427': {
            '0': 'book out all trades on day of execution',
            '1': 'accumulate executions until order is filled or expires',
            '2': 'accumulate until verbally notified otherwise'
        },
        '429': {
            '1': 'Ack',
            '2': 'Response',
            '3': 'Timed',
            '4': 'ExecStarted',
            '5': 'AllDone',
            '6': 'Alert'
        },
        '430': {
            '1': 'Net',
            '2': 'Gross'
        },
        '431': {
            '1': 'InBiddingProcess',
            '2': 'ReceivedForExecution',
            '3': 'Executing',
            '4': 'Canceling',
            '5': 'Alert',
            '6': 'All Done',
            '7': 'Reject'
        },
        '433': {
            '1': 'Immediate',
            '2': 'Wait for Execute Instruction (e.g. a List Execute  message or phone call before proceeding with execution of the list)',
            '3': 'Exchange/switch CIV order - Sell driven',
            '4': 'Exchange/switch CIV order - Buy driven, cash top-up (i.e. additional cash will be provided to fulfil the order)',
            '5': 'Exchange/switch CIV order - Buy driven, cash withdraw (i.e. additional cash will not be provided to fulfil the order)'
        },
        '434': {
            '1': 'Order Cancel Request',
            '2': 'Order Cancel/Replace Request'
        },
        '442': {
            '1': 'Single Security (default if not specified)',
            '2': 'Individual leg of a multi-leg security',
            '3': 'Multi-leg security'
        },
        '447': {
            'B': 'BIC (Bank Identification Code—Swift managed) code (ISO 9362 – See Appendix 6-B)',
            'C': 'Generally accepted market participant identifier (e.g. NASD mnemonic)',
            'D': 'Proprietary/Custom code',
            'E': 'ISO Country Code',
            'F': 'Settlement Entity Location (note if Local Market Settlement use "E = ISO Country Code") (see Appendix 6-G for valid values)',
            'G': 'MIC (ISO 10383 - Market Identifier Code) (See Appendix 6-C)',
            'H': 'CSD participant/member code (e.g. Euroclear, DTC, CREST or Kassenverein number)',
            '1': 'Korean Investor ID',
            '2': 'Taiwanese Qualified Foreign Investor ID QFII / FID',
            '3': 'Taiwanese Trading Account',
            '4': 'Malaysian Central Depository (MCD) number',
            '5': 'Chinese B Share (Shezhen and Shanghai)',
            '6': 'UK National Insurance or Pension Number',
            '7': 'US Social Security Number',
            '8': 'US Employer Identification Number',
            '9': 'Australian Business Number',
            'A': 'Australian Tax File Number',
            'I': 'Directed broker three character acronym as defined in ISITC "ETC Best Practice" guidelines document'
        },
        '456': {
            '1': 'CUSIP',
            '2': 'SEDOL',
            '3': 'QUIK',
            '4': 'ISIN number',
            '5': 'RIC code',
            '6': 'ISO Currency  Code',
            '7': 'ISO Country  Code',
            '8': 'Exchange Symbol',
            '9': 'Consolidated Tape Association (CTA) Symbol (SIAC CTS/CQS line format)',
            'A': 'Bloomberg Symbol',
            'B': 'Wertpapier',
            'C': 'Dutch',
            'D': 'Valoren',
            'E': 'Sicovam',
            'F': 'Belgian',
            'G': '"Common" (Clearstream and Euroclear)',
            'H': 'Clearing House / Clearing Organization',
            'I': 'ISDA/FpML Product Specification',
            'J': 'Options Price Reporting Authority'
        },
        '459': {
            '1': 'CUSIP',
            '2': 'SEDOL',
            '3': 'QUIK',
            '4': 'ISIN number',
            '5': 'RIC code',
            '6': 'ISO Currency  Code',
            '7': 'ISO Country  Code',
            '8': 'Exchange Symbol',
            '9': 'Consolidated Tape Association (CTA) Symbol (SIAC CTS/CQS line format)',
            'A': 'Bloomberg Symbol',
            'B': 'Wertpapier',
            'C': 'Dutch',
            'D': 'Valoren',
            'E': 'Sicovam',
            'F': 'Belgian',
            'G': '"Common" (Clearstream and Euroclear)',
            'H': 'Clearing House / Clearing Organization',
            'I': 'ISDA/FpML Product Specification',
            'J': 'Options Price Reporting Authority'
        },
        '460': {
            '1': 'AGENCY',
            '2': 'COMMODITY',
            '3': 'CORPORATE',
            '4': 'CURRENCY',
            '5': 'EQUITY',
            '6': 'GOVERNMENT',
            '7': 'INDEX',
            '8': 'LOAN',
            '9': 'MONEYMARKET',
            '10': 'MORTGAGE',
            '11': 'MUNICIPAL',
            '12': 'OTHER',
            '13': 'FINANCING',
        },
        '462': {
            '1': 'AGENCY',
            '2': 'COMMODITY',
            '3': 'CORPORATE',
            '4': 'CURRENCY',
            '5': 'EQUITY',
            '6': 'GOVERNMENT',
            '7': 'INDEX',
            '8': 'LOAN',
            '9': 'MONEYMARKET',
            '10': 'MORTGAGE',
            '11': 'MUNICIPAL',
            '12': 'OTHER',
            '13': 'FINANCING'
        },
        '464': {
            'Y': 'True (Test)',
            'N': 'False (Production)'
        },
        '465': {
            '1': 'SHARES',
            '2': 'BONDS',
            '3': 'CURRENTFACE',
            '4': 'ORIGINALFACE',
            '5': 'CURRENCY',
            '6': 'CONTRACTS',
            '7': 'OTHER',
            '8': 'PAR'
        },
        '481': {
            'Y': 'Passed',
            'N': 'Not checked',
            '1': 'Exempt - Below The Limit',
            '2': 'Exempt - Client Money Type Exemption',
            '3': 'Exempt - Authorised Credit or Financial Institution.'
        },
        '487': {
            '0': 'New',
            '1': 'Cancel',
            '2': 'Replace',
            '3': 'Release',
            '4': 'Reverse'
        },
        '506': {
            'A': 'Accepted',
            'R': 'Rejected',
            'H': 'Held',
            'N': 'Reminder - i.e. Registration Instructions  are still outstanding'
        },
        '514': {
            '0': 'New',
            '1': 'Replace',
            '2': 'Cancel'
        },
        '517': {
            '2': 'Joint Trustees',
            'J': 'Joint Investors',
            'T': 'Tenants in Common'
        },
        '522': {
            '1': 'Individual Investor',
            '2': 'Public Company',
            '3': 'Private Company',
            '4': 'Individual Trustee',
            '5': 'Company Trustee',
            '6': 'Pension Plan',
            '7': 'Custodian Under Gifts to Minors Act',
            '8': 'Trusts',
            '9': 'Fiduciaries',
            '10': 'Networking Sub-Account',
            '11': 'Non-Profit Organization',
            '12': 'Corporate Body',
            '13': 'Nominee'
        },
        '528': {
            'A': 'Agency',
            'G': 'Proprietary',
            'I': 'Individual',
            'P': 'Principal (Note for CMS purposes, Principal includes Proprietary)',
            'R': 'Riskless Principal',
            'W': 'Agent for Other Member'
        },
        '529': {
            '1': 'Program Trade',
            '2': 'Index Arbitrage',
            '3': 'Non-Index Arbitrage',
            '4': 'Competing Market Maker',
            '5': 'Acting as Market Maker or Specialist in the security',
            '6': 'Acting as Market Maker or Specialist in the underlying security of a derivative security',
            '7': 'Foreign Entity (of foreign government or regulatory jurisdiction)',
            '8': 'External Market Participant',
            '9': 'External Inter-connected Market Linkage',
            'A': 'Riskless Arbitrage'
        },
        '530': {
            '1': 'Cancel orders for a security',
            '2': 'Cancel orders for an Underlying security',
            '3': 'Cancel orders for a Product',
            '4': 'Cancel orders for a CFICode',
            '5': 'Cancel orders for a SecurityType',
            '6': 'Cancel orders for a trading session',
            '7': 'Cancel all orders'
        },
        '531': {
            '0': 'Cancel Request Rejected - See MassCancelRejectReason',
            '1': 'Cancel orders for a security',
            '2': 'Cancel orders for an Underlying security',
            '3': 'Cancel orders for a Product',
            '4': 'Cancel orders for a CFICode',
            '5': 'Cancel orders for a SecurityType',
            '6': 'Cancel orders for a trading session',
            '7': 'Cancel all orders'
        },
        '532': {
            '0': 'Mass Cancel Not Supported',
            '1': 'Invalid or unknown Security',
            '2': 'Invalid or unknown Underlying security',
            '3': 'Invalid or unknown Product',
            '4': 'Invalid or unknown CFICode',
            '5': 'Invalid or unknown SecurityType',
            '6': 'Invalid or unknown trading session',
            '99': 'Other'
        },
        '537': {
            '0': 'Indicative',
            '1': 'Tradeable',
            '2': 'Restricted Tradeable',
            '3': 'Counter (tradable)'
        },
        '543': {
            'BIC (Bank Identification Code—Swift managed)': 'the depository or custodian who maintains ownership Records',
            'ISO Country  Code': 'country in which registry is kept',
            '"ZZ"': 'physical or bearer'
        },
        '544': {
            '1': 'Cash',
            '2': 'Margin Open',
            '3': 'Margin Close'
        },
        '546': {
            '1': 'Local (Exchange, ECN, ATS)',
            '2': 'National',
            '3': 'Global'
        },
        '547': {
            'Y': 'Client has responsibility for implicitly deleting bids or offers falling outside the MarketDepth  of the request.',
            'N': 'Server must send an explicit delete for bids or offers falling outside the requested MarketDepth  of the request.'
        },
        '549': {
            '1': 'Cross Trade which is executed completely or not. Both sides are treated in the same manner. This is equivalent to an All',
            '2': 'Cross Trade which is executed partially and the rest is cancelled. One side is fully executed, the other side is partially'
        },
        '552': {
            '1': 'one side',
            '2': 'both sides'
        },
        '559': {
            '0': 'Symbol',
            '1': 'CFICode',
            '2': 'Product',
            '3': 'TradingSessionID',
            '4': 'All Securities'
        },
        '560': {
            '0': 'Valid request',
            '1': 'Invalid or unsupported request',
            '2': 'No instruments found that match selection criteria',
            '3': 'Not authorized to retrieve instrument data',
            '4': 'data temporarily unavailable',
            '5': 'Request for instrument data not supported'
        },
        '567': {
            '1': 'Unknown or invalid TradingSessionID',
            '99': 'Other'
        },
        '569': {
            '0': 'All trades',
            '1': 'Matched trades matching Criteria provided on request (parties, exec id, trade id, order id, instrument, input source, etc.)',
            '2': 'Unmatched trades that match criteria',
            '3': 'Unreported trades that match criteria',
            '4': 'Advisories that match criteria'
        },
        '570': {
            'Y': 'previously reported to counterparty',
            'N': 'not reported to counterparty'
        },
        '573': {
            '0': 'compared, matched or affirmed',
            '1': 'uncompared, unmatched, or unaffirmed',
            '2': 'advisory or alert'
        },
        '574': {
            'A1': 'Exact match on Trade Type , and Special Trade Indicator plus four badges and execution time (within two-minute window)',
            'A2': 'Exact match on Trade Date, Stock Symbol, Quantity, Price, Trade Type, and Special Trade Indicator plus four badges',
            'A3': 'Exact match on Trade Date, Stock Symbol, Quantity, Price, Trade Type, and Special Trade Indicator plus two badges and execution time (within two-minute window)',
            'A4': 'Exact match on Trade Date, Stock Symbol, Quantity, Price, Trade Type, and Special Trade Indicator plus two badges',
            'A5': 'Exact match on Trade Date, Stock Symbol, Quantity, Price, Trade Type, and Special Trade Indicator plus execution time (within two-minute window)',
            'AQ': 'Compared records resulting from stamped advisories or specialist accepts/pair-offs',
            'S1 to S5': 'Summarized Match using A1 to A5 exact match criteria except quantity is summarized',
            'M1': 'Exact Match on Trade Date, Stock Symbol, Quantity, Price, Trade Type, and Special Trade Indicator minus badges and times',
            'M2': 'Summarized Match minus badges and times',
            'MT': 'OCS Locked In',
            'M1': 'ACT M1 Match',
            'M2': 'ACT M2 Match',
            'M3': 'ACT Accepted Trade',
            'M4': 'ACT Default Trade',
            'M5': 'ACT Default After M2',
            'M6': 'ACT M6 Match',
            'MT': 'Non-ACT'
        },
        '577': {
            '0': 'process normally',
            '1': 'exclude from all netting',
            '2': 'bilateral netting only',
            '3': 'ex clearing',
            '4': 'special trade',
            '5': 'multilateral netting',
            '6': 'clear against central counterparty',
            '7': 'exclude from central counterparty',
            '8': 'Manual mode (pre-posting and/or pre-giveup)',
            '9': 'Automatic posting mode (trade posting to the position account number specified)',
            '10': 'Automatic give-up mode (trade give-up to the give-up destination number specified)',
            '11': 'Qualified Service Representative (QSR)',
            '12': 'Customer Trade',
            '13': 'Self clearing'
        },
        '581': {
            '1': 'Account is carried on customer Side of Books',
            '2': 'Account is carried on non-customer Side of books',
            '3': 'House Trader',
            '4': 'Floor Trader',
            '6': 'Account is carried on non-customer side of books and is cross margined',
            '7': 'Account is house trader and is cross margined',
            '8': 'Joint Backoffice Account (JBO)'
        },
        '585': {
            '1': 'Status for orders for a security',
            '2': 'Status for orders for an Underlying security',
            '3': 'Status for orders for a Product',
            '4': 'Status for orders for a CFICode',
            '5': 'Status for orders for a SecurityType',
            '6': 'Status for orders for a trading session',
            '7': 'Status for all orders',
            '8': 'Status for orders for a PartyID'
        },
        '589': {
            '0': 'Can trigger booking without reference to the order initiator ("auto")',
            '1': 'Speak with order initiator before booking ("speak first")',
            '2': 'Accumulate'
        },
        '590': {
            '0': 'Each partial execution is a bookable unit',
            '1': 'Aggregate partial executions on this order, and book one trade per order',
            '2': 'Aggregate executions for this symbol, side, and settlement date'
        },
        '591': {
            '0': 'Pro-rata',
            '1': 'Do not pro-rata = discuss first'
        },
        '626': {
            '1': 'Calculated (includes MiscFees and NetMoney )',
            '2': 'Preliminary (without MiscFees and NetMoney )',
            '7': 'Warehouse instruction',
            '8': 'Request to Intermediary'
        },
        '636': {
            'Y': 'Order is currently being worked',
            'N': 'Order has been accepted but not yet in a working state'
        },
        '638': {
            '0': 'Priority Unchanged',
            '1': 'Lost Priority as result of order change'
        },
        '650': {
            'Y': 'Legal confirm',
            'N': 'Does not constitute a legal confirm'
        },
        '658': {
            '1': 'Unknown symbol (Security)',
            '2': 'Exchange(Security) closed',
            '3': 'Quote Request  exceeds limit',
            '4': 'Too late to enter',
            '5': 'Invalid price',
            '6': 'Not authorized to request quote',
            '7': 'No match for inquiry',
            '8': 'No market for instrument',
            '9': 'No inventory',
            '10': 'Pass',
            '99': 'Other'
        },
        '660': {
            '1': 'BIC',
            '2': 'SID code',
            '3': 'TFM (GSPTA)',
            '4': 'OMGEO (AlertID)',
            '5': 'DTCC code',
            '99': 'Other (custom or proprietary)'
        },
        '665': {
            '1': 'Received',
            '2': 'Mismatched account',
            '3': 'Missing settlement instructions',
            '4': 'Confirmed',
            '5': 'Request rejected'
        },
        '666': {
            '0': 'New',
            '1': 'Replace',
            '2': 'Cancel'
        },
        '668': {
            '1': 'BookEntry (default)',
            '2': 'Bearer'
        },
        '690': {
            '1': 'Par For Par',
            '2': 'Modified Duration',
            '4': 'Risk',
            '5': 'Proceeds'
        },
        '692': {
            '1': 'percent (percent of par)',
            '2': 'per share (e.g. cents per share)',
            '3': 'fixed amount (absolute value)',
            '4': 'discount - percentage points below par',
            '5': 'premium - percentage points over par',
            '6': 'basis points relative to benchmark',
            '7': 'TED price',
            '8': 'TED yield',
            '9': 'Yield spread (swaps)',
            '10': 'Yield'
        },
        '694': {
            '1': 'Hit/Lift',
            '2': 'Counter',
            '3': 'Expired',
            '4': 'Cover',
            '5': 'Done Away',
            '6': 'Pass'
        },
        '703': {
            'TQ': 'Transaction Quantity',
            'IAS': 'Intra-Spread Qty',
            'IES': 'Inter-Spread Qty',
            'FIN': 'End-of-Day Qty',
            'SOD': 'Start-of-Day Qty',
            'EX': 'Option Exercise Qty',
            'AS': 'Option Assignment',
            'TX': 'Transaction from Exercise',
            'TA': 'Transaction from Assignment',
            'PIT': 'Pit Trade Qty',
            'TRF': 'Transfer Trade Qty',
            'ETR': 'Electronic Trade Qty',
            'ALC': 'Allocation Trade Qty',
            'PA': 'Adjustment Qty',
            'ASF': 'As-of Trade Qty',
            'DLV': 'Delivery Qty',
            'TOT': 'Total Transaction Qty',
            'XM': 'Cross Margin Qty',
            'SPL': 'Integral Split'
        },
        '706': {
            '0': 'Submitted',
            '1': 'Accepted',
            '2': 'Rejected'
        },
        '707': {
            'FMTM': 'Final Mark-to-Market Amount',
            'IMTM': 'Incremental Mark-to-Market Amount',
            'TVAR': 'Trade Variation Amount',
            'SMTM': 'Start-of-Day Mark-to-Market Amount',
            'PREM': 'Premium Amount',
            'CRES': 'Cash Residual Amount',
            'CASH': 'Cash Amount (Corporate Event)',
            'VADJ': 'Value Adjusted Amount'
        },
        '709': {
            '1': 'Exercise',
            '2': 'Do Not Exercise',
            '3': 'Position Adjustment',
            '4': 'Position Change Submission/Margin Disposition',
            '5': 'Pledge'
        },
        '712': {
            '1': 'New: used to increment the overall transaction quantity',
            '2': 'Replace: used to override the overall transaction quantity or specific add messages based on the reference id',
            '3': 'Cancel: used to remove the overall transaction or specific add messages based on reference id'
        },
        '718': {
            '0': 'Process request as Margin Disposition',
            '1': 'Delta_plus',
            '2': 'Delta_minus',
            '3': 'Final'
        },
        '722': {
            '0': 'Accepted',
            '1': 'Accepted with Warnings',
            '2': 'Rejected',
            '3': 'Completed',
            '4': 'Completed with Warnings'
        },
        '723': {
            '0': 'Successful completion - no warnings or errors',
            '1': 'Rejected',
            '99': 'Other'
        },
        '724': {
            '0': 'Positions',
            '1': 'Trades',
            '2': 'Exercises',
            '3': 'Assignments'
        },
        '725': {
            '0': 'Inband: transport the request was sent over (Default)',
            '1': 'Out-of-Band: pre-arranged out of band delivery mechanism (i.e. FTP, HTTP, NDM, etc) between counterparties. Details specified'
        },
        '728': {
            '0': 'Valid Request',
            '1': 'Invalid or unsupported Request',
            '2': 'No positions found that match criteria',
            '3': 'Not authorized to request positions',
            '4': 'Request for Position not supported',
            '99': 'Other (use Text  in conjunction with this code for an explanation)'
        },
        '729': {
            '0': 'Completed',
            '1': 'Completed with Warnings',
            '2': 'Rejected'
        },
        '731': {
            '1': 'Final',
            '2': 'Theoretical'
        },
        '744': {
            'R': 'Random',
            'P': 'ProRata'
        },
        '747': {
            'A': 'Automatic',
            'M': 'Manual'
        },
        '749': {
            '0': 'Successful (Default)',
            '1': 'Invalid or unknown instrument',
            '2': 'Invalid type of trade requested',
            '3': 'Invalid parties',
            '4': 'Invalid Transport Type requested',
            '5': 'Invalid Destination requested',
            '8': 'TradeRequestType  not supported',
            '9': 'Unauthorized for Trade Capture Report Request',
            '99': 'Other'
        },
        '751': {
            '0': 'Successful (Default)',
            '1': 'Invalid party information',
            '2': 'Unknown instrument',
            '3': 'Unauthorized to report trades',
            '4': 'Invalid trade type',
            '99': 'Other'
        },
        '752': {
            '1': 'Single Security (default if not specified)',
            '2': 'Individual leg of a multileg security',
            '3': 'Multileg security'
        },
        '770': {
            '1': 'Execution Time',
            '2': 'Time In',
            '3': 'Time Out',
            '4': 'Broker Receipt',
            '5': 'Broker Execution'
        },
        '773': {
            '1': 'Status',
            '2': 'Confirmation',
            '3': 'Text (field)'
        },
        '774': {
            '1': 'Mismatched account',
            '2': 'Missing settlement instructions',
            '99': 'Other'
        },
        '775': {
            '0': 'Regular booking',
            '1': 'CFD (Contract For Difference)',
            '2': 'Total return swap'
        },
        '780': {
            '0': 'use default instructions',
            '1': 'derive from parameters provided',
            '2': 'full details provided',
            '3': 'SSI db ids provided',
            '4': 'phone for instructions'
        },
        '787': {
            'S': 'securities',
            'C': 'cash'
        },
        '788': {
            '1': 'Overnight',
            '2': 'Term',
            '3': 'Flexible',
            '4': 'Open'
        },
        '792': {
            '0': 'unable to process request (e.g. database unavailable)',
            '1': 'unknown account',
            '2': 'no matching settlement instructions found',
            '99': 'other'
        },
        '794': {
            '3': 'Sellside Calculated Using Preliminary (includes MiscFees and NetMoney )',
            '4': 'Sellside Calculated Without Preliminary (sent unsolicited by sellside, includes MiscFees and NetMoney )',
            '5': 'Warehouse recap',
            '8': 'Request to Intermediary'
        },
        '796': {
            '1': 'Original details incomplete/incorrect',
            '2': 'Change in underlying order details',
            '99': 'Other'
        },
        '798': {
            '1': 'Account is carried on customer Side of Books',
            '2': 'Account is carried on non-Customer Side of books',
            '3': 'House Trader',
            '4': 'Floor Trader',
            '6': 'Account is carried on non-customer side of books and is cross margined',
            '7': 'Account is house trader and is cross margined',
            '8': 'Joint Backoffice Account (JBO)'
        },
        '808': {
            '1': 'Pending Accept',
            '2': 'Pending Release',
            '3': 'Pending Reversal',
            '4': 'Accept',
            '5': 'Block Level Reject',
            '6': 'Account Level Reject'
        },
        '814': {
            '0': 'No action taken',
            '1': 'Queue flushed',
            '2': 'Overlay last',
            '3': 'End session'
        },
        '815': {
            '0': 'No action taken',
            '1': 'Queue flushed',
            '2': 'Overlay last',
            '3': 'End session'
        },
        '819': {
            '0': 'No Average Pricing',
            '1': 'Trade is part of an average price group identified by the TradeLinkID',
            '2': 'Last Trade in the average price group identified by the TradeLinkID'
        },
        '826': {
            '0': 'Allocation not required',
            '1': 'Allocation required (give up trade) allocation information not provided (incomplete)',
            '2': 'Use allocation provided with the trade'
        },
        '827': {
            '0': 'Expire on trading session close (default)',
            '1': 'Expire on trading session open'
        },
        '828': {
            '0': 'Regular Trade',
            '1': 'Block Trade',
            '2': 'EFP (Exchange for Physical)',
            '3': 'Transfer',
            '4': 'Late Trade',
            '5': 'T Trade',
            '6': 'Weighted Average Price Trade',
            '7': 'Bunched Trade',
            '8': 'Late Bunched Trade',
            '9': 'Prior Reference Price Trade',
            '10': 'After Hours Trade'
        },
        '835': {
            '0': 'Floating (default)',
            '1': 'Fixed'
        },
        '836': {
            '0': 'Price (default)',
            '1': 'Basis Points',
            '2': 'Ticks',
            '3': 'Price Tier / Level'
        },
        '837': {
            '0': 'Or better (default) - price improvement allowed',
            '1': 'Strict - limit is a strict limit',
            '2': 'Or worse - for a buy the peg limit is a minimum and for a sell the peg limit is a maximum (for use for orders which have a price range)'
        },
        '838': {
            '1': 'More aggressive - on a buy order round the price up round up to the nearest tick, on a sell round down to the nearest tick',
            '2': 'More passive - on a buy order round down to nearest tick on a sell order round up to nearest tick'
        },
        '840': {
            '1': 'Local (Exchange, ECN, ATS)',
            '2': 'National',
            '3': 'Global',
            '4': 'National excluding local',
        },
        '841': {
            '0': 'Floating (default)',
            '1': 'Fixed'
        },
        '842': {
            '0': 'Price (default)',
            '1': 'Basis Points',
            '2': 'Ticks',
            '3': 'Price Tier / Level'
        },
        '843': {
            '0': 'Or better (default) - price improvement allowed',
            '1': 'Strict - limit is a strict limit',
            '2': 'Or worse - for a buy the discretion price is a minimum and for a sell the discretion price is a maximum (for use for orders which have a price range)'
        },
        '844': {
            '1': 'More aggressive - on a buy order round the price up round up to the nearest tick, on a sell round down to the nearest tick',
            '2': 'More passive - on a buy order round down to nearest tick on a sell order round up to nearest tick'
        },
        '846': {
            '1': 'Local (Exchange, ECN, ATS)',
            '2': 'National',
            '3': 'Global',
            '4': 'National excluding local'
        },
        '851': {
            '1': 'Added Liquidity',
            '2': 'Removed Liquidity',
            '3': 'Liquidity Routed Out'
        },
        '852': {
            'Y': 'Report trade',
            'N': 'Do not report trade'
        },
        '853': {
            '0': 'Dealer Sold Short',
            '1': 'Dealer Sold Short Exempt',
            '2': 'Selling Customer Sold Short',
            '3': 'Selling Customer Sold Short Exempt',
            '4': 'Qualifed Service Representative (QSR) or Automatic Giveup (AGU) Contra Side Sold Short',
            '5': 'QSR or AGU Contra Side Sold Short Exempt'
        },
        '854': {
            '0': 'Units (shares, par, currency)',
            '1': 'Contracts (if used - should specify ContractMultiplier )'
        },
        '856': {
            '0': 'Submit',
            '1': 'Alleged',
            '2': 'Accept',
            '3': 'Decline',
            '4': 'Addendum',
            '5': 'No/Was',
            '6': 'Trade Report Cancel',
            '7': 'Locked In Trade Break'
        },
        '857': {
            '0': 'Not specified',
            '1': 'Explicit list provided'
        },
        '865': {
            '1': 'Put',
            '2': 'Call',
            '3': 'Tender',
            '4': 'Sinking Fund Call',
            '99': 'Other'
        },
        '871': {
            '1': 'Flat (securities pay interest on a current basis but are traded without interest)',
            '2': 'Zero coupon',
            '3': 'Interest bearing (for Euro commercial paper when not issued at discount)',
            '4': 'No periodic payments',
            '5': 'Variable rate',
            '6': 'Less fee for put',
            '7': 'Stepped coupon',
            '8': 'Coupon period (if not semi-annual). Supply redemption date in the InstrAttribValue field',
            '9': 'When [and if] issued',
            '10': 'Original issue discount',
            '11': 'Callable, puttable',
            '12': 'Escrowed to Maturity',
            '13': 'Escrowed to redemption date - callable. Supply redemption date in the InstrAttribValue field',
            '14': 'Prerefunded',
            '15': 'In default',
            '16': 'Unrated',
            '17': 'Taxable',
            '18': 'Indexed',
            '19': 'Subject to Alternative Minimum Tax',
            '20': 'Original issue discount price. Supply price in the InstrAttribValue field',
            '21': 'Callable below maturity value',
            '22': 'Callable without notice by mail to holder unless registered',
            '99': 'Text. Supply the text of the attribute or disclaimer in the InstrAttribValue field'
        },
        '875': {
            '1': '3(a)(3)',
            '2': '4(2)',
            '99': 'Other'
        },
        '891': {
            '0': 'Absolute',
            '1': 'Per unit',
            '2': 'Percentage'
        },
        '893': {
            'Y': 'Last message',
            'N': 'Not last message'
        },
        '895': {
            '0': 'Initial',
            '1': 'Scheduled',
            '2': 'Time Warning',
            '3': 'Margin Deficiency',
            '4': 'Margin Excess',
            '5': 'Forward Collateral Demand',
            '6': 'Event of default',
            '7': 'Adverse tax event'
        },
        '896': {
            '0': 'Trade Date',
            '1': 'GC Instrument',
            '2': 'CollateralInstrument',
            '3': 'Substitution Eligible',
            '4': 'Not Assigned',
            '5': 'Partially Assigned',
            '6': 'Fully Assigned',
            '7': 'Outstanding Trades (Today &lt; end date)'
        },
        '903': {
            '0': 'New',
            '1': 'Replace',
            '2': 'Cancel',
            '3': 'Release',
            '4': 'Reverse'
        },
        '905': {
            '0': 'Received',
            '1': 'Accepted',
            '2': 'Declined',
            '3': 'Rejected'
        },
        '906': {
            '0': 'Unknown deal (order / trade)',
            '1': 'Unknown or invalid instrument',
            '2': 'Unauthorized transaction',
            '3': 'Insufficient collateral',
            '4': 'Invalid type of collateral',
            '5': 'Excessive substitution',
            '99': 'Other'
        },
        '910': {
            '0': 'Unassigned',
            '1': 'Partially Assigned',
            '2': 'Assignment Proposed',
            '3': 'Assigned (Accepted)',
            '4': 'Challenged'
        },
        '912': {
            'Y': 'Last message',
            'N': 'Not last message'
        },
        '919': {
            '0': '"Versus. Payment": Deliver (if Sell) or Receive (if Buy) vs. (Against) Payment',
            '1': '"Free": Deliver (if Sell) or Receive (if Buy) Free',
            '2': 'Tri-Party',
            '3': 'Hold In Custody'
        },
        '924': {
            '1': 'LogOnUser',
            '2': 'LogOffUser',
            '3': 'ChangePasswordForUser',
            '4': 'Request Individual User Status'
        },
        '926': {
            '1': 'Logged In',
            '2': 'Not Logged In',
            '3': 'User Not Recognised',
            '4': 'Password Incorrect',
            '5': 'Password Changed',
            '6': 'Other'
        },
        '928': {
            '1': 'Connected',
            '2': 'Not connected - down expected up',
            '3': 'Not connected - down expected down',
            '4': 'In Process'
        },
        '935': {
            '1': 'Snapshot',
            '2': 'Subscribe',
            '4': 'Stop subscribing',
            '8': 'Level of detail, then NoCompIDs becomes required'
        },
        '937': {
            '1': 'Full',
            '2': 'Incremental update'
        },
        '939': {
            '0': 'Accepted',
            '1': 'Rejected'
        },
        '940': {
            '1': 'Received',
            '2': 'Confirm rejected, i.e. not affirmed',
            '3': 'Affirmed'
        },
        '944': {
            '0': 'Retain',
            '1': 'Add',
            '2': 'Remove'
        },
        '945': {
            '0': 'Accepted',
            '1': 'Accepted with Warnings',
            '2': 'Completed',
            '3': 'Completed with Warnings',
            '4': 'Rejected' 
        },
        '946': {
            '0': 'Successful (Default)',
            '1': 'Invalid or unknown instrument',
            '2': 'Invalid or unknown collateral type',
            '3': 'Invalid parties',
            '4': 'Invalid Transport Type requested',
            '5': 'Invalid Destination requested',
            '6': 'No collateral found for the trade specified',
            '7': 'No collateral found for the order specified',
            '8': 'Collateral Inquiry type not supported',
            '9': 'Unauthorized for collateral inquiry',
            '99': 'Other (further information in Text  field)'
        }
    }

    with open("C:\\temp\\python\\fix_parser\\sample_fix_log.log", "r") as myfile:
        # import fix tags as dictionary
        

        # figure out if this is FIX 4.2 or FIX 4.4
        # parse each line for FIX tags
        for line in myfile:
            # delimiter is ^ or | or SOH \u0001 == unicode escape
            delimiter = 'â˜º' # which is \u0001
            # remember, there are certain fields that can occur multiple times in a line e.g., fills
            for fieldvaluepair in line.split(delimiter):
                # print(fieldvaluepair)
                (individualfield, individualvalue) = fieldvaluepair.split('=')
                # this, except for fills, placements, quantity fields, etc.
                if individualfield in fix42fields:
                    print(fix42dict[individualfield] + '\t' + fix42fields[individualfield][individualvalue])
                else:
                    print(fix42dict[individualfield] + '\t' + str(individualvalue))
        # eventually want to build a dataframe (start with list of lists)
        # output 1: flatfile (text, csv)
        # output 2: Excel
        # sort order?

parse_file()
