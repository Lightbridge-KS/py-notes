from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class PieceType(Enum):
    KING = "King"
    QUEEN = "Queen"
    ROOK = "Rook"
    BISHOP = "Bishop"
    KNIGHT = "Knight"
    PAWN = "Pawn"

class Color(Enum):
    WHITE = "White"
    BLACK = "Black"

@dataclass
class Position:
    """
    Represents a position on the chess board.
    
    Parameters
    ----------
    x : int
        The x-coordinate (0-7)
    y : int
        The y-coordinate (0-7)
    chess_board : Board
        Reference to the board this position belongs to
    """
    x: int
    y: int
    chess_board: 'Board'

    def __str__(self) -> str:
        """Convert position to chess notation (e.g., 'a1', 'e4')"""
        return f"{chr(97 + self.x)}{self.y + 1}"

class Piece:
    """
    Represents a chess piece.
    
    Parameters
    ----------
    piece_type : PieceType
        The type of the piece (King, Queen, etc.)
    color : Color
        The color of the piece (White or Black)
    chess_set : ChessSet
        Reference to the chess set this piece belongs to
    """
    def __init__(self, piece_type: PieceType, color: Color, chess_set: 'ChessSet'):
        self.piece_type = piece_type
        self.color = color
        self.chess_set = chess_set
        self.position: Optional[Position] = None

    def __str__(self) -> str:
        return f"{self.color.value} {self.piece_type.value}"

    def move(self, new_position: Position) -> bool:
        """
        Move the piece to a new position.
        
        Parameters
        ----------
        new_position : Position
            The target position to move to
            
        Returns
        -------
        bool
            True if the move was successful, False otherwise
        """
        # Basic validation (implement proper chess rules later)
        if 0 <= new_position.x < 8 and 0 <= new_position.y < 8:
            self.position = new_position
            return True
        return False

class Board:
    """
    Represents the chess board.
    
    Parameters
    ----------
    chess_set : ChessSet
        Reference to the chess set this board belongs to
    """
    def __init__(self, chess_set: 'ChessSet'):
        self.chess_set = chess_set
        self.positions = [[Position(x, y, self) for x in range(8)] for y in range(8)]

    def draw(self):
        """Draw the current state of the board"""
        print("  a b c d e f g h")
        print("  ---------------")
        for y in range(7, -1, -1):
            row = f"{y+1}|"
            for x in range(8):
                piece = self.get_piece_at_position(x, y)
                if piece:
                    symbol = piece.piece_type.value[0]
                    symbol = symbol.lower() if piece.color == Color.BLACK else symbol.upper()
                else:
                    symbol = "."
                row += f"{symbol}|"
            print(row)
        print("  ---------------")

    def get_piece_at_position(self, x: int, y: int) -> Optional[Piece]:
        """
        Get the piece at a specific position.
        
        Parameters
        ----------
        x : int
            The x-coordinate
        y : int
            The y-coordinate
            
        Returns
        -------
        Optional[Piece]
            The piece at the position, or None if empty
        """
        for piece in self.chess_set.pieces:
            if piece.position and piece.position.x == x and piece.position.y == y:
                return piece
        return None

class ChessSet:
    """
    Represents a complete chess set with pieces and board.
    """
    def __init__(self):
        self.board = Board(self)
        self.pieces: List[Piece] = []
        self._initialize_pieces()

    def _initialize_pieces(self):
        """Initialize all chess pieces in their starting positions"""
        # Initialize white pieces
        self._create_pieces(Color.WHITE)
        # Initialize black pieces
        self._create_pieces(Color.BLACK)

    def _create_pieces(self, color: Color):
        """Create pieces for one side"""
        base_row = 0 if color == Color.WHITE else 7
        pawn_row = 1 if color == Color.WHITE else 6

        # Create back row pieces
        piece_types = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]
        
        for x, piece_type in enumerate(piece_types):
            piece = Piece(piece_type, color, self)
            piece.position = Position(x, base_row, self.board)
            self.pieces.append(piece)

        # Create pawns
        for x in range(8):
            pawn = Piece(PieceType.PAWN, color, self)
            pawn.position = Position(x, pawn_row, self.board)
            self.pieces.append(pawn)

class Player:
    """
    Represents a chess player.
    
    Parameters
    ----------
    name : str
        The name of the player
    color : Color
        The color of pieces the player controls
    """
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color

    def make_move(self, chess_set: ChessSet, from_pos: str, to_pos: str) -> bool:
        """
        Make a move on the chess board.
        
        Parameters
        ----------
        chess_set : ChessSet
            The chess set to make the move on
        from_pos : str
            Starting position in chess notation (e.g., 'e2')
        to_pos : str
            Target position in chess notation (e.g., 'e4')
            
        Returns
        -------
        bool
            True if the move was successful, False otherwise
        """
        # Convert chess notation to coordinates
        from_x = ord(from_pos[0].lower()) - 97
        from_y = int(from_pos[1]) - 1
        to_x = ord(to_pos[0].lower()) - 97
        to_y = int(to_pos[1]) - 1

        # Find the piece to move
        piece = chess_set.board.get_piece_at_position(from_x, from_y)
        if not piece or piece.color != self.color:
            return False

        # Create new position and attempt move
        new_position = Position(to_x, to_y, chess_set.board)
        return piece.move(new_position)

# Example usage
def main():
    # Create chess set
    chess_set = ChessSet()
    
    # Create players
    player1 = Player("Player 1", Color.WHITE)
    player2 = Player("Player 2", Color.BLACK)
    
    # Draw initial board
    chess_set.board.draw()
    
    # Example moves
    print("\nMaking some moves:")
    player1.make_move(chess_set, "e2", "e4")  # White pawn move
    chess_set.board.draw()
    
    player2.make_move(chess_set, "e7", "e5")  # Black pawn move
    chess_set.board.draw()

if __name__ == "__main__":
    main()
