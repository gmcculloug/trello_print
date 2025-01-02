# frozen_string_literal: true

# Usage: ruby trello_print.rb [column_name]
# Description: Print titles of cards for each column (list) on the Trello board
#
# Environment variables:
#   - TRELLO_DEVELOPER_PUBLIC_KEY: Trello developer public key
#   - TRELLO_MEMBER_TOKEN: Trello member token
#   - TRELLO_BOARD_ID: Trello board ID
#   - column_name: Optional column name to filter lists by

require 'trello'

# Set up Trello board ID
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
