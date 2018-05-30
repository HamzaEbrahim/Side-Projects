import requests
from bs4 import BeautifulSoup

def run():
  decklist_page = fetch_decklist_page('http://mtgportal.co.za/decklist?decklistid=779')
  decklist = extract_decklist_from_page(decklist_page)
  deck_dict, sideboard_dict = build_deck_dictionary(decklist)
  print('Main deck in dictionary form:')
  print('%s %s' % ('Number'.ljust(10), 'Card'))
  for card, num in deck_dict.items():
    print('%s %s' % (num.ljust(10), card))
  print('Sideboard in dictionary form:')
  print('%s %s' % ('Number'.ljust(10), 'Card'))
  for card, num in sideboard_dict.items():
    print('%s %s' % (num.ljust(10), card))

def fetch_decklist_page(url):
  r = requests.get(url)
  return r.text

def extract_decklist_from_page(decklist_page):
  soup = BeautifulSoup(decklist_page, 'html.parser')
  return soup.find('div', attrs={'class': 'deck-list'}).text.strip()

def build_deck_dictionary(decklist):
  decklist = decklist.split('\n')
  mb_list = decklist[:decklist.index('sideboard')]
  # Assume that there will always be a sb
  sb_list = decklist[decklist.index('sideboard')+1:]
  # could use a regex here but it's simpler to just do a split because I'm lazy
  deck_dict = {card.split('x')[1].strip():card.split('x')[0] for card in [entry for entry in mb_list] if card}
  side_dict = {card.split('x')[1].strip():card.split('x')[0] for card in [entry for entry in sb_list] if card}
  return deck_dict, side_dict

if __name__ == '__main__':
  run()
