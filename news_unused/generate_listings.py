# this file is unused, but can be useful for future improvements to the news article data collection

# import urllib.request

# def get_listings() -> dict:
#     nasdaq_symbols_companies = {}
#     file = urllib.request.urlopen("ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt")
#     for line in file:
#         decoded_line = line.decode("utf-8")
#         if "NASDAQ TEST STOCK" not in decoded_line and "Symbol|" not in decoded_line and "File Creation Time" not in decoded_line and "Nasdaq Symbology Test" not in decoded_line:
#             listing_info = decoded_line.split('|')
#             company = listing_info[1]
#             if " etf" in company.lower():
#                 company = company[:company.lower().find(" ETF")]
#             if " index fund" in company.lower():
#                 company = company[:company.lower().find(" index fund")]
#             if " - " in company:
#                 company = company[:listing_info[1].find(" - ")]
#             nasdaq_symbols_companies[listing_info[0]] = company
#     file = urllib.request.urlopen("ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt")
#     for line in file:
#         decoded_line = line.decode("utf-8")
#         if "NASDAQ TEST STOCK" not in decoded_line and "Symbol|" not in decoded_line and "File Creation Time" not in decoded_line and "Nasdaq Symbology Test" not in decoded_line:
#             listing_info = decoded_line.split('|')
#             company = listing_info[1]
#             if " etf" in company.lower():
#                 company = company[:company.lower().find(" etf")]
#             if " index fund" in company.lower():
#                 company = company[:company.lower().find(" index fund")]
#             if " common s" in company.lower():
#                 company = company[:company.lower().find(" common s")]
#             if ". " in company:
#                 company = company[:listing_info[1].find(". ") + 1]
#             nasdaq_symbols_companies[listing_info[0]] = company
#     return nasdaq_symbols_companies
