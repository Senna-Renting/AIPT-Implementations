import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Institute: Radboud University
 * Course: SEM1V (AI: Principles & Techniques)
 * Student: Senna Renting (s1067489)
 * Task: 2
 * Date: 25 November 2022
 */

public class Sudoku {
  private Field[][] board;

  Sudoku(String filename) {
    this.board = readsudoku(filename);
  }

  @Override
  public String toString() {
    String output = "╔═══════╦═══════╦═══════╗\n";
		for(int i=0;i<9;i++){
      if(i == 3 || i == 6) {
		  	output += "╠═══════╬═══════╬═══════╣\n";
		  }
      output += "║ ";
		  for(int j=0;j<9;j++){
		   	if(j == 3 || j == 6) {
          output += "║ ";
		   	}
         output += board[i][j] + " ";
		  }
		  
      output += "║\n";
	  }
    output += "╚═══════╩═══════╩═══════╝\n";
    return output;
  }

  /**
	 * Reads sudoku from file
	 * @param filename
	 * @return 2d int array of the sudoku
	 */
	public static Field[][] readsudoku(String filename) {
		assert filename != null && filename != "" : "Invalid filename";
		String line = "";
		Field[][] grid = new Field[9][9];
		try {
		FileInputStream inputStream = new FileInputStream(filename);
        Scanner scanner = new Scanner(inputStream);
        for(int i = 0; i < 9; i++) {
        	if(scanner.hasNext()) {
        		line = scanner.nextLine();
        		for(int j = 0; j < 9; j++) {
                  int numValue = Character.getNumericValue(line.charAt(j));
                  if(numValue == 0) {
                    grid[i][j] = new Field();
                  } else if (numValue != -1) {
                    grid[i][j] = new Field(numValue);
                  }
                }
        	}
        }
        scanner.close();
		}
		catch (FileNotFoundException e) {
			System.out.println("error opening file: "+filename);
		}
        addNeighbours(grid);
		return grid;
	}

  /**
   * Adds a list of neighbours to each field, i.e., arcs to be satisfied
   *
   * @param grid a 9x9 grid with the sudoku fields in it.
   */
  private static void addNeighbours(Field[][] grid) {
      // test part:
      //int[] pos = new int[] {0,0};
      //grid[0][0].setNeighbours(findNeighbours(pos, grid));
      // actual part:
      for(int i = 0; i < grid.length; i++) {
          for (int j = 0; j < grid[i].length; j++) {
              int[] pos = new int[]{i, j};
              grid[i][j].setNeighbours(findNeighbours(pos, grid));
          }
      }
  }

    /**
     * Find the neighbours of a field (Helper function of addNeighbours)
     *
     * @param pos coordinates on the grid of the field we want the neighbours of
     * @param grid a 9x9 grid with the sudoku fields in it.
     *
     * @return list of the found neighbours
     */
    private static List<Field> findNeighbours(int[] pos, Field[][] grid){
        // find start position of the block of the variable (pos)
        int blockRow = pos[0] / 3;
        int blockCol = pos[1] / 3;
        List<Field> allNeighbours = new ArrayList<>();
        // find the neighbours in the 3x3 block of parameter pos
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                int row = blockRow*3 + i;
                int col = blockCol*3 + j;
                if(row != pos[0] && col != pos[1]){
                    allNeighbours.add(grid[row][col]);
                }
            }
        }
        //System.out.println(diagNeighbours);
        // add neighbours present on the lines with respect to the variable (pos)
        allNeighbours.addAll(findLineN(pos, true, grid));
        allNeighbours.addAll(findLineN(pos, false, grid));
        // return all the found neighbours
        //System.out.println(diagNeighbours);
        return allNeighbours;
    }

    /**
     * Find the neighbours in either the horizontal, or the vertical line of the field given by the pos parameter and the horizontal conditional parameter
     * @param pos coordinates on the grid of a field
     * @param horizontal if true checks the horizontal line that goes through parameter pos else it checks the vertical line
     * @param grid a 9x9 grid with the sudoku fields in it.
     * @return list of the neighbours found on the specified line with respect to the pos parameter.
     */
    private static List<Field> findLineN(int[] pos, boolean horizontal, Field[][] grid){
        List<Field> lineNeighbours = new ArrayList<>();
        for(int i =0; i < grid.length; i++) {
            if (horizontal) {
                if(i!=pos[1])
                    lineNeighbours.add(grid[pos[0]][i]);
            } else {
                if(i!=pos[0])
                    lineNeighbours.add(grid[i][pos[1]]);
            }
        }
        //System.out.println(lineNeighbours);
        return lineNeighbours;
    }

  /**
	 * Generates fileformat output
	 */
	public String toFileString(){
    String output = "";
    for (int i = 0; i < board.length; i++) {
      for (int j = 0; j < board[0].length; j++) {
        output += board[i][j].getValue();
      }
      output += "\n";
    }
    return output;
	}

  public Field[][] getBoard(){
    return board;
  }
}
