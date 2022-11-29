/**
 * Institute: Radboud University
 * Course: SEM1V (AI: Principles & Techniques)
 * Student: Senna Renting (s1067489)
 * Task: 2
 * Date: 25 November 2022
 */

public class App {
    public static void main(String[] args) throws Exception {

        //This is used for testing the overal complexity along with other measures
        //uncomment this if you want to test the function: benchmark();

        //General sudoku solve and show part
        start("Sudoku1.txt", "No heuristic");

        // testing game methods (was used for debugging the algorithm)
        //Game game1 = new Game(new Sudoku("SudokuSolved.txt"));
        //game1.showSudoku();
        //System.out.println(game1.validSolution());

        // testing sudoku neighbour methods (was used for debugging the algorithm)
        //Sudoku sudoku = new Sudoku("Sudoku1.txt");
        //System.out.println(sudoku);
        //sudoku.getBoard()[0][0].getNeighbours().forEach(x -> System.out.println(x.getValue()));
    }

    public static void benchmark(){
        // benchmarking the heuristics with respect to no heuristic on all solvable sudoku's
        String[] hs = new String[]{"MinRemainValue", "FinalizedField", "DegreeSort", "No heuristic"};
        Game[][] games = new Game[hs.length][5];
        // initialize and solve the sudoku's and their respective heuristics
        for(int i =0; i<hs.length; i++){
            System.out.println("\n"+hs[i]+" heuristic:\n");
            games[i][0] = new Game(new Sudoku("Sudoku1.txt"), hs[i]);
            games[i][1] = new Game(new Sudoku("Sudoku2.txt"), hs[i]);
            games[i][2] = new Game(new Sudoku("Sudoku3.txt"), hs[i]);
            games[i][3] = new Game(new Sudoku("Sudoku4.txt"), hs[i]);
            games[i][4] = new Game(new Sudoku("Sudoku5.txt"), hs[i]);
            games[i][0].solve();
            games[i][1].solve();
            games[i][2].solve();
            games[i][3].solve();
            games[i][4].solve();
        }
        // show respective solutions for each method
        for(int i = 0; i < hs.length; i++){
            System.out.println("Solutions for "+hs[i]+": \n");
            games[i][0].showSudoku();
            games[i][1].showSudoku();
            games[i][2].showSudoku();
            games[i][3].showSudoku();
            games[i][4].showSudoku();
        }
    }

    /**
     * Start AC-3 using the sudoku from the given filepath, and reports whether the sudoku could be solved or not, and how many steps the algorithm performed
     * 
     * @param filePath the path to the text file representing a sudoku in a specific format
     * @param heuristic the heuristic we want to apply on the sudoku when applying the AC-3 algorithm on it.
     */
    public static void start(String filePath, String heuristic){
        Game game1 = new Game(new Sudoku(filePath), heuristic);
        game1.showSudoku();

        if (game1.solve() && game1.validSolution()){
            System.out.println("Solved!");
        }
        else{
            System.out.println("Could not solve this sudoku :(");
        }
        game1.showSudoku();
        //showAllDomains(game1.getSudoku());
    }

    /***
     * This is a function I used for testing. It prints the domain (values we can choose) of each field in the sudoku
     * @param s the sudoku we want to check
     */
    public static void showAllDomains(Sudoku s){
        Field[][] grid = s.getBoard();
        for(int i =0; i < grid.length; i++){
            for(int j =0; j < grid[0].length; j++){
                System.out.println(i+","+j+" :"+grid[i][j].getDomain().toString());
            }
        }
    }
}
