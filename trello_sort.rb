require 'trello'

# Set up your Trello API key and token
Trello.configure do |config|
  config.developer_public_key = ENV['TRELLO_DEVELOPER_PUBLIC_KEY']
  config.member_token = ENV['TRELLO_MEMBER_TOKEN']
end

# SidePiece board ID
board_id = ENV['TRELLO_BOARD_ID']
COLUMN_NAME = 'Master Song List'.freeze

# Get the Trello board and column
board = Trello::Board.find(board_id)

def reposition_cards(cards)
  cards.each_with_index do |card, idx|
    printf('%02d : %02d - %s', card.pos, idx, card.name)
    puts
    if card.pos != idx
      puts "    Moving card: #{card.pos} : #{idx} - #{card.name}\n"
      card.pos = idx
      card.save
    end
  end
end

board.lists.each do |list|
  if list.name == COLUMN_NAME
    # Fetch and sort cards by title
    cards = list.cards.sort_by(&:name)
    reposition_cards(cards)
  end
end

puts "\nCards in the [#{COLUMN_NAME}] column have been sorted by title."
