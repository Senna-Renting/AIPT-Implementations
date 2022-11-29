import java.util.*;

/**
 * Institute: Radboud University
 * Course: SEM1V (AI: Principles & Techniques)
 * Student: Senna Renting (s1067489)
 * Task: 2
 * Date: 25 November 2022
 */
public class Game {
  public int domainComparisons = 0;

  public int complexity = 0;
  private Sudoku sudoku;

  // used to indicate which heuristic we want to use within the AC-3 algorithm
  private String heuristic;

  Game(Sudoku sudoku){
    this.sudoku = sudoku;
  }
  // I will use this implementation of the Game class for benchmarking the performance of the AC-3 algorithm, given a few possible heuristic combinations
  Game(Sudoku sudoku, String heuristic) {
    this.sudoku = sudoku;
    this.heuristic = heuristic;
  }

  public Sudoku getSudoku(){
    return this.sudoku;
  }
  public void showSudoku() {
    System.out.println(sudoku);
  }

  /**
   * Implementation of the AC-3 algorithm
   * 
   * @return true if the constraints can be satisfied, else false
   */
  public boolean solve() {
    // get the variables and initialize the worklist
    Field[][] variables = sudoku.getBoard();
    MinRemainValueSort comp1 = new MinRemainValueSort();
    DegreeSort comp3 = new DegreeSort();
    FinalizedFieldSort comp2 = new FinalizedFieldSort();
    StandardOrder comp4 = new StandardOrder();

    // initialize the PriorityQueue with the right Comparator (heuristic) objects
    PriorityQueue<List<Field>> worklist;
    if(heuristic.equals("MinRemainValue")){
      worklist = new PriorityQueue<>(comp1);
    }else if(heuristic.equals("FinalizedField")){
      worklist = new PriorityQueue<>(comp2);
    }else if(heuristic.equals("DegreeSort")){
      worklist = new PriorityQueue<>(comp3);
    }else{
      worklist = new PriorityQueue<>(comp4);
    }

    // get initial arcs of the sudoku
    for(int i =0; i < variables.length; i++){
      for(int j=0; j < variables[0].length; j++){
        // get each individual variable along with its neighbours
        Field variable = variables[i][j];
        List<Field> neighbours = variable.getNeighbours();
        for(int k=0; k < neighbours.size(); k++){
          // make an arc between all the neighbours of each variable
          worklist.add(Arrays.asList(variable, neighbours.get(k)));
        }
      }
    }

      while(worklist.size() > 0) {
        //System.out.println(worklist.size());
        // check a candidate arc and remove it from the list
        List<Field> arc = worklist.poll();
        // reduce domains of the variables contained by the arc
        if (arcReduce(arc)) {
          if (arc.get(0).getDomainSize() == 0) {
            // we failed to find a correct solution
            return false;
          } else {
            // add other neighbours that are influenced by the change of the arc
            List<Field> neighbourss = arc.get(0).getOtherNeighbours(arc.get(1));
            for(int i = 0; i < neighbourss.size(); i++){
                worklist.add(Arrays.asList(neighbourss.get(i), arc.get(0)));
            }
          }
        }
    }
    //System.out.println("count: "+globalCounter);
    //we found a (hopefully) correct solution
    int sortAmount = comp1.sort+comp2.sort+comp3.sort+comp4.sort;
    System.out.print("Domain comparisons: "+domainComparisons + " | sorts: "+sortAmount+" | Complexity: "+(complexity+sortAmount)+"\n");
    return true;
  }

  /**
   * Changes (Reduces) the domain of the first variable each time a domain value of var1 cannot be matched with a domain value of var2
   * @param arc The arc which we want to make consistent
   * @return (boolean) True when the domain of var1 has been changed
   */
  private boolean arcReduce(List<Field> arc){
    boolean change = false;
    Field var1 = arc.get(0);
    Field var2 = arc.get(1);
    if(arc.get(0).getDomainSize() > 0) {
      for (int i = 0; i < var1.getDomainSize(); i++) {
        boolean consistent = false;
        if(var2.getDomainSize() > 0) {
          for (int j = 0; j < var2.getDomainSize(); j++) {
            complexity++;
            domainComparisons++;
            // check each value in the domain of both variables on the constraint X[x] is not equal to Y[x]
            if (!var1.getDomain().get(i).equals(var2.getDomain().get(j))) {
              consistent = true;
              break;
            }
          }
        }else{
          // if the second variable only has a single value (so no domain) check that one!
          if (!var1.getDomain().get(i).equals(var2.getValue())) {
            consistent = true;
          }
        }
        // check if value i of var1 was consistent for some value j of y
        if (!consistent) {
          var1.removeFromDomain(var1.getDomain().get(i));
          //System.out.println(var1.getDomain());
          change = true;
        }
      }
    }
    return change;
  }

  /**
   * Checks the validity of a sudoku solution
   * 
   * @return true if the sudoku solution is correct
   */
  public boolean validSolution() {
    int i = 0;
    while(i < 9){
      if(checkBlock(i) && checkLine(i, true) && checkLine(i, false)){
        i += 1;
      }else{
        return false;
      }
    }
    return true;
  }

  /**
   * Checks the validity of the diagonal blocks on a 3x3 block on a sudoku (helper function of validSolution)
   *
   * X O X
   * O O O
   * X O X
   *
   * @param blockNum the 3x3 block index that specifies the block we want to check
   * @return true if the block is valid else the block is determined invalid by the function
   */
  private boolean checkBlock(int blockNum){
    int rowB = blockNum/3;
    int colB = blockNum%3;
    int row = rowB*3;
    int col = colB*3;

    Field[][] grid = this.sudoku.getBoard();
    List<Integer> values = new ArrayList<>(Arrays.asList(1,2,3,4,5,6,7,8,9));

    for(int i = 0; i < 3; i++){
      for(int j = 0; j < 3; j++){
        if(values.contains(grid[row+i][col+j].getValue())){
          values.remove(Integer.valueOf(grid[row+i][col+j].getValue()));
        }else{
          return false;
        }
      }
    }
    return values.size() == 0;
  }

  /**
   * Checks the validity of a line on a sudoku (helper function of validSolution)
   *
   * @param horizontal when true we check the horizontal line else we check the vertical line
   * @param lineIndex number between 1 and 9 that specifies either the row or the column of the line
   * @return true if line of the sudoku is valid else false
   */
  private boolean checkLine(int lineIndex, boolean horizontal){
    Field[][] grid = this.sudoku.getBoard();
    List<Integer> values = new ArrayList<>(Arrays.asList(1,2,3,4,5,6,7,8,9));

    for(int i = 0; i < 9; i++){
      if(horizontal){
        // check horizontal line
        int value = grid[i][lineIndex].getValue();
        if(values.contains(value)){
          values.remove(Integer.valueOf(value));
        }else{
          return false;
        }
      }else{
        // check vertical lines
        int value = grid[lineIndex][i].getValue();
        if(values.contains(value)){
          values.remove(Integer.valueOf(value));
        }else{
          return false;
        }
      }
    }
    return values.size() == 0;
  }
}
