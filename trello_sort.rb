# frozen_string_literal: true

require 'trello'

# Set up your Trello API key and token
Trello.configure do |config|
  config.developer_public_key = ENV['TRELLO_DEVELOPER_PUBLIC_KEY']
  config.member_token = ENV['TRELLO_MEMBER_TOKEN']
end

# SidePiece board ID
board_id = ENV['TRELLO_BOARD_ID']
COLUMN_NAME = 'Master Song List'

# Get the Trello board and column
board = Trello::Board.find(board_id)

def reposition_cards(cards)
  cards.each_with_index do |card, idx|
    printf('%<pos>02d : %<idx>02d - %<name>s', card.pos, idx, card.name)
    puts

    next if card.pos == idx

    puts "    Moving card: #{card.pos} : #{idx} - #{card.name}\n"
    card.pos = idx
    card.save
  end
end

board.lists.each do |list|
  next if list.name != COLUMN_NAME

  # Fetch and sort cards by title
  cards = list.cards.sort_by(&:name)
  reposition_cards(cards)
end

puts "\nCards in the [#{COLUMN_NAME}] column have been sorted by title."
