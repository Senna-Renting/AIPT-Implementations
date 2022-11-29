import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * Institute: Radboud University
 * Course: SEM1V (AI: Principles & Techniques)
 * Student: Senna Renting (s1067489)
 * Task: 2
 * Date: 25 November 2022
 */
public class FinalizedFieldSort implements Comparator<List<Field>> {
    /***
     * Compares two arcs with respect to the amount of neighbours, of the first field in the arc, that contain a finalized field
     * @param a the first object to be compared.
     * @param b the second object to be compared.
     */
    public int sort = 0;
    public int compare(List<Field> a, List<Field> b){
        List<Field> neighsA = new ArrayList<Field>();
        neighsA.addAll(a.get(0).getNeighbours());
        List<Field> neighsB = new ArrayList<Field>();
        neighsB.addAll(b.get(0).getNeighbours());
        int finalA = 0;
        int finalB = 0;
        for(int i = 0; i < neighsA.size(); i++){
            sort++;
            if(neighsA.get(i).getDomainSize() == 0)
                finalA++;
        }
        for(int j = 0; j < neighsB.size(); j++){
            sort++;
            if(neighsB.get(j).getDomainSize() == 0)
                finalB++;
        }
        return Integer.compare(finalA, finalB);
    }
}
