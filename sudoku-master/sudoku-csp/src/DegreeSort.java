import java.util.Comparator;
import java.util.List;

/**
 * Institute: Radboud University
 * Course: SEM1V (AI: Principles & Techniques)
 * Student: Senna Renting (s1067489)
 * Task: 2
 * Date: 25 November 2022
 */
public class DegreeSort implements Comparator<List<Field>> {
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
            List<Field> neighs1 = a.get(0).getNeighbours();
            List<Field> neighs2 = a.get(0).getNeighbours();
            int final1 = 0;
            int final2 = 0;
            for(int i = 0; i < neighs1.size(); i++){
                sort++;
                if(neighs1.get(i).getDomainSize() == 0)
                    final1++;
            }
            for(int j = 0; j < neighs2.size(); j++){
                sort++;
                if(neighs2.get(j).getDomainSize() == 0)
                    final2++;
            }
            return Integer.compare(final2, final1);
        }
    }
}
