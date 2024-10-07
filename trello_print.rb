# frozen_string_literal: true

require 'trello'

# SidePiece board ID
BOARD_ID = ENV['TRELLO_BOARD_ID']
ALL_LISTS = '__ALL__'

# Set up Trello API credentials
Trello.configure do |config|
  config.developer_public_key = ENV['TRELLO_DEVELOPER_PUBLIC_KEY']
  config.member_token = ENV['TRELLO_MEMBER_TOKEN']
end

column_name = ARGV.empty? ? ALL_LISTS : ARGV.join(' ')

# Get the board
board = Trello::Board.find(BOARD_ID)

# Print titles of cards for each column (list) on the board
skipped_boards = []

board.lists.each do |list|
  if list.name.include?(column_name) || column_name == ALL_LISTS
    puts "** #{list.name}"
    list.cards.each do |card|
      puts card.name
    end
    puts
  else
    skipped_boards << list.name
  end
end

puts "\n**Skipped list names:\n#{skipped_boards.join("\n")}"
