require 'trello'

# Set up Trello API credentials
Trello.configure do |config|
  config.developer_public_key = ENV['TRELLO_DEVELOPER_PUBLIC_KEY']
  config.member_token = ENV['TRELLO_MEMBER_TOKEN']
end

# SidePiece board ID
board_id = ENV['TRELLO_BOARD_ID']

# Get the board
board = Trello::Board.find(board_id)

# Print titles of cards for each column (list) on the board
skipped_boards = []

board.lists.each do |list|
  if list.name.include?('Set ')
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
