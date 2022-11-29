import java.util.Comparator;
import java.util.List;

/**
 * Institute: Radboud University
 * Course: SEM1V (AI: Principles & Techniques)
 * Student: Senna Renting (s1067489)
 * Task: 2
 * Date: 25 November 2022
 */

public class MinRemainValueSort implements Comparator<List<Field>> {
    /***
     * Compares two arcs with respect to the domain size of the second field (the field that gets constrained) in the arc
     * @param a the first object to be compared.
     * @param b the second object to be compared.
     */
    public int sort = 0;
    public int compare(List<Field> a, List<Field> b){
        int cval1 = a.get(1).getDomainSize();
        int cval2 = b.get(1).getDomainSize();
        sort++;
        // compare the domain sizes
        if(cval1 > cval2){
            return 1;
        }else if(cval1 < cval2){
            return -1;
        }else{
            return 0;
        }
        //return Integer.compare(cval2, cval1);
        //System.out.println(value);
    }
}
