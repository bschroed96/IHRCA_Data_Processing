import sys
sys.path.insert(0, r'c:\users\admin\dash\ihrca\lib\site-packages')
from bs4 import BeautifulSoup
import re
import csv

langs = ['English', 'Spanish', 'Swedish', 'Croatian', 'Ukrainian']

lang_dict = {"English": "eng", "Spanish": "spa", "Swedish": "swe", "Croatian": "hrv",
             "Ukrainian": "ukr", "French": "fre", "Polish": "pol", "German": "ger",
             "Czech": "cze", "Slovak": "slo", "Armenian": "arm", "Belarusian": "bel",
             "Slovenian": "slv", "Slovak": "slo", "Estonian": "est", "Greek": "gre",
             "Hungarian": "hun", "Italian": "ita", "Latvian": "lav", "Lithuanian": "lit",
             "Serbian": "-scc"}

def get_strong(htmlfile):
    for item in htmlfile.find_all("strong"):
        print(item.text)


def get_p(htmlfile):
    for text in htmlfile.find_all("p"):
        print(text)


def remove_strong(htmlfile):
    for text in htmlfile.find_all("strong"):
        text.replace_with("")


def get_alt_title(htmlfile):
    remove_strong(htmlfile)
    for line in soup.find_all('p'):
        stringy = str(line.text.partition('.')[0])
        try:
            stringy = re.search('\(([^)]+)', stringy).group(1)
        except AttributeError:
            print(stringy)
            continue
        print(stringy)


def get_title(htmlfile, primary_lang='eng'):
    output_title = sys.argv[1]
    cut_ind = output_title.find('.')
    output_title = output_title[:cut_ind]

    csvfile = open('./output_csvs/' + output_title + '.csv', 'w', newline='')
    file_writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    file_writer.writerow(['Title', 'Place of publication', 'Date range of issues',
                          'Only one issue?', 'Primary Language', 'Secondary language',
                          'Format (print/microfilm', 'Condition', 'Periodical/Newspaper',
                          'Priority (L/M/H)', 'Plans for digitization', 'Alt title', 'Notes'])
    serial_news = 'N'
    for title in htmlfile.find_all('p'):
        # Parse for Serial or Newspaper
        serial = title.find_previous_sibling('a')
        # print(serial)
        if serial_news == 'N' and serial["id"] == 'serials':
            serial_news = 'P'
            # print(serial["id"])

        # parse location of publication
        start = title.text.find(',')
        location = ''
        if start != -1:
            location = title.text[start+2:]
        start = location.find('.')
        if start != -1:
            location = str(location[:start])
        # print(location)

        # Parse Date range of publication
        start = title.text.find(':')
        date_range = ''
        if start != -1:
            date_range = str(title.text[start+2:])
            end = date_range.find('.')
            date_range = date_range[:end]
        # print(date_range)

        # Parse Format print or microfilm
        # print(title.text)
        text_type = 'P'
        if re.search('microfilm', title.text, re.IGNORECASE):
            # print("Microfilm")
            text_type = 'M'

        # Get microfilm Date range
        if text_type == 'M':
            ind = title.text.find('Microfilm')
            if ind != -1:
                ind += 10
                end = title.text[ind:]
                end_ind = end.find('.')
                # print(end_ind)
                micro_date = end[:end_ind-1]
                if bool(re.search(r'\d', micro_date)):
                    print(micro_date)
                    date_range += '; microfilm:' + micro_date
                    print(date_range)

        # # Parse Secondary Language
        # secondary_langs = ""
        # for lang, code in lang_dict.items():
        #     if title.text.find(lang) != -1:
        #         print("HERE=================================================================")
        #         secondary_langs += (code + ',')
        # print(secondary_langs)


        # parse title and alternative title
        # write to csv file
        primary_title = str(title.text.partition(',')[0])
        alt_title = ''
        try:
            alt_title = re.search('\(([^)]+)', primary_title).group(1)
            start = primary_title.find('(')
            if start != -1:
                primary_title = primary_title[:start]

            # Parse Secondary Language
            secondary_langs = ""
            for lang, code in lang_dict.items():
                if title.text.find(lang) != -1:
                    # print("HERE=================================================================")
                    secondary_langs += (code + ',')
            if secondary_langs.find('eng') == -1 and primary_lang != 'eng':
                if len(alt_title) > 0:
                    secondary_langs += ('eng')
            # print(secondary_langs)
        except AttributeError:
            # print("title: " + primary_title)
            # print("alternate title: " + alt_title)

            # Parse Secondary Language
            secondary_langs = ""
            for lang, code in lang_dict.items():
                if title.text.find(lang) != -1:
                    # print("HERE=================================================================")
                    secondary_langs += (code + ',')
            if secondary_langs.find('eng') == -1 and primary_lang != 'eng':
                if len(alt_title) > 0:
                    secondary_langs += ('eng')
            # print(secondary_langs)

            file_writer.writerow([primary_title, location, date_range, '', primary_lang, secondary_langs, text_type, '', serial_news, '', '', alt_title, ''])
            continue
        # print("title: " + primary_title)
        # print("alternate title: " + alt_title)
        file_writer.writerow([primary_title, location, date_range, '', primary_lang, secondary_langs, text_type, '', serial_news, '', '', alt_title, ''])

# soup = BeautifulSoup(open("list2.html"), "html.parser")
# get_alt_title(soup)

# get_title(soup)

def main():
    try:
        html_file = './country_lists/' + sys.argv[1]
        soup = BeautifulSoup(open(html_file), "html.parser")
        if len(sys.argv) > 2:
            primary_language = sys.argv[2]
            get_title(soup, primary_language)
        else:
            get_title(soup)
    except IndexError:
        # print usage info
        print("Usage: python3 main.py <finnish.html> <primary_language>")
if __name__=='__main__':
    main()